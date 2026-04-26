import argparse
import os
import sys

from rich.console import Console

from core.analysis.indices import get_index_components
from core.io.parsers import parse_ticker_file
from core.orchestrator import run_bulk_analysis
from core.reporting.csv_reporter import CSVReporter
from core.reporting.txt_reporter import TXTReporter
from core.ui.terminal import display_individual_results, display_summary_table

console = Console()


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
		"-e",
		"--export",
		help="Export results to a CSV or TXT file (e.g., report.csv or report.txt)",
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
	is_bulk = len(tickers) > 1
	console.print(
		f"[bold green]Analyzing {len(tickers)} asset(s) with [cyan]{args.profile.upper()}[/cyan] profile[/bold green]"
	)

	def progress_callback(res):
		if not is_bulk:
			display_individual_results(
				res["symbol"],
				res["name"],
				res["results"],
				res["benchmark_defs"],
				res.get("sector"),
				res.get("industry"),
			)

	all_analysis_results = run_bulk_analysis(
		tickers, args.profile, args.benchmarks, progress_callback
	)

	# 3. Bulk Summary & Export
	if is_bulk and all_analysis_results:
		display_summary_table(all_analysis_results)

	if args.export and all_analysis_results:
		# Ensure reports directory exists
		reports_dir = "reports"
		if not os.path.exists(reports_dir):
			os.makedirs(reports_dir)

		export_path = os.path.join(reports_dir, args.export)
		ext = os.path.splitext(args.export)[1].lower()

		if ext == ".csv":
			reporter = CSVReporter()
		elif ext == ".txt":
			reporter = TXTReporter()
		else:
			# Default to CSV if extension is unrecognized
			reporter = CSVReporter()

		reporter.export(all_analysis_results, export_path)


if __name__ == "__main__":
	main()
