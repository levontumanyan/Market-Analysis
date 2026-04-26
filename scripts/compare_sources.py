import json
from pathlib import Path
from typing import Any, Dict

from config import CACHE_DIR, FMP_CACHE_DIR


def load_json(path: Path) -> Dict[str, Any]:
	if path.exists():
		try:
			return json.loads(path.read_text())
		except Exception:
			return {}
	return {}


def compare_values(v1: Any, v2: Any, threshold: float = 0.1) -> bool:
	"""Return True if values are significantly different."""
	if v1 is None or v2 is None:
		return False  # Can't compare missing data

	try:
		v1, v2 = float(v1), float(v2)
		if v1 == 0 or v2 == 0:
			return abs(v1 - v2) > threshold
		# Check relative difference
		diff = abs(v1 - v2) / max(abs(v1), abs(v2))
		return diff > threshold
	except Exception:
		return str(v1) != str(v2)


def run_comparison():
	print(f"{'Ticker':<8} | {'Metric':<20} | {'FMP':<12} | {'Yahoo':<12} | {'Diff %'}")
	print("-" * 70)

	# Get all tickers from FMP cache
	fmp_files = list(FMP_CACHE_DIR.glob("*.json"))

	metrics_to_check = {
		"trailingPE": ("quote", "pe"),
		"forwardPE": ("key_metrics", "forwardPeRatio"),
		"pegRatio": ("key_metrics", "pegRatio"),
		"priceToBook": ("key_metrics", "pbRatio"),
		"returnOnEquity": ("ratios", "returnOnEquity"),
		"profitMargins": ("ratios", "netProfitMargin"),
		"currentRatio": ("ratios", "currentRatio"),
	}

	for fmp_path in fmp_files:
		ticker = fmp_path.stem
		yf_path = CACHE_DIR / f"{ticker}.json"

		fmp_data = load_json(fmp_path)
		yf_data = load_json(yf_path)

		if not yf_data:
			continue

		for internal_key, (fmp_cat, fmp_key) in metrics_to_check.items():
			f_val = fmp_data.get(fmp_cat, {}).get(fmp_key)
			y_val = yf_data.get(internal_key)

			if compare_values(f_val, y_val):
				try:
					diff_pct = (
						abs(float(f_val) - float(y_val))
						/ max(abs(float(f_val)), abs(float(y_val)))
						* 100
					)
					diff_str = f"{diff_pct:.1f}%"
				except Exception:
					diff_str = "N/A"

				print(
					f"{ticker:<8} | {internal_key:<20} | {str(f_val)[:12]:<12} | {str(y_val)[:12]:<12} | {diff_str}"
				)


if __name__ == "__main__":
	run_comparison()
