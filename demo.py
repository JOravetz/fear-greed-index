#!/usr/bin/env python3
"""Fear & Greed Index Demo - Showcase all features."""

import subprocess
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def run_command(cmd: list[str], description: str) -> None:
    """Run a command and display its output."""
    console.print(f"\n[bold cyan]{description}[/bold cyan]")
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]\n")
    time.sleep(0.5)
    subprocess.run(cmd)
    console.print()


def wait_for_enter(message: str = "Press Enter to continue...") -> None:
    """Wait for user to press Enter."""
    console.print(f"\n[yellow]{message}[/yellow]")
    input()


def main():
    console.clear()

    # Welcome banner
    banner = Text()
    banner.append("\n")
    banner.append("CNN FEAR & GREED INDEX", style="bold cyan")
    banner.append("\n\n")
    banner.append("Feature Demonstration", style="dim")
    banner.append("\n")

    console.print(Panel(
        banner,
        box=box.DOUBLE,
        padding=(1, 4),
    ))

    console.print("\nThis demo will showcase all the features of the Fear & Greed Index library.")
    console.print("Each feature will be demonstrated with a brief pause between them.\n")

    wait_for_enter("Press Enter to start the demo...")

    # CLI Features
    console.rule("[bold cyan]CLI Features[/bold cyan]")

    # 1. Dashboard
    run_command(
        ["uv", "run", "fgi", "dashboard"],
        "1. Full Dashboard - Complete view with gauge, comparisons, and indicators"
    )
    wait_for_enter()

    # 2. Score
    run_command(
        ["uv", "run", "fgi", "score"],
        "2. Quick Score - Just the current score and rating"
    )
    wait_for_enter()

    # 3. Signal
    run_command(
        ["uv", "run", "fgi", "signal"],
        "3. Trading Signal - AI-generated trading recommendation"
    )
    wait_for_enter()

    # 4. Indicators
    run_command(
        ["uv", "run", "fgi", "indicators"],
        "4. Individual Indicators - Detailed view of all 7 market indicators"
    )
    wait_for_enter()

    # 5. History
    run_command(
        ["uv", "run", "fgi", "history", "--limit", "10"],
        "5. Historical Data - Last 10 days of Fear & Greed scores"
    )
    wait_for_enter()

    # 6. JSON Output
    run_command(
        ["uv", "run", "fgi", "json"],
        "6. JSON Output - Machine-readable format for scripting"
    )
    wait_for_enter()

    # Python API Demo
    console.rule("[bold cyan]Python API Features[/bold cyan]")
    console.print("\n[bold]7. Python API - Programmatic access to Fear & Greed data[/bold]\n")

    from fear_greed_index import CNNFearAndGreedIndex
    from rich.table import Table

    console.print("[dim]>>> from fear_greed_index import CNNFearAndGreedIndex[/dim]")
    console.print("[dim]>>> fgi = CNNFearAndGreedIndex()[/dim]\n")

    fgi = CNNFearAndGreedIndex()

    # Create summary table
    table = Table(title="Fear & Greed Index Summary", box=box.ROUNDED)
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Score", f"{fgi.score:.1f}")
    table.add_row("Rating", fgi.rating.title())
    table.add_row("Previous Close", f"{fgi.previous_close:.1f}")
    table.add_row("1 Week Ago", f"{fgi.previous_1_week:.1f}")
    table.add_row("1 Month Ago", f"{fgi.previous_1_month:.1f}")
    table.add_row("1 Year Ago", f"{fgi.previous_1_year:.1f}")
    table.add_row("Indicators", str(len(fgi.all_indicators)))
    table.add_row("Historical Days", str(len(fgi.get_historical_data())))

    console.print(table)
    wait_for_enter()

    # Web Dashboard
    console.rule("[bold cyan]Web Dashboard[/bold cyan]")
    console.print("\n[bold]8. Streamlit Web Dashboard - Interactive browser interface[/bold]\n")
    console.print("The web dashboard provides:")
    console.print("  - Real-time gauge visualization")
    console.print("  - Interactive historical charts")
    console.print("  - Indicator breakdown with Plotly charts")
    console.print("  - Auto-refresh capability\n")

    console.print("[yellow]Starting web dashboard on http://localhost:8501...[/yellow]")
    console.print("[dim]Press Ctrl+C to stop the dashboard and exit the demo.[/dim]\n")

    try:
        subprocess.run(["uv", "run", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped.[/yellow]")

    # Closing
    console.print()
    console.rule("[bold cyan]Demo Complete[/bold cyan]")
    console.print("\n[green]Thank you for trying the Fear & Greed Index library![/green]")
    console.print("\nFor more information:")
    console.print("  - README.md - Full documentation")
    console.print("  - uv run fgi --help - CLI help")
    console.print("  - uv run pytest -v - Run test suite\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted.[/yellow]")
        sys.exit(0)
