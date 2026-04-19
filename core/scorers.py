import math


def calculate_sigmoid_score(val: float, best: float, worst: float) -> float:
	midpoint = (best + worst) / 2
	try:
		k = math.log(1 / 19) / (best - midpoint)
		score = 1 / (1 + math.exp(k * (val - midpoint)))
	except (ZeroDivisionError, ValueError, OverflowError):
		score = 1.0 if val == best else 0.0
	return score


def calculate_linear_score(val: float, best: float, worst: float) -> float:
	"""Linear scoring. Works for both higher-better and lower-better."""
	if abs(best - worst) < 1e-9:
		return 1.0 if val >= best else 0.0

	if best > worst:  # Higher is better (e.g. ROE)
		pct = (val - worst) / (best - worst)
	else:  # Lower is better (e.g. P/E)
		pct = (worst - val) / (worst - best)

	return max(0.0, min(1.0, pct))


def calculate_bell_score(val: float, target: float, width: float) -> float:
	try:
		return math.exp(-0.5 * ((val - target) / width) ** 2)
	except (ZeroDivisionError, OverflowError):
		return 0.0


def calculate_threshold_score(val: float, threshold: float) -> float:
	return 1.0 if val >= threshold else 0.0


# Registry for easy extension
SCORERS = {
	"sigmoid": calculate_sigmoid_score,
	"linear": calculate_linear_score,
	"bell_curve": calculate_bell_score,
	"threshold": calculate_threshold_score,
}
