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
