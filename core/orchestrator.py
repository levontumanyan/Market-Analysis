from typing import Any, Dict, List, Optional

from core.data import get_stock_data, load_benchmarks
from core.evaluation import evaluate_metric
from core.profiles import get_profile_weights
from core.schema import AssetType


def analyze_asset(
	symbol: str, profile: str, benchmark_path: str | None = None
) -> Optional[Dict[str, Any]]:
	"""
	Analyze a single asset and return the results and score.
	"""
	asset = get_stock_data(symbol)
	if not asset:
		return None

	# Determine benchmark file based on asset type if not explicitly provided
	if not benchmark_path:
		if asset.asset_type == AssetType.ETF:
			benchmark_path = "benchmarks_etf.json"
		else:
			benchmark_path = "benchmarks_stock.json"

	# Load benchmarks with sector context for stocks
	sector_context = asset.sector if asset.asset_type == AssetType.STOCK else None
	benchmark_defs = load_benchmarks(benchmark_path, sector=sector_context)

	if not benchmark_defs:
		return None

	profile_weights = get_profile_weights(profile)
	results = [evaluate_metric(asset, b, profile_weights) for b in benchmark_defs]

	# Calculate total score
	total_score = 0.0
	max_score = 0.0
	for res in results:
		total_score += res["score"]
		max_score += res["weight"]

	final_pct = (total_score / max_score * 100) if max_score > 0 else 0.0

	return {
		"symbol": asset.symbol,
		"name": asset.display_name,
		"sector": asset.sector,
		"industry": asset.industry,
		"results": results,
		"benchmark_defs": benchmark_defs,
		"score": final_pct,
		"asset_type": asset.asset_type,
	}


def run_bulk_analysis(
	tickers: List[str],
	profile: str,
	benchmark_path: str | None = None,
	progress_callback: Optional[Any] = None,
) -> List[Dict[str, Any]]:
	"""
	Run analysis for multiple tickers.
	"""
	all_results = []
	for ticker in tickers:
		ticker = ticker.upper().strip()
		try:
			res = analyze_asset(ticker, profile, benchmark_path)
			if res:
				all_results.append(res)
				if progress_callback:
					progress_callback(res)
		except Exception as e:
			# In a real app, we might log this properly
			print(f"Error analyzing {ticker}: {e}")

	return all_results
