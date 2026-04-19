import argparse
import sys

from rich.console import Console

from core.data import get_stock_data, load_benchmarks
from core.display import display_results
from core.evaluation import evaluate_metric
from core.profiles import get_profile_weights

console = Console()


def main():
	parser = argparse.ArgumentParser(description="Stock Fundamental Analyzer")
	parser.add_argument("tickers", nargs="+", help="One or more ticker symbols")
	parser.add_argument(
		"-b", "--benchmarks", default="benchmarks.json", help="Path to benchmarks file"
	)
	parser.add_argument(
		"-p",
		"--profile",
		default="balanced",
		choices=["balanced", "growth", "dividend"],
		help="Investment profile to use",
	)
	args = parser.parse_args()

	benchmark_defs = load_benchmarks()
	if not benchmark_defs:
		console.print("[bold red]Error: Could not load benchmarks.[/bold red]")
		sys.exit(1)

	# Get weights for selected profile
	profile_weights = get_profile_weights(args.profile)
	console.print(
		f"[bold green]Analyzing with [cyan]{args.profile.upper()}[/cyan] profile[/bold green]"
	)

	for ticker in args.tickers:
		ticker = ticker.upper().strip()
		console.print(f"\n[bold green]Analyzing {ticker}...[/bold green]")

		try:
			info = get_stock_data(ticker)
			if not info or "symbol" not in info:
				console.print(f"[red]No data found for {ticker}[/red]")
				continue

			# This line is now very clean!
			results = [
				evaluate_metric(info, b, profile_weights) for b in benchmark_defs
			]

			display_results(
				ticker,
				info.get("longName", info.get("shortName", ticker)),
				results,
				benchmark_defs,
			)

		except Exception as e:
			console.print(f"[bold red]Error analyzing {ticker}:[/bold red] {e}")


if __name__ == "__main__":
	main()
