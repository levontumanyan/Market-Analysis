import argparse
import os
import sys

from rich.console import Console

from core.bulk import get_index_components, parse_ticker_file
from core.data import get_stock_data, load_benchmarks
from core.display import display_results
from core.evaluation import evaluate_metric
from core.profiles import get_profile_weights
from core.report import display_summary_table, export_to_csv
from core.schema import AssetType

console = Console()


def analyze_asset(symbol: str, profile: str, benchmark_path: str | None = None):
	"""Analyze a single asset and return the results and score."""
	asset = get_stock_data(symbol)
	if not asset:
		return None

	# Determine benchmark file based on asset type if not explicitly provided
	if not benchmark_path:
		if asset.asset_type == AssetType.ETF:
			benchmark_path = "benchmarks_etf.json"
		else:
			benchmark_path = "benchmarks_stock.json"

	benchmark_defs = load_benchmarks(benchmark_path)
	if not benchmark_defs:
		return None

	profile_weights = get_profile_weights(profile)
	results = [evaluate_metric(asset, b, profile_weights) for b in benchmark_defs]

	# Calculate total score
	total_score = 0.0
	max_score = 0.0
	for res in results:
		total_score += res["score"]
		max_score += res["weight"]

	final_pct = (total_score / max_score * 100) if max_score > 0 else 0.0

	return {
		"symbol": asset.symbol,
		"name": asset.display_name,
		"results": results,
		"benchmark_defs": benchmark_defs,
		"score": final_pct,
		"asset_type": asset.asset_type,
	}


def main():
	parser = argparse.ArgumentParser(description="Stock & ETF Fundamental Analyzer")
	parser.add_argument("tickers", nargs="*", help="One or more ticker symbols")
	parser.add_argument("-f", "--file", help="Path to a file containing tickers")
	parser.add_argument(
		"-i", "--index", help="Ticker of an index/ETF to analyze its components"
	)
	parser.add_argument("-b", "--benchmarks", help="Override path to benchmarks file")
	parser.add_argument(
		"-p",
		"--profile",
		default="balanced",
		choices=["balanced", "growth", "dividend"],
		help="Investment profile to use",
	)
	parser.add_argument(
		"-e", "--export", help="Export results to a CSV file (e.g., report.csv)"
	)
	args = parser.parse_args()

	# 1. Collect Tickers
	tickers = list(args.tickers)
	if args.file:
		tickers.extend(parse_ticker_file(args.file))
	if args.index:
		tickers.extend(get_index_components(args.index))

	if not tickers:
		console.print("[bold red]Error: No tickers provided.[/bold red]")
		parser.print_help()
		sys.exit(1)

	# 2. Process Tickers
	all_analysis_results = []
	is_bulk = len(tickers) > 1

	console.print(
		f"[bold green]Analyzing {len(tickers)} asset(s) with [cyan]{args.profile.upper()}[/cyan] profile[/bold green]"
	)

	for ticker in tickers:
		ticker = ticker.upper().strip()
		if not is_bulk:
			console.print(f"\n[bold green]Analyzing {ticker}...[/bold green]")

		try:
			res = analyze_asset(ticker, args.profile, args.benchmarks)
			if res:
				all_analysis_results.append(res)
				if not is_bulk:
					display_results(
						res["symbol"],
						res["name"],
						res["results"],
						res["benchmark_defs"],
					)
			else:
				console.print(f"[red]Failed to analyze {ticker}[/red]")
		except Exception as e:
			console.print(f"[bold red]Error analyzing {ticker}:[/bold red] {e}")

	# 3. Bulk Summary & Export
	if is_bulk and all_analysis_results:
		display_summary_table(all_analysis_results)

	if args.export and all_analysis_results:
		# Ensure reports directory exists
		reports_dir = "reports"
		if not os.path.exists(reports_dir):
			os.makedirs(reports_dir)

		export_path = os.path.join(reports_dir, args.export)
		export_to_csv(all_analysis_results, export_path)


if __name__ == "__main__":
	main()
