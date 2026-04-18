import json

from analyze import evaluate_metric, load_benchmarks


def test_evaluate_metric_pass():
	benchmark = {"name": "Test", "metric": "pe", "max": 20, "weight": 1.0}
	info = {"pe": 15}
	res = evaluate_metric(info, benchmark)
	assert res["status"] == "PASS"
	assert res["score"] == 1.0
	assert res["value"] == "15.00"


def test_evaluate_metric_fail():
	benchmark = {"name": "Test", "metric": "pe", "max": 20, "weight": 1.0}
	info = {"pe": 25}
	res = evaluate_metric(info, benchmark)
	assert res["status"] == "FAIL"
	assert res["score"] == 0


def test_evaluate_metric_na():
	benchmark = {"name": "Test", "metric": "pe", "max": 20, "weight": 1.0}
	info = {}  # Missing metric
	res = evaluate_metric(info, benchmark)
	assert res["status"] == "N/A"
	assert res["weight"] == 0


def test_evaluate_metric_percentage():
	benchmark = {"name": "Test", "metric": "margin", "min": 0.1, "is_percentage": True}
	info = {"margin": 0.15}
	res = evaluate_metric(info, benchmark)
	assert res["value"] == "15.00%"


def test_load_benchmarks_valid(tmp_path):
	d = tmp_path / "sub"
	d.mkdir()
	p = d / "benchmarks.json"
	content = {"benchmarks": [{"name": "Test", "metric": "pe", "max": 20}]}
	p.write_text(json.dumps(content))

	benchmarks = load_benchmarks(str(p))
	assert len(benchmarks) == 1
	assert benchmarks[0]["name"] == "Test"


def test_load_benchmarks_invalid():
	# Should return empty list and print error on missing file
	benchmarks = load_benchmarks("non_existent.json")
	assert benchmarks == []
