from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


def get_color_for_pct(pct: float) -> str:
	if pct >= 0.9:
		return "bold green"
	if pct >= 0.7:
		return "green"
	if pct >= 0.4:
		return "yellow"
	return "red"


def display_individual_results(
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

	total_score = total_weight = 0.0

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
			f"\n[bold]FINAL SCORE:[/bold] [{color}]{total_score:.2f}/{total_weight:.1f} ({final_pct:.1f}%)[/{color}]\n"
		)
	else:
		console.print("\n[bold red]Insufficient data to calculate score.[/bold red]\n")


def display_summary_table(all_results: List[Dict[str, Any]]):
	"""
	Display a summary table of all analyzed assets.
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
