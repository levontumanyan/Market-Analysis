import json
import logging
from pathlib import Path
from core.database import DatabaseManager, DatabaseRepository

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def migrate():
	db_manager = DatabaseManager()
	repo = DatabaseRepository(db_manager)
	
	sectors_path = Path("benchmarks/sectors.json")
	if not sectors_path.exists():
		logger.error("sectors.json not found")
		return

	try:
		with open(sectors_path, "r") as f:
			data = json.load(f)
		
		for sector, metrics in data.items():
			logger.info(f"Migrating benchmarks for sector: {sector}")
			for metric_key, thresholds in metrics.items():
				# Detect type
				if "best" in thresholds and "worst" in thresholds:
					b_type = "best_worst"
					val_a = thresholds["best"]
					val_b = thresholds["worst"]
				elif "target" in thresholds and "width" in thresholds:
					b_type = "target_width"
					val_a = thresholds["target"]
					val_b = thresholds["width"]
				else:
					logger.warning(f"Unknown threshold format for {sector} -> {metric_key}")
					continue
				
				repo.upsert_sector_benchmark(
					sector=sector,
					metric_key=metric_key,
					benchmark_type=b_type,
					value_a=val_a,
					value_b=val_b
				)
		logger.info("Sector migration complete.")
	except Exception as e:
		logger.error(f"Migration failed: {e}")

if __name__ == "__main__":
	migrate()
