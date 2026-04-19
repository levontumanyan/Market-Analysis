from typing import Any, Dict

from .scorers import SCORERS


def format_display_value(val: float, unit: str | None, is_decimal: bool = False) -> str:
	"""Format the value for human-readable display."""
	if unit == "percentage":
		return f"{val * 100:.2f}%" if is_decimal else f"{val:.2f}%"
	elif unit == "multiplier":
		return f"{val:.2f}x"
	elif unit == "currency":
		return f"${val:,.2f}"
	else:
		return f"{val:.2f}"


def evaluate_metric(info: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
	"""
	Evaluate a single metric for a stock against its benchmark definition.
	Returns formatted result with score.
	"""
	metric_key = benchmark["metric"]
	val = info.get(metric_key)
	weight = benchmark.get("weight", 1.0)
	formula_type = benchmark.get("type", "sigmoid")
	unit = benchmark.get("unit")
	is_decimal = benchmark.get("is_decimal", False)

	# Handle missing or invalid data
	if val is None or not isinstance(val, (int, float)):
		return {
			"status": "N/A",
			"value": "N/A",
			"score": 0.0,
			"weight": 0.0,
			"pct": 0.0,
		}

	# Format value for display
	display_val = format_display_value(val, unit, is_decimal)

	# Calculate percentage score using the appropriate scorer
	scorer = SCORERS.get(formula_type)
	if not scorer:
		pct = 0.0
	elif formula_type == "sigmoid":
		pct = scorer(val, benchmark.get("best", 0), benchmark.get("worst", 100))
	elif formula_type == "linear":
		pct = scorer(val, benchmark.get("best", 0), benchmark.get("worst", 100))
	elif formula_type == "bell_curve":
		pct = scorer(val, benchmark.get("target", 0), benchmark.get("width", 1))
	elif formula_type == "threshold":
		pct = scorer(val, benchmark.get("threshold", 0))
	else:
		pct = 0.0

	score = weight * pct

	return {
		"status": f"{pct * 100:.0f}%",
		"value": display_val,
		"score": score,
		"weight": weight,
		"pct": pct,
	}
