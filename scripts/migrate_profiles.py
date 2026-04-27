import json
import logging
from pathlib import Path

from core.database import DatabaseManager, DatabaseRepository

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def migrate():
	db_manager = DatabaseManager()
	repo = DatabaseRepository(db_manager)

	profiles_path = Path("profiles/investor_profiles.json")
	if not profiles_path.exists():
		logger.error("investor_profiles.json not found")
		return

	try:
		with open(profiles_path, "r") as f:
			data = json.load(f)

		profiles = data.get("profiles", {})
		for key, profile_data in profiles.items():
			logger.info(f"Migrating profile: {key}")

			# key is 'balanced', 'growth', etc.
			repo.upsert_profile(name=key, description=profile_data.get("description"))

			weights = profile_data.get("weights", {})
			for metric, weight in weights.items():
				repo.upsert_profile_weight(
					profile_name=key, metric_key=metric, weight=float(weight)
				)

		logger.info("Profile migration complete.")
	except Exception as e:
		logger.error(f"Migration failed: {e}")


if __name__ == "__main__":
	migrate()
