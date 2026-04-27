import json
import logging
from pathlib import Path

from core.database import DatabaseManager, DatabaseRepository

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Mapping from JSON camelCase keys to DB snake_case keys
METRIC_NAME_MAP = {
	"forwardPE": "forward_pe",
	"trailingPE": "pe_ratio",
	"pegRatio": "peg_ratio",
	"priceToBook": "price_to_book",
	"returnOnEquity": "return_on_equity",
	"profitMargins": "profit_margin",
	"debtToEquity": "debt_to_equity",
	"currentRatio": "current_ratio",
	"revenueGrowth": "revenue_growth",
	"heldPercentInsiders": "insider_ownership",
	"heldPercentInstitutions": "institution_ownership",
	"dividendYield": "dividend_yield",
	"recommendationMean": "recommendation_mean",
	"payoutRatio": "payout_ratio",
}


def migrate():
	db_manager = DatabaseManager()
	repo = DatabaseRepository(db_manager)

	# Clear existing profile data to ensure clean state
	conn = db_manager.get_connection()
	conn.execute("DELETE FROM profile_weights")
	conn.execute("DELETE FROM investor_profiles")
	conn.commit()

	profiles_path = Path("profiles/investor_profiles.json")
	if not profiles_path.exists():
		# For development: create a dummy json or handle missing
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
				# Map camelCase to snake_case if mapping exists
				db_metric_key = METRIC_NAME_MAP.get(metric, metric)
				repo.upsert_profile_weight(
					profile_name=key, metric_key=db_metric_key, weight=float(weight)
				)

		logger.info("Profile migration complete.")
	except Exception as e:
		logger.error(f"Migration failed: {e}")


if __name__ == "__main__":
	migrate()
