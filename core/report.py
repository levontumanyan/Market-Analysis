import csv
import io
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


def display_summary_table(all_results: List[Dict[str, Any]]):
	"""
	Display a summary table of all analyzed assets.
	all_results should contain {symbol, name, total_score, status_summary, etc.}
	"""
	table = Table(title="Analysis Summary")
	table.add_column("Symbol", style="cyan")
	table.add_column("Name", style="white")
	table.add_column("Score", justify="right", style="green")
	table.add_column("Verdict", style="bold")

	# Sort by score descending
	sorted_results = sorted(all_results, key=lambda x: x["score"], reverse=True)

	for res in sorted_results:
		score = res["score"]
		verdict = (
			"Strong Buy"
			if score > 80
			else "Buy"
			if score > 65
			else "Hold"
			if score > 40
			else "Avoid"
		)
		color = "green" if score > 65 else "yellow" if score > 40 else "red"

		table.add_row(
			res["symbol"],
			res["name"][:30],
			f"[{color}]{score:.1f}%[/{color}]",
			f"[{color}]{verdict}[/{color}]",
		)

	console.print(table)


def export_to_csv(all_results: List[Dict[str, Any]], output_path: str):
	"""Export full results to a CSV file in horizontal format."""
	if not all_results:
		return

	# 1. Determine all unique benchmark names across all results
	benchmark_names = []
	for res in all_results:
		for metric in res.get("results", []):
			name = metric["name"]
			if name not in benchmark_names:
				benchmark_names.append(name)

	# 2. Build Headers
	headers = ["Symbol", "Name", "Asset Type", "Total Score (%)"]
	for name in benchmark_names:
		headers.append(f"{name} (Value)")
		headers.append(f"{name} (Strength %)")

	try:
		with open(output_path, "w", newline="") as f:
			writer = csv.DictWriter(f, fieldnames=headers)
			writer.writeheader()

			for res in all_results:
				row = {
					"Symbol": res["symbol"],
					"Name": res["name"],
					"Asset Type": str(res["asset_type"].value),
					"Total Score (%)": f"{res['score']:.2f}",
				}

				metric_map = {m["name"]: m for m in res.get("results", [])}
				for name in benchmark_names:
					metric_data = metric_map.get(name)
					if metric_data:
						row[f"{name} (Value)"] = metric_data["value"]
						row[f"{name} (Strength %)"] = metric_data["status"].replace(
							"%", ""
						)
					else:
						row[f"{name} (Value)"] = "N/A"
						row[f"{name} (Strength %)"] = "N/A"

				writer.writerow(row)

		console.print(f"[bold green]Results exported to {output_path}[/bold green]")
	except Exception as e:
		console.print(f"[bold red]Failed to export CSV: {e}[/bold red]")


def export_to_txt(all_results: List[Dict[str, Any]], output_path: str):
	"""Export results to a plain text file mirroring terminal output."""
	if not all_results:
		return

	# Use a separate console to capture text output
	capture_console = Console(file=io.StringIO(), force_terminal=False, width=100)

	sorted_results = sorted(all_results, key=lambda x: x["score"], reverse=True)

	for i, res in enumerate(sorted_results):
		# Add a separator between tickers, but not before the first one
		if i > 0:
			capture_console.print("\n")

		capture_console.print(f"{'=' * 50}")
		capture_console.print(f"Analysis for {res['name']} ({res['symbol']})")
		capture_console.print(f"{'=' * 50}")

		table = Table(show_header=True, header_style="bold")
		table.add_column("Metric", style="dim")
		table.add_column("Value", justify="right")
		table.add_column("Strength", justify="right")
		table.add_column("Points", justify="right")

		for m in res["results"]:
			table.add_row(
				m["name"],
				str(m["value"]),
				m["status"],
				f"{m['score']:.2f}/{m['weight']:.1f}",
			)

		capture_console.print(table)
		capture_console.print(f"FINAL SCORE: {res['score']:.2f}%")

	try:
		with open(output_path, "w") as f:
			f.write(capture_console.file.getvalue())
		console.print(f"[bold green]Results exported to {output_path}[/bold green]")
	except Exception as e:
		console.print(f"[bold red]Failed to export TXT: {e}[/bold red]")
