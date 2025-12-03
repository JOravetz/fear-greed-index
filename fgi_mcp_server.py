#!/usr/bin/env python3
"""MCP Server for CNN Fear & Greed Index.

This server exposes Fear & Greed Index data to AI assistants via
the Model Context Protocol (MCP).

Run with: uv run python fgi_mcp_server.py
"""

import asyncio
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from fear_greed_index import CNNFearAndGreedIndex

# Create MCP server instance
server = Server("fear-greed-index")


def get_fgi_data() -> CNNFearAndGreedIndex:
    """Fetch current Fear & Greed Index data."""
    return CNNFearAndGreedIndex()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the MCP server."""
    return [
        Tool(
            name="get_fear_greed_score",
            description="Get the current CNN Fear & Greed Index score and rating. "
                       "Returns the overall market sentiment score (0-100) and rating "
                       "(Extreme Fear, Fear, Neutral, Greed, Extreme Greed).",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_fear_greed_indicators",
            description="Get all individual Fear & Greed indicators with their scores. "
                       "Includes: Market Momentum, Stock Price Strength, Stock Price Breadth, "
                       "Put/Call Options, Market Volatility, Safe Haven Demand, Junk Bond Demand.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_fear_greed_comparison",
            description="Get Fear & Greed Index comparison with previous periods. "
                       "Shows current score vs previous close, 1 week ago, 1 month ago, and 1 year ago.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_trading_signal",
            description="Get a trading signal based on the Fear & Greed Index. "
                       "Returns STRONG BUY, BUY, HOLD, SELL, or STRONG SELL with explanation.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_fear_greed_history",
            description="Get historical Fear & Greed Index data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days of history to return (default: 10)",
                        "default": 10
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_complete_report",
            description="Get a complete Fear & Greed Index report with all data.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from MCP clients."""

    if name == "get_fear_greed_score":
        fgi = get_fgi_data()
        result = (
            f"CNN Fear & Greed Index\n"
            f"======================\n"
            f"Score: {fgi.score:.1f}/100\n"
            f"Rating: {fgi.rating}\n"
            f"Timestamp: {fgi.timestamp.strftime('%Y-%m-%d %H:%M:%S') if fgi.timestamp else 'N/A'}"
        )
        return [TextContent(type="text", text=result)]

    elif name == "get_fear_greed_indicators":
        fgi = get_fgi_data()
        lines = ["Fear & Greed Indicators", "=" * 50]
        for ind in fgi.all_indicators:
            lines.append(f"{ind.name}: {ind.score:.1f} ({ind.rating})")
        return [TextContent(type="text", text="\n".join(lines))]

    elif name == "get_fear_greed_comparison":
        fgi = get_fgi_data()
        result = (
            f"Fear & Greed Comparison\n"
            f"=======================\n"
            f"Current Score: {fgi.score:.1f}\n"
            f"Previous Close: {fgi.previous_close:.1f} (change: {fgi.score - fgi.previous_close:+.1f})\n"
            f"1 Week Ago: {fgi.previous_1_week:.1f} (change: {fgi.score - fgi.previous_1_week:+.1f})\n"
            f"1 Month Ago: {fgi.previous_1_month:.1f} (change: {fgi.score - fgi.previous_1_month:+.1f})\n"
            f"1 Year Ago: {fgi.previous_1_year:.1f} (change: {fgi.score - fgi.previous_1_year:+.1f})"
        )
        return [TextContent(type="text", text=result)]

    elif name == "get_trading_signal":
        fgi = get_fgi_data()

        if fgi.score < 20:
            signal = "STRONG BUY"
            recommendation = "Extreme fear in the market. Historically, this represents a potential buying opportunity as markets tend to be oversold."
        elif fgi.score < 40:
            signal = "BUY"
            recommendation = "Fear in the market. Consider accumulating positions as sentiment is pessimistic."
        elif fgi.score < 60:
            signal = "HOLD"
            recommendation = "Neutral sentiment. Market is balanced - maintain current positions."
        elif fgi.score < 80:
            signal = "SELL"
            recommendation = "Greed in the market. Consider taking profits as sentiment is optimistic."
        else:
            signal = "STRONG SELL"
            recommendation = "Extreme greed in the market. Historically, this represents a potential market top. Exercise caution."

        result = (
            f"Trading Signal: {signal}\n"
            f"================\n"
            f"Score: {fgi.score:.1f} ({fgi.rating})\n\n"
            f"Analysis: {recommendation}\n\n"
            f"Disclaimer: This is not financial advice. The Fear & Greed Index is one of many "
            f"indicators and should not be used as the sole basis for investment decisions."
        )
        return [TextContent(type="text", text=result)]

    elif name == "get_fear_greed_history":
        days = arguments.get("days", 10)
        fgi = get_fgi_data()
        historical = fgi.get_historical_data()[-days:]

        lines = [f"Fear & Greed History (Last {days} Days)", "=" * 40]
        for point in reversed(historical):
            date = datetime.fromtimestamp(point["x"] / 1000).strftime("%Y-%m-%d")
            lines.append(f"{date}: {point['y']:.1f} ({point['rating']})")

        return [TextContent(type="text", text="\n".join(lines))]

    elif name == "get_complete_report":
        fgi = get_fgi_data()
        return [TextContent(type="text", text=fgi.get_complete_report())]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
