import json

from core.data import load_benchmarks


def test_load_benchmarks_with_sector_overrides(tmp_path, mocker):
	# 1. Create a global defaults file
	global_file = tmp_path / "stock.json"
	global_data = [
		{"name": "PE", "metric": "trailingPE", "best": 15, "worst": 30},
		{"name": "Margin", "metric": "margin", "best": 20, "worst": 10},
	]
	global_file.write_text(json.dumps(global_data))

	# 2. Create a sector overrides file
	sectors_file = tmp_path / "sectors.json"
	sectors_data = {"Tech": {"trailingPE": {"best": 25, "worst": 40}}}
	sectors_file.write_text(json.dumps(sectors_data))

	# Mock SECTORS_PATH in core.data to point to our test sectors file
	mocker.patch("core.data.SECTORS_PATH", str(sectors_file))

	# Test Global (no sector provided)
	global_b = load_benchmarks(str(global_file))
	pe_b = next(b for b in global_b if b["metric"] == "trailingPE")
	assert pe_b["best"] == 15

	# Test Sector Override
	tech_b = load_benchmarks(str(global_file), sector="Tech")
	tech_pe_b = next(b for b in tech_b if b["metric"] == "trailingPE")
	assert tech_pe_b["best"] == 25
	# Margin should still be global
	tech_margin_b = next(b for b in tech_b if b["metric"] == "margin")
	assert tech_margin_b["best"] == 20

	# Test Unknown Sector (should fallback to global)
	unknown_b = load_benchmarks(str(global_file), sector="Agriculture")
	assert unknown_b == global_data
