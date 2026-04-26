import csv
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
	"""Export full results to a CSV file."""
	if not all_results:
		return

	# Extract all unique metric keys for headers
	headers = ["Symbol", "Name", "Total Score"]

	try:
		with open(output_path, "w", newline="") as f:
			writer = csv.DictWriter(f, fieldnames=headers)
			writer.writeheader()
			for res in all_results:
				writer.writerow(
					{
						"Symbol": res["symbol"],
						"Name": res["name"],
						"Total Score": f"{res['score']:.2f}%",
					}
				)
		console.print(f"[bold green]Results exported to {output_path}[/bold green]")
	except Exception as e:
		console.print(f"[bold red]Failed to export CSV: {e}[/bold red]")
