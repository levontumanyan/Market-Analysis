import json

import pytest

from core.data import load_benchmarks
from core.database import DatabaseManager, DatabaseRepository


@pytest.fixture
def repo(tmp_path):
	db_file = tmp_path / "test_market_sectors.db"
	manager = DatabaseManager(str(db_file))
	repo = DatabaseRepository(manager)

	# Seed for tests
	repo.upsert_sector_benchmark("Tech", "trailingPE", "best_worst", 25.0, 40.0)

	yield repo
	manager.close()


def test_load_benchmarks_with_sector_overrides(tmp_path, repo):
	# 1. Create a global defaults file
	global_file = tmp_path / "stock.json"
	global_data = [
		{"name": "PE", "metric": "trailingPE", "best": 15, "worst": 30},
		{"name": "Margin", "metric": "margin", "best": 20, "worst": 10},
	]
	global_file.write_text(json.dumps(global_data))

	# Test Global (no sector provided)
	global_b = load_benchmarks(str(global_file))
	pe_b = next(b for b in global_b if b["metric"] == "trailingPE")
	assert pe_b["best"] == 15

	# Test Sector Override from DB
	tech_b = load_benchmarks(str(global_file), sector="Tech", repo=repo)
	tech_pe_b = next(b for b in tech_b if b["metric"] == "trailingPE")
	assert tech_pe_b["best"] == 25
	assert tech_pe_b["worst"] == 40
	# Margin should still be global
	tech_margin_b = next(b for b in tech_b if b["metric"] == "margin")
	assert tech_margin_b["best"] == 20

	# Test Unknown Sector (should fallback to global)
	unknown_b = load_benchmarks(str(global_file), sector="Agriculture", repo=repo)
	assert unknown_b == global_data
