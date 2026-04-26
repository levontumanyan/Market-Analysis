import json

from core.data import load_benchmarks


def test_load_benchmarks_with_sector_overrides(tmp_path):
	benchmarks_file = tmp_path / "test_benchmarks.json"
	data = {
		"global": [
			{"name": "PE", "metric": "trailingPE", "best": 15, "worst": 30},
			{"name": "Margin", "metric": "margin", "best": 20, "worst": 10},
		],
		"sector_overrides": {"Tech": {"trailingPE": {"best": 25, "worst": 40}}},
	}
	benchmarks_file.write_text(json.dumps(data))

	# Test Global
	global_b = load_benchmarks(str(benchmarks_file))
	pe_b = next(b for b in global_b if b["metric"] == "trailingPE")
	assert pe_b["best"] == 15

	# Test Sector Override
	tech_b = load_benchmarks(str(benchmarks_file), sector="Tech")
	tech_pe_b = next(b for b in tech_b if b["metric"] == "trailingPE")
	assert tech_pe_b["best"] == 25
	# Margin should still be global
	tech_margin_b = next(b for b in tech_b if b["metric"] == "margin")
	assert tech_margin_b["best"] == 20

	# Test Unknown Sector (should fallback to global)
	unknown_b = load_benchmarks(str(benchmarks_file), sector="Agriculture")
	assert unknown_b == data["global"]
