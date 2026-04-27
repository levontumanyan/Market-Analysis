import logging
from typing import List, Optional, Tuple
from .manager import DatabaseManager

logger = logging.getLogger(__name__)

class DatabaseRepository:
	def __init__(self, db_manager: DatabaseManager):
		self.db = db_manager

	def upsert_asset(self, symbol: str, name: Optional[str] = None, asset_type: Optional[str] = None, sector: Optional[str] = None, industry: Optional[str] = None):
		"""Insert or update an asset."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO assets (symbol, name, asset_type, sector, industry, last_updated)
			VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
			ON CONFLICT(symbol) DO UPDATE SET
				name = COALESCE(excluded.name, assets.name),
				asset_type = COALESCE(excluded.asset_type, assets.asset_type),
				sector = COALESCE(excluded.sector, assets.sector),
				industry = COALESCE(excluded.industry, assets.industry),
				last_updated = CURRENT_TIMESTAMP
		""", (symbol, name, asset_type, sector, industry))
		conn.commit()

	def upsert_index(self, symbol: str, name: str, is_etf: bool = False):
		"""Insert or update an index."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO indices (symbol, name, is_etf, last_updated)
			VALUES (?, ?, ?, CURRENT_TIMESTAMP)
			ON CONFLICT(symbol) DO UPDATE SET
				name = excluded.name,
				is_etf = excluded.is_etf,
				last_updated = CURRENT_TIMESTAMP
		""", (symbol, name, is_etf))
		conn.commit()

	def update_index_constituents(self, index_symbol: str, constituents: List[str]):
		"""Replace all constituents for an index."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		
		# First ensure assets exist (minimal entry)
		for symbol in constituents:
			cursor.execute("""
				INSERT OR IGNORE INTO assets (symbol, last_updated)
				VALUES (?, CURRENT_TIMESTAMP)
			""", (symbol,))
		
		# Remove old constituents
		cursor.execute("DELETE FROM index_constituents WHERE index_symbol = ?", (index_symbol,))
		
		# Add new ones
		for symbol in constituents:
			cursor.execute("""
				INSERT INTO index_constituents (index_symbol, asset_symbol)
				VALUES (?, ?)
			""", (index_symbol, symbol))
		
		conn.commit()

	def get_index_constituents(self, index_symbol: str) -> List[str]:
		"""Get constituents for an index from the DB."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			SELECT asset_symbol FROM index_constituents
			WHERE index_symbol = ?
		""", (index_symbol,))
		return [row[0] for row in cursor.fetchall()]

	def get_index(self, symbol: str) -> Optional[dict]:
		"""Get index metadata."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM indices WHERE symbol = ?", (symbol,))
		row = cursor.fetchone()
		return dict(row) if row else None

	def upsert_financial_statement(self, symbol: str, statement_type: str, period_type: str, fiscal_date: str, metric_key: str, value: float):
		"""Insert or update a financial statement line item."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO financial_statements (symbol, statement_type, period_type, fiscal_date, metric_key, value)
			VALUES (?, ?, ?, ?, ?, ?)
		""", (symbol, statement_type, period_type, fiscal_date, metric_key, value))
		conn.commit()

	def create_analysis_snapshot(self, symbol: str, profile: str, total_score: float, results_json: str):
		"""Create a new analysis snapshot."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO analysis_snapshots (symbol, profile, total_score, results_json)
			VALUES (?, ?, ?, ?)
		""", (symbol, profile, total_score, results_json))
		conn.commit()

	def upsert_sector_benchmark(self, sector: str, metric_key: str, benchmark_type: str, value_a: float, value_b: float):
		"""Insert or update a sector-specific benchmark."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO sector_benchmarks (sector, metric_key, benchmark_type, value_a, value_b, last_updated)
			VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
			ON CONFLICT(sector, metric_key) DO UPDATE SET
				benchmark_type = excluded.benchmark_type,
				value_a = excluded.value_a,
				value_b = excluded.value_b,
				last_updated = CURRENT_TIMESTAMP
		""", (sector, metric_key, benchmark_type, value_a, value_b))
		conn.commit()

	def get_sector_benchmarks(self, sector: str) -> List[dict]:
		"""Get all benchmarks for a specific sector."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM sector_benchmarks WHERE sector = ?", (sector,))
		return [dict(row) for row in cursor.fetchall()]

	def insert_metric_history(self, symbol: str, metric_key: str, value: float):
		"""Insert a new metric record."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO metrics_history (symbol, metric_key, value)
			VALUES (?, ?, ?)
		""", (symbol, metric_key, value))
		conn.commit()

	def upsert_profile(self, name: str, description: Optional[str] = None):
		"""Insert or update an investor profile."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO investor_profiles (name, description)
			VALUES (?, ?)
			ON CONFLICT(name) DO UPDATE SET
				description = COALESCE(excluded.description, investor_profiles.description)
		""", (name, description))
		conn.commit()

	def upsert_profile_weight(self, profile_name: str, metric_key: str, weight: float):
		"""Insert or update a weight for a profile."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO profile_weights (profile_name, metric_key, weight)
			VALUES (?, ?, ?)
			ON CONFLICT(profile_name, metric_key) DO UPDATE SET
				weight = excluded.weight
		""", (profile_name, metric_key, weight))
		conn.commit()

	def get_profile_weights(self, profile_name: str) -> dict:
		"""Get all weights for a specific profile as a dictionary."""
		conn = self.db.get_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT metric_key, weight FROM profile_weights WHERE profile_name = ?", (profile_name,))
		return {row["metric_key"]: row["weight"] for row in cursor.fetchall()}
