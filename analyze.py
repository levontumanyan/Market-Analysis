import json
import math
import sys
from typing import Any, Dict, List

import yfinance as yf
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

console = Console()


def load_benchmarks(file_path: str) -> List[Dict[str, Any]]:
	try:
		with open(file_path, "r") as f:
			data = json.load(f)
			return data.get("benchmarks", [])
	except Exception as e:
		console.print(f"[bold red]Error loading benchmarks.json:[/bold red] {e}")
		return []


def calculate_sigmoid_score(val: float, best: float, worst: float) -> float:
	"""
	Calculates a score between 0 and 1 using a sigmoid (S-curve) function.
	The curve is centered at the midpoint between best and worst.
	"""
	midpoint = (best + worst) / 2
	# Calculate k (steepness) such that 'best' gets ~0.95 and 'worst' gets ~0.05
	# 0.95 = 1 / (1 + exp(k * (best - midpoint)))
	# ln(1/0.95 - 1) = k * (best - midpoint)
	# k = ln(1/19) / (best - midpoint)
	try:
		k = math.log(1 / 19) / (best - midpoint)
	except (ZeroDivisionError, ValueError):
		k = 0.1  # Fallback

	# Sigmoid formula: 1 / (1 + exp(k * (x - midpoint)))
	try:
		score = 1 / (1 + math.exp(k * (val - midpoint)))
	except OverflowError:
		score = 1.0 if (k * (val - midpoint)) < 0 else 0.0

	return score


def evaluate_metric(info: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
	metric_key = benchmark["metric"]
	val = info.get(metric_key)
	weight = benchmark.get("weight", 1.0)
	best = benchmark.get("best")
	worst = benchmark.get("worst")

	if val is None or best is None or worst is None:
		return {"status": "N/A", "value": "N/A", "score": 0, "weight": 0, "pct": 0}

	# Use Sigmoid Scoring
	pct = calculate_sigmoid_score(val, best, worst)
	score = weight * pct

	display_val = f"{val:.2f}"
	if benchmark.get("is_percentage"):
		display_val = f"{val * 100:.2f}%" if abs(val) < 1.0 else f"{val:.2f}%"

	return {
		"status": f"{pct * 100:.0f}%",
		"value": display_val,
		"score": score,
		"weight": weight,
		"pct": pct,
	}


def get_stock_data(ticker_symbol: str) -> Dict[str, Any]:
	ticker = yf.Ticker(ticker_symbol)
	return ticker.info


def get_color_for_pct(pct: float) -> str:
	if pct >= 0.9:
		return "bold green"
	if pct >= 0.7:
		return "green"
	if pct >= 0.4:
		return "yellow"
	return "red"


def display_results(
	ticker_symbol: str,
	company_name: str,
	results: List[Dict[str, Any]],
	benchmark_defs: List[Dict[str, Any]],
):
	table = Table(title=f"Analysis for {company_name} ({ticker_symbol})")
	table.add_column("Metric", style="cyan")
	table.add_column("Value", justify="right")
	table.add_column("Strength", justify="center")
	table.add_column("Points", justify="right")

	total_score = 0
	total_weight = 0

	for res, b_def in zip(results, benchmark_defs):
		if res["weight"] == 0:
			status_style = "dim"
			points_str = "N/A"
		else:
			status_style = get_color_for_pct(res["pct"])
			points_str = f"{res['score']:.2f}/{res['weight']:.1f}"

		table.add_row(
			b_def["name"],
			res["value"],
			f"[{status_style}]{res['status']}[/{status_style}]",
			points_str,
		)

		total_score += res["score"]
		total_weight += res["weight"]

	console.print(table)

	if total_weight > 0:
		final_pct = (total_score / total_weight) * 100
		color = (
			"bold green" if final_pct >= 70 else "yellow" if final_pct >= 40 else "red"
		)
		console.print(
			f"\n[bold]FINAL SCORE: [/bold][{color}]{total_score:.2f}/{total_weight:.1f} ({final_pct:.1f}%)[/{color}]\n"
		)
	else:
		console.print("\n[bold red]Insufficient data to calculate score.[/bold red]\n")


def main():
	if len(sys.argv) < 2:
		console.print("[bold red]Error:[/bold red] No ticker symbol provided.")
		console.print(
			"[yellow]Usage:[/yellow] uv run analyze.py <TICKER1> <TICKER2> ... (e.g., uv run analyze.py AAPL MSFT)"
		)
		sys.exit(1)

	tickers = sys.argv[1:]
	benchmark_defs = load_benchmarks("benchmarks.json")

	if not benchmark_defs:
		sys.exit(1)

	for ticker_symbol in tickers:
		ticker_symbol = ticker_symbol.upper()
		with Progress(transient=True) as progress:
			progress.add_task(
				f"[green]Fetching data for {ticker_symbol}...", total=None
			)
			try:
				info = get_stock_data(ticker_symbol)
			except Exception as e:
				console.print(
					f"[bold red]Error fetching data for {ticker_symbol}:[/bold red] {e}"
				)
				continue

		if not info or "symbol" not in info:
			console.print(
				f"[bold red]Error:[/bold red] Could not find data for {ticker_symbol}"
			)
			continue

		results = [evaluate_metric(info, b) for b in benchmark_defs]

		display_results(
			ticker_symbol, info.get("longName", ticker_symbol), results, benchmark_defs
		)


if __name__ == "__main__":
	main()
