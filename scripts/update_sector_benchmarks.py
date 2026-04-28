import logging

from core.database import DatabaseManager, DatabaseRepository

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
	db_manager = DatabaseManager()
	repo = DatabaseRepository(db_manager)

	# --- TECHNOLOGY ---
	# Price to Book: Semiconductor average ~13x, NVIDIA ~33x-40x.
	logger.info("Updating Technology sector Price to Book benchmark...")
	repo.upsert_sector_benchmark(
		sector="Technology",
		metric_key="price_to_book",
		benchmark_type="best_worst",
		value_a=10.0,
		value_b=60.0,
	)

	# EV/EBITDA: Industry average ~27.5x, NVIDIA ~39x.
	# Setting Best=15.0 (Great value for Tech) and Worst=50.0 (High premium)
	logger.info("Updating Technology sector EV/EBITDA benchmark...")
	repo.upsert_sector_benchmark(
		sector="Technology",
		metric_key="enterprise_to_ebitda",
		benchmark_type="best_worst",
		value_a=15.0,
		value_b=50.0,
	)

	# --- FINANCIAL SERVICES ---
	# Price to Book: Best=1.0, Worst=3.5
	logger.info("Updating Financial Services sector Price to Book benchmark...")
	repo.upsert_sector_benchmark(
		sector="Financial Services",
		metric_key="price_to_book",
		benchmark_type="best_worst",
		value_a=1.0,
		value_b=3.5,
	)

	logger.info("Database update complete.")


if __name__ == "__main__":
	main()
