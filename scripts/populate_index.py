import argparse
import logging

from core.analysis.indices import get_index_components
from core.database import DatabaseManager, DatabaseRepository

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
	parser = argparse.ArgumentParser(
		description="Populate index constituents in the database without analysis."
	)
	parser.add_argument(
		"index", help="Ticker of the index or ETF (e.g., NASDAQ100, SP500)"
	)
	args = parser.parse_args()

	db_manager = DatabaseManager()
	repo = DatabaseRepository(db_manager)

	logger.info(f"Populating constituents for {args.index}...")
	components = get_index_components(args.index, repo=repo)

	if components and len(components) > 1:
		logger.info(
			f"Successfully populated {len(components)} constituents for {args.index} in the database."
		)
	else:
		logger.warning(
			f"Could not find constituents for {args.index}. Only found: {components}"
		)


if __name__ == "__main__":
	main()
