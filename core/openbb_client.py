import json
import random
import time
from typing import Any, Dict

from openbb import obb

from config import CACHE_DIR
from core.logger import get_logger
from core.stats import stats

logger = get_logger(__name__)


def get_openbb_data(ticker_symbol: str) -> Dict[str, Any]:
	"""
	Fetch standardized data via OpenBB Platform using multiple endpoints.
	Handles 3-hour local caching.
	"""
	ticker_symbol = ticker_symbol.upper()
	cache_file = CACHE_DIR / f"{ticker_symbol}.json"

	# 1. Return cache if fresh (< 3 hour)
	if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < 10800:
		try:
			logger.info(f"Cache hit for {ticker_symbol}")
			stats.cache_hits += 1
			return json.loads(cache_file.read_text())
		except Exception as e:
			logger.warning(f"Failed to read cache for {ticker_symbol}: {e}")
			pass

	# 2. Fetch fresh data
	logger.info(f"Fetching fresh data for {ticker_symbol} from OpenBB")
	stats.api_calls += 1
	try:
		combined_data = {}
		provider = "yfinance"

		# Helper to merge OpenBB result into combined_data
		def merge_res(res):
			data = res.to_dict()
			if not data:
				return

			# If it's a dict of lists (standard metrics format)
			if isinstance(data, dict) and any(
				isinstance(v, list) for v in data.values()
			):
				for k, v in data.items():
					if isinstance(v, list) and len(v) > 0:
						combined_data[k] = v[0]
					else:
						combined_data[k] = v
			# If it's a list of dicts (standard profile/consensus format)
			elif isinstance(data, list) and len(data) > 0:
				combined_data.update(data[0])
			# If it's just a dict
			elif isinstance(data, dict):
				combined_data.update(data)

		# Endpoint 1: Fundamental Metrics (Stocks)
		try:
			merge_res(
				obb.equity.fundamental.metrics(symbol=ticker_symbol, provider=provider)
			)
		except Exception as e:
			logger.debug(f"Metrics fetch failed for {ticker_symbol}: {e}")

		# Endpoint 2: Company Profile (Stocks)
		try:
			merge_res(obb.equity.profile(symbol=ticker_symbol, provider=provider))
		except Exception as e:
			logger.debug(f"Profile fetch failed for {ticker_symbol}: {e}")

		# Endpoint 3: Analyst Consensus (Stocks)
		try:
			merge_res(
				obb.equity.estimates.consensus(symbol=ticker_symbol, provider=provider)
			)
		except Exception as e:
			logger.debug(f"Consensus fetch failed for {ticker_symbol}: {e}")

		# Endpoint 4: Ownership Statistics (Stocks)
		try:
			merge_res(
				obb.equity.ownership.share_statistics(
					symbol=ticker_symbol, provider=provider
				)
			)
		except Exception as e:
			logger.debug(f"Ownership fetch failed for {ticker_symbol}: {e}")

		# Endpoint 5: ETF Info (if above fails or it is an ETF)
		if (
			not combined_data
			or "fund_family" in str(combined_data)
			or not combined_data.get("name")
		):
			try:
				merge_res(obb.etf.info(symbol=ticker_symbol, provider=provider))
			except Exception as e:
				logger.debug(f"ETF info fetch failed for {ticker_symbol}: {e}")

		if not combined_data:
			logger.warning(f"No data retrieved for {ticker_symbol}")
			return {}

		# Save to cache
		CACHE_DIR.mkdir(parents=True, exist_ok=True)
		cache_file.write_text(json.dumps(combined_data, default=str, indent="\t"))

		# Light rate limiting
		time.sleep(random.uniform(0.6, 1.1))
		return combined_data

	except Exception as e:
		logger.error(f"OpenBB overall error for {ticker_symbol}: {e}")
		stats.errors += 1
		return {}
