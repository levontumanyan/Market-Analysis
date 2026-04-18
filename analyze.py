import json
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


def evaluate_metric(info: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
	metric_key = benchmark["metric"]
	val = info.get(metric_key)
	weight = benchmark.get("weight", 1.0)

	if val is None:
		return {"status": "N/A", "value": "N/A", "score": 0, "weight": 0}

	passed = True
	if "min" in benchmark and val < benchmark["min"]:
		passed = False
	if "max" in benchmark and val > benchmark["max"]:
		passed = False

	status = "PASS" if passed else "FAIL"
	score = weight if passed else 0

	display_val = f"{val:.2f}"
	if benchmark.get("is_percentage"):
		display_val = f"{val * 100:.2f}%" if abs(val) < 1.0 else f"{val:.2f}%"

	return {"status": status, "value": display_val, "score": score, "weight": weight}


def get_stock_data(ticker_symbol: str) -> Dict[str, Any]:
	ticker = yf.Ticker(ticker_symbol)
	return ticker.info


def display_results(
	ticker_symbol: str,
	company_name: str,
	results: List[Dict[str, Any]],
	benchmark_defs: List[Dict[str, Any]],
):
	table = Table(title=f"Analysis for {company_name} ({ticker_symbol})")
	table.add_column("Metric", style="cyan")
	table.add_column("Value", justify="right")
	table.add_column("Status", justify="center")
	table.add_column("Weight", justify="right")

	total_score = 0
	total_weight = 0

	for res, b_def in zip(results, benchmark_defs):
		status_str = res["status"]
		status_style = {"PASS": "bold green", "FAIL": "bold red"}.get(status_str, "dim")

		table.add_row(
			b_def["name"],
			res["value"],
			f"[{status_style}]{status_str}[/{status_style}]",
			str(b_def.get("weight", 1.0)),
		)

		total_score += res["score"]
		total_weight += res["weight"]

	console.print(table)

	if total_weight > 0:
		final_pct = (total_score / total_weight) * 100
		color = "green" if final_pct >= 70 else "yellow" if final_pct >= 40 else "red"
		console.print(
			f"\n[bold]FINAL SCORE: [/bold][bold {color}]{total_score:.1f}/{total_weight:.1f} ({final_pct:.1f}%)[/bold {color}]"
		)
	else:
		console.print("\n[bold red]Insufficient data to calculate score.[/bold red]")


def main():
	if len(sys.argv) < 2:
		console.print("[bold red]Error:[/bold red] No ticker symbol provided.")
		console.print(
			"[yellow]Usage:[/yellow] uv run analyze.py <TICKER> (e.g., uv run analyze.py MSFT)"
		)
		sys.exit(1)

	ticker_symbol = sys.argv[1].upper()
	benchmark_defs = load_benchmarks("benchmarks.json")

	if not benchmark_defs:
		sys.exit(1)

	with Progress(transient=True) as progress:
		progress.add_task(f"[green]Fetching data for {ticker_symbol}...", total=None)
		try:
			info = get_stock_data(ticker_symbol)
		except Exception as e:
			console.print(f"[bold red]Error fetching data:[/bold red] {e}")
			sys.exit(1)

	if not info or "symbol" not in info:
		console.print(
			f"[bold red]Error:[/bold red] Could not find data for {ticker_symbol}"
		)
		sys.exit(1)

	results = [evaluate_metric(info, b) for b in benchmark_defs]

	display_results(
		ticker_symbol, info.get("longName", ticker_symbol), results, benchmark_defs
	)


if __name__ == "__main__":
	main()
