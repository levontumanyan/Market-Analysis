import json
import pytest
from analyze import evaluate_metric, load_benchmarks, calculate_sigmoid_score

def test_sigmoid_math():
	# best=10, worst=30. Midpoint is 20.
	assert calculate_sigmoid_score(10, 10, 30) == pytest.approx(0.95, abs=0.01)
	assert calculate_sigmoid_score(30, 10, 30) == pytest.approx(0.05, abs=0.01)
	assert calculate_sigmoid_score(20, 10, 30) == pytest.approx(0.50, abs=0.01)

def test_evaluate_metric_sigmoid_best():
	# Higher is better: 20 is best, 10 is worst. 20 should get ~95%
	benchmark = {"name": "Test", "metric": "roe", "best": 20, "worst": 10, "weight": 1.0}
	info = {"roe": 20}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == pytest.approx(0.95, abs=0.01)

def test_evaluate_metric_sigmoid_worst():
	# Lower is better: 10 is best, 30 is worst. 30 should get ~5%
	benchmark = {"name": "Test", "metric": "pe", "best": 10, "worst": 30, "weight": 1.0}
	info = {"pe": 30}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == pytest.approx(0.05, abs=0.01)

def test_evaluate_metric_na():
	benchmark = {"name": "Test", "metric": "pe", "best": 10, "worst": 30}
	info = {} # Missing metric
	res = evaluate_metric(info, benchmark)
	assert res["value"] == "N/A"
	assert res["weight"] == 0

def test_evaluate_metric_percentage_display():
	benchmark = {"name": "Test", "metric": "margin", "best": 0.2, "worst": 0.0, "is_percentage": True}
	info = {"margin": 0.1} # Midpoint (50%)
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
