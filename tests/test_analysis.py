import pytest
from analyze import evaluate_metric, calculate_sigmoid_score, calculate_linear_score, calculate_bell_score, calculate_threshold_score

def test_sigmoid_math():
	assert calculate_sigmoid_score(10, 10, 30) == pytest.approx(0.95, abs=0.01)
	assert calculate_sigmoid_score(20, 10, 30) == pytest.approx(0.50, abs=0.01)

def test_linear_math():
	# Higher is better: 20 best, 10 worst. 15 is 50%.
	assert calculate_linear_score(15, 20, 10) == 0.5
	# Lower is better: 10 best, 20 worst. 15 is 50%.
	assert calculate_linear_score(15, 10, 20) == 0.5
	# Clamping
	assert calculate_linear_score(25, 20, 10) == 1.0
	assert calculate_linear_score(5, 20, 10) == 0.0

def test_bell_curve_math():
	# Target 50, width 10. 50 should be 1.0
	assert calculate_bell_score(50, 50, 10) == 1.0
	# Should drop as we move away
	assert calculate_bell_score(60, 50, 10) < 1.0
	assert calculate_bell_score(40, 50, 10) < 1.0

def test_threshold_math():
	assert calculate_threshold_score(0.025, 0.02) == 1.0
	assert calculate_threshold_score(0.015, 0.02) == 0.0

def test_evaluate_metric_dispatch():
	# Test Bell Curve dispatch
	benchmark = {"name": "Debt", "metric": "d2e", "type": "bell_curve", "target": 50, "width": 10}
	info = {"d2e": 50}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == 1.0
	
	# Test Threshold dispatch
	benchmark = {"name": "Div", "metric": "yield", "type": "threshold", "threshold": 0.02}
	info = {"yield": 0.03}
	res = evaluate_metric(info, benchmark)
	assert res["pct"] == 1.0
