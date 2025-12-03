#!/usr/bin/env python3
"""CNN Fear & Greed Index CLI - Beautiful terminal interface."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box
from datetime import datetime

console = Console()


def get_color_for_score(score: float) -> str:
    """Return rich color based on fear/greed score."""
    if score < 25:
        return "red"
    elif score < 45:
        return "orange1"
    elif score < 55:
        return "yellow"
    elif score < 75:
        return "green"
    else:
        return "dark_green"


def get_emoji_for_score(score: float) -> str:
    """Return emoji based on fear/greed score."""
    if score < 25:
        return "🔴"
    elif score < 45:
        return "🟠"
    elif score < 55:
        return "🟡"
    elif score < 75:
        return "🟢"
    else:
        return "💚"


def create_gauge(score: float, width: int = 56) -> Text:
    """Create a text-based gauge as a Rich Text object with labels and pointer."""
    filled = int((score / 100) * width)
    empty = width - filled
    color = get_color_for_score(score)

    # Calculate pointer position
    pointer_pos = int((score / 100) * width)
    label_offset = 7  # "FEAR 0 " length

    gauge = Text()

    # First line: pointer with score
    gauge.append(" " * (label_offset + pointer_pos))
    gauge.append(f"▼ {score:.0f}", style=f"bold {color}")
    gauge.append("\n")

    # Second line: the gauge bar with labels
    gauge.append("FEAR ", style="bold red")
    gauge.append("0 ", style="dim")
    gauge.append("█" * filled, style=color)
    gauge.append("░" * empty, style="dim")
    gauge.append(" 100", style="dim")
    gauge.append(" GREED", style="bold green")

    return gauge


def load_data():
    """Load Fear & Greed data with spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Fetching Fear & Greed data...", total=None)
        from fear_greed_index import CNNFearAndGreedIndex
        return CNNFearAndGreedIndex()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """CNN Fear & Greed Index CLI - Real-time market sentiment."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(dashboard)


@cli.command()
def dashboard():
    """Display the full Fear & Greed dashboard."""
    fgi = load_data()

    color = get_color_for_score(fgi.score)
    emoji = get_emoji_for_score(fgi.score)

    # Main score panel
    score_text = Text()
    score_text.append("\n")
    score_text.append_text(create_gauge(fgi.score))
    score_text.append("\n\n")
    score_text.append(f"  {fgi.score:.1f}", style=f"bold {color}")
    score_text.append(f"  {fgi.rating.upper()} {emoji}\n", style=f"bold {color}")

    panel = Panel(
        score_text,
        title="[bold cyan]CNN FEAR & GREED INDEX[/bold cyan]",
        subtitle=f"[dim]Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}[/dim]",
        box=box.DOUBLE,
        padding=(0, 2),
    )
    console.print(panel)

    # Comparison table
    comparison = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    comparison.add_column("Period", style="dim")
    comparison.add_column("Score", justify="right")
    comparison.add_column("Change", justify="right")

    periods = [
        ("Previous Close", fgi.previous_close),
        ("1 Week Ago", fgi.previous_1_week),
        ("1 Month Ago", fgi.previous_1_month),
        ("1 Year Ago", fgi.previous_1_year),
    ]

    for period, value in periods:
        change = fgi.score - value
        change_str = f"[green]+{change:.1f}[/green]" if change > 0 else f"[red]{change:.1f}[/red]"
        comparison.add_row(period, f"{value:.1f}", change_str)

    console.print(comparison)
    console.print()

    # Indicators table
    indicators = Table(
        title="[bold]Individual Indicators[/bold]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    indicators.add_column("Indicator", style="bold")
    indicators.add_column("Score", justify="right")
    indicators.add_column("Rating", justify="center")
    indicators.add_column("", justify="center", width=3)

    for ind in fgi.all_indicators:
        ind_color = get_color_for_score(ind.score)
        ind_emoji = get_emoji_for_score(ind.score)
        indicators.add_row(
            ind.name,
            f"[{ind_color}]{ind.score:.1f}[/{ind_color}]",
            f"[{ind_color}]{ind.rating.title()}[/{ind_color}]",
            ind_emoji
        )

    console.print(indicators)


@cli.command()
def score():
    """Display just the current score."""
    fgi = load_data()
    color = get_color_for_score(fgi.score)
    emoji = get_emoji_for_score(fgi.score)
    console.print(f"{emoji} [{color}]{fgi.score:.1f}[/{color}] - [{color}]{fgi.rating.upper()}[/{color}]")


@cli.command()
def signal():
    """Display trading signal based on sentiment."""
    fgi = load_data()

    if fgi.score < 20:
        signal = "STRONG BUY"
        recommendation = "Extreme fear - potential buying opportunity"
        color = "green"
        emoji = "🚀"
    elif fgi.score < 40:
        signal = "BUY"
        recommendation = "Fear in market - consider accumulating"
        color = "green"
        emoji = "📈"
    elif fgi.score < 60:
        signal = "HOLD"
        recommendation = "Neutral sentiment - maintain positions"
        color = "yellow"
        emoji = "⏸️"
    elif fgi.score < 80:
        signal = "SELL"
        recommendation = "Greed in market - consider taking profits"
        color = "orange1"
        emoji = "📉"
    else:
        signal = "STRONG SELL"
        recommendation = "Extreme greed - potential market top"
        color = "red"
        emoji = "🛑"

    panel = Panel(
        f"\n{emoji} [{color} bold]{signal}[/{color} bold]\n\n[dim]{recommendation}[/dim]\n\nScore: {fgi.score:.1f} ({fgi.rating})\n",
        title="[bold cyan]TRADING SIGNAL[/bold cyan]",
        box=box.DOUBLE,
    )
    console.print(panel)


@cli.command()
def indicators():
    """Display all indicators in detail."""
    fgi = load_data()

    for ind in fgi.all_indicators:
        color = get_color_for_score(ind.score)
        emoji = get_emoji_for_score(ind.score)
        timestamp = ind.timestamp.strftime("%Y-%m-%d %H:%M") if ind.timestamp else "N/A"

        content = Text()
        content.append("\n")
        content.append_text(create_gauge(ind.score))
        content.append("\n\n")
        content.append("Score: ")
        content.append(f"{ind.score:.1f}", style=color)
        content.append("  Rating: ")
        content.append(f"{ind.rating.title()}", style=color)
        content.append(f" {emoji}\n")
        content.append(f"Updated: {timestamp}\n", style="dim")

        panel = Panel(
            content,
            title=f"[bold]{ind.name}[/bold]",
            box=box.ROUNDED,
        )
        console.print(panel)


@cli.command()
@click.option("--limit", "-l", default=10, help="Number of days to show")
def history(limit):
    """Display historical data."""
    fgi = load_data()

    table = Table(
        title=f"[bold]Historical Data (Last {limit} Days)[/bold]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("Date", style="dim")
    table.add_column("Score", justify="right")
    table.add_column("Rating", justify="center")
    table.add_column("", justify="center", width=3)

    historical = fgi.get_historical_data()[-limit:]
    for point in reversed(historical):
        date = datetime.fromtimestamp(point["x"] / 1000).strftime("%Y-%m-%d")
        score = point["y"]
        rating = point["rating"]
        color = get_color_for_score(score)
        emoji = get_emoji_for_score(score)

        table.add_row(
            date,
            f"[{color}]{score:.1f}[/{color}]",
            f"[{color}]{rating.title()}[/{color}]",
            emoji
        )

    console.print(table)


@cli.command()
def json():
    """Output data as JSON."""
    import json as json_lib
    fgi = load_data()

    data = {
        "timestamp": fgi.timestamp.isoformat() if fgi.timestamp else None,
        "score": fgi.score,
        "rating": fgi.rating,
        "previous_close": fgi.previous_close,
        "previous_1_week": fgi.previous_1_week,
        "previous_1_month": fgi.previous_1_month,
        "previous_1_year": fgi.previous_1_year,
        "indicators": {
            ind.name: {"score": ind.score, "rating": ind.rating}
            for ind in fgi.all_indicators
        }
    }

    from rich.syntax import Syntax
    syntax = Syntax(json_lib.dumps(data, indent=2), "json", theme="monokai")
    console.print(syntax)


@cli.command()
def watch():
    """Watch mode - refresh every 60 seconds."""
    from time import sleep

    console.print("[bold cyan]Watch mode[/bold cyan] - Press Ctrl+C to exit\n")

    try:
        while True:
            console.clear()
            fgi = load_data()

            color = get_color_for_score(fgi.score)
            emoji = get_emoji_for_score(fgi.score)

            content = Text()
            content.append("\n")
            content.append_text(create_gauge(fgi.score))
            content.append("\n\n")
            content.append(f"  {fgi.score:.1f}", style=f"bold {color}")
            content.append(f"  {fgi.rating.upper()} {emoji}\n", style=color)

            console.print(Panel(
                content,
                title="[bold cyan]CNN FEAR & GREED INDEX[/bold cyan]",
                subtitle=f"[dim]Refreshing every 60s | {datetime.now().strftime('%H:%M:%S')}[/dim]",
                box=box.DOUBLE,
            ))

            # Quick indicators summary
            for ind in fgi.all_indicators:
                ind_emoji = get_emoji_for_score(ind.score)
                ind_color = get_color_for_score(ind.score)
                console.print(f"  {ind_emoji} [{ind_color}]{ind.score:5.1f}[/{ind_color}] {ind.name}")

            console.print("\n[dim]Press Ctrl+C to exit[/dim]")
            sleep(60)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching.[/yellow]")


def main():
    cli()


if __name__ == "__main__":
    main()
