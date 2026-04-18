import json
import pytest
from analyze import evaluate_metric, load_benchmarks

def test_evaluate_metric_best():
	# Higher is better: 20 is best, 10 is worst. 25 should be 1.0 (100%)
	benchmark = {"name": "Test", "metric": "roe", "best": 20, "worst": 10, "weight": 1.0}
	info = {"roe": 25}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == 1.0
	assert res["score"] == 1.0

def test_evaluate_metric_worst():
	# Lower is better: 10 is best, 30 is worst. 35 should be 0.0 (0%)
	benchmark = {"name": "Test", "metric": "pe", "best": 10, "worst": 30, "weight": 1.0}
	info = {"pe": 35}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == 0.0
	assert res["score"] == 0.0

def test_evaluate_metric_midpoint():
	# Lower is better: 10 is best, 30 is worst. 20 is exactly in middle.
	benchmark = {"name": "Test", "metric": "pe", "best": 10, "worst": 30, "weight": 2.0}
	info = {"pe": 20}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == 0.5
	assert res["score"] == 1.0 # 0.5 * 2.0 weight

def test_evaluate_metric_na():
	benchmark = {"name": "Test", "metric": "pe", "best": 10, "worst": 30}
	info = {} # Missing metric
	res = evaluate_metric(info, benchmark)
	assert res["value"] == "N/A"
	assert res["weight"] == 0

def test_evaluate_metric_percentage_display():
	benchmark = {"name": "Test", "metric": "margin", "best": 0.2, "worst": 0.0, "is_percentage": True}
	info = {"margin": 0.1} # 50% strength
	res = evaluate_metric(info, benchmark)
	assert res["value"] == "10.00%"
	assert res["status"] == "50%"

def test_load_benchmarks_valid(tmp_path):
	d = tmp_path / "sub"
	d.mkdir()
	p = d / "benchmarks.json"
	content = {
		"benchmarks": [{"name": "Test", "metric": "pe", "best": 10, "worst": 30}]
	}
	p.write_text(json.dumps(content))
	
	benchmarks = load_benchmarks(str(p))
	assert len(benchmarks) == 1
	assert benchmarks[0]["best"] == 10
