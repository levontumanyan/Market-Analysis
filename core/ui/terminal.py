from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table

from core.stats import SessionStats

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
	sector: Optional[str] = None,
	industry: Optional[str] = None,
):
	title = f"Analysis for {company_name} ({ticker_symbol})"
	if sector:
		title += f"\n[dim]{sector} | {industry}[/dim]"

	table = Table(title=title)
	table.add_column("Metric", style="cyan")
	table.add_column("Value", justify="right")
	table.add_column("Strength", justify="center")
	table.add_column("Points", justify="right")

	# Combine data for sorting
	display_data = []
	for res, b_def in zip(results, benchmark_defs):
		# Clarify specific metric names for readability
		friendly_name = b_def["name"]
		if friendly_name == "Current Ratio":
			friendly_name = "Current Ratio (Liquidity)"
		elif friendly_name == "Trailing P/E Ratio":
			friendly_name = "Trailing P/E (Past 12m)"
		elif friendly_name == "Forward P/E Ratio":
			friendly_name = "Forward P/E (Next 12m)"

		display_data.append(
			{
				"name": friendly_name,
				"value": res["value"],
				"status": res["status"],
				"score": res["score"],
				"weight": res["weight"],
				"pct": res["pct"],
			}
		)

	# Sort by weight descending (importance)
	display_data.sort(key=lambda x: x["weight"], reverse=True)

	total_score = total_weight = 0.0

	for item in display_data:
		if item["weight"] == 0:
			status_style = "dim"
			points_str = "N/A"
		else:
			status_style = get_color_for_pct(item["pct"])
			points_str = f"{item['score']:.2f}/{item['weight']:.1f}"

		table.add_row(
			item["name"],
			item["value"],
			f"[{status_style}]{item['status']}[/{status_style}]",
			points_str,
		)
		total_score += item["score"]
		total_weight += item["weight"]

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


def display_run_summary(stats: SessionStats):
	"""Display a summary of the execution run (timers, cache hits, etc)."""
	table = Table(title="Execution Run Summary", show_header=False, box=None)
	table.add_column("Metric", style="dim")
	table.add_column("Value", style="bold")

	# Duration metrics
	table.add_row("Total Duration", f"{stats.get_total_time():.2f}s")
	for stage, duration in stats.stage_times.items():
		table.add_row(f"  └─ {stage}", f"{duration:.2f}s")

	# Cache metrics
	total_requests = stats.cache_hits + stats.api_calls
	cache_rate = (stats.cache_hits / total_requests * 100) if total_requests > 0 else 0
	table.add_row("Cache Hits", f"{stats.cache_hits} ({cache_rate:.1f}%)")
	table.add_row("API Calls", str(stats.api_calls))

	if stats.errors > 0:
		table.add_row("Errors", f"[bold red]{stats.errors}[/bold red]")

	console.print("\n")
	console.print(table)
