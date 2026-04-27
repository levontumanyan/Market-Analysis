import json
import logging
from pathlib import Path

from core.database import DatabaseManager, DatabaseRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
	db_manager = DatabaseManager()
	repo = DatabaseRepository(db_manager)

	cache_dir = Path("cache/yfinance")
	if not cache_dir.exists():
		logger.error("Cache directory not found")
		return

	files = list(cache_dir.glob("*.json"))
	logger.info(f"Found {len(files)} files to migrate")

	for file_path in files:
		try:
			data = json.loads(file_path.read_text())
			symbol = data.get("symbol")
			if not symbol:
				continue

			name = data.get("name") or data.get("long_name")
			sector = data.get("sector")
			industry = data.get("industry_category") or data.get("industry")

			# Asset Type heuristic
			asset_type = "STOCK"
			if (
				"fund_family" in data
				or "nav_price" in data
				or data.get("issue_type") == "etf"
			):
				asset_type = "ETF"

			repo.upsert_asset(
				symbol=symbol,
				name=name,
				asset_type=asset_type,
				sector=sector,
				industry=industry,
			)
			logger.info(f"Migrated {symbol}")
		except Exception as e:
			logger.error(f"Failed to migrate {file_path.name}: {e}")


if __name__ == "__main__":
	migrate()
