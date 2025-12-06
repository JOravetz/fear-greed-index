# CNN Fear & Greed Index

A Python library and web dashboard for fetching and visualizing CNN's Fear & Greed Index, a popular indicator of market sentiment.

## Features

- **Real-time data** from CNN's Fear & Greed Index API
- **7 market indicators**: Junk Bond Demand, Market Volatility (VIX), Put/Call Options, Market Momentum (S&P 500), Stock Price Strength, Stock Price Breadth, Safe Haven Demand
- **Historical data** with 1-year trend analysis
- **Interactive web dashboard** built with Streamlit and Plotly
- **Beautiful CLI** with Rich terminal interface
- **MCP Server** for AI assistant integration (Claude, Cursor, VS Code)
- **Alpaca Trading integration** for automated trading workflows
- **Python API** for programmatic access

## Installation

### Using UV (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Quick Commands

After installing with UV, these are the most useful commands:

```bash
uv run fgi --help      # CLI help - see all available commands
uv run pytest -v       # Run the test suite
```

## Quick Start

### Python API

```python
from fear_greed_index import CNNFearAndGreedIndex

# Fetch current data
fgi = CNNFearAndGreedIndex()

# Get overall index
print(f"Score: {fgi.score}")        # e.g., 24.4
print(f"Rating: {fgi.rating}")      # e.g., "extreme fear"

# Get complete report
print(fgi.get_complete_report())
```

### Web Dashboard

Launch the interactive dashboard:

```bash
uv run streamlit run app.py --server.headless=true
```

Then open http://localhost:8501 in your browser.

### Command Line Interface (CLI)

Beautiful terminal interface powered by Rich:

```bash
# Full dashboard with gauge and tables
uv run fgi dashboard

# Just the current score
uv run fgi score

# Trading signal (STRONG BUY/BUY/HOLD/SELL/STRONG SELL)
uv run fgi signal

# All indicators in detail
uv run fgi indicators

# Historical data (last 10 days by default)
uv run fgi history --limit 20

# JSON output for scripting
uv run fgi json

# Live watch mode (refreshes every 60 seconds)
uv run fgi watch
```

### Interactive Demo

Run the interactive demo to see all features in action:

```bash
uv run fgi-demo
```

The demo walks you through:
1. CLI dashboard with gauge visualization
2. Quick score and trading signal
3. Individual indicators breakdown
4. Historical data display
5. JSON output format
6. Python API usage
7. Streamlit web dashboard

## Usage Examples

### Example 1: Basic Market Sentiment Check

```python
from fear_greed_index import CNNFearAndGreedIndex

fgi = CNNFearAndGreedIndex()

print(f"Current Fear & Greed Index: {fgi.score:.1f}")
print(f"Market Sentiment: {fgi.rating.upper()}")
print(f"Previous Close: {fgi.previous_close:.1f}")
print(f"Change: {fgi.score - fgi.previous_close:+.1f}")
```

### Example 2: Compare Current vs Historical Sentiment

```python
from fear_greed_index import CNNFearAndGreedIndex

fgi = CNNFearAndGreedIndex()

print("Fear & Greed Index Comparison")
print("=" * 40)
print(f"Now:          {fgi.score:.1f} ({fgi.rating})")
print(f"Yesterday:    {fgi.previous_close:.1f}")
print(f"1 Week Ago:   {fgi.previous_1_week:.1f}")
print(f"1 Month Ago:  {fgi.previous_1_month:.1f}")
print(f"1 Year Ago:   {fgi.previous_1_year:.1f}")
```

### Example 3: Analyze Individual Indicators

```python
from fear_greed_index import CNNFearAndGreedIndex

fgi = CNNFearAndGreedIndex()

print("Individual Market Indicators")
print("=" * 50)
for indicator in fgi.all_indicators:
    status = "🔴" if indicator.score < 25 else "🟡" if indicator.score < 50 else "🟢"
    print(f"{status} {indicator.name}: {indicator.score:.1f} ({indicator.rating})")
```

### Example 4: Trading Signal Based on Sentiment

```python
from fear_greed_index import CNNFearAndGreedIndex

fgi = CNNFearAndGreedIndex()

def get_trading_signal(score: float) -> str:
    """Generate trading signal based on Fear & Greed score."""
    if score < 20:
        return "STRONG BUY - Extreme fear, potential opportunity"
    elif score < 40:
        return "BUY - Fear in the market"
    elif score < 60:
        return "HOLD - Neutral sentiment"
    elif score < 80:
        return "SELL - Greed in the market"
    else:
        return "STRONG SELL - Extreme greed, potential top"

signal = get_trading_signal(fgi.score)
print(f"Score: {fgi.score:.1f}")
print(f"Signal: {signal}")
```

### Example 5: Historical Data Analysis with Pandas

```python
from fear_greed_index import CNNFearAndGreedIndex
from datetime import datetime
import pandas as pd

fgi = CNNFearAndGreedIndex()

# Convert historical data to DataFrame
historical = fgi.get_historical_data()
df = pd.DataFrame(historical)
df['date'] = pd.to_datetime(df['x'], unit='ms')
df = df.rename(columns={'y': 'score'})
df = df[['date', 'score', 'rating']]

# Analysis
print(f"Data points: {len(df)}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Average score: {df['score'].mean():.1f}")
print(f"Min score: {df['score'].min():.1f}")
print(f"Max score: {df['score'].max():.1f}")

# Count days in each sentiment zone
print("\nSentiment Distribution:")
print(df['rating'].value_counts())
```

### Example 6: Detect Sentiment Extremes

```python
from fear_greed_index import CNNFearAndGreedIndex
from datetime import datetime

fgi = CNNFearAndGreedIndex()

historical = fgi.get_historical_data()

# Find extreme fear days (score < 20)
extreme_fear_days = [
    (datetime.fromtimestamp(d['x']/1000).strftime('%Y-%m-%d'), d['y'])
    for d in historical if d['y'] < 20
]

print(f"Extreme Fear Days (score < 20) in past year: {len(extreme_fear_days)}")
for date, score in extreme_fear_days[-5:]:  # Show last 5
    print(f"  {date}: {score:.1f}")
```

### Example 7: VIX-Specific Analysis

```python
from fear_greed_index import CNNFearAndGreedIndex

fgi = CNNFearAndGreedIndex()

vix = fgi.market_volatility
print(f"VIX Indicator Score: {vix.score:.1f}")
print(f"VIX Sentiment: {vix.rating}")
print(f"Last Updated: {vix.timestamp.strftime('%Y-%m-%d %H:%M')}")

# VIX is often inverse to market - high VIX = fear
if vix.score < 30:
    print("⚠️  High volatility expected - VIX indicating fear")
elif vix.score > 70:
    print("✅ Low volatility - VIX indicating complacency")
```

### Example 8: Export Data to JSON

```python
from fear_greed_index import CNNFearAndGreedIndex
import json

fgi = CNNFearAndGreedIndex()

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

print(json.dumps(data, indent=2))

# Save to file
with open("fear_greed_data.json", "w") as f:
    json.dump(data, f, indent=2)
```

### Example 9: Build a FastAPI Service

Create your own REST API to serve Fear & Greed data to other applications:

```python
# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fear_greed_index import CNNFearAndGreedIndex

app = FastAPI(
    title="Fear & Greed Index API",
    description="REST API for CNN Fear & Greed Index data",
    version="1.0.0"
)

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Response models
class IndicatorResponse(BaseModel):
    name: str
    score: float
    rating: str
    timestamp: Optional[datetime]

class FearGreedResponse(BaseModel):
    score: float
    rating: str
    previous_close: float
    previous_1_week: float
    previous_1_month: float
    previous_1_year: float
    timestamp: Optional[datetime]
    indicators: list[IndicatorResponse]

class TradingSignalResponse(BaseModel):
    score: float
    rating: str
    signal: str
    recommendation: str

# Cache the data (refresh every 5 minutes in production)
_cache = {"data": None, "timestamp": None}

def get_fgi():
    """Get Fear & Greed data with simple caching."""
    now = datetime.now()
    if (_cache["data"] is None or
        _cache["timestamp"] is None or
        (now - _cache["timestamp"]).total_seconds() > 300):
        _cache["data"] = CNNFearAndGreedIndex()
        _cache["timestamp"] = now
    return _cache["data"]

@app.get("/", response_model=FearGreedResponse)
async def get_fear_greed():
    """Get current Fear & Greed Index with all indicators."""
    fgi = get_fgi()
    return FearGreedResponse(
        score=fgi.score,
        rating=fgi.rating,
        previous_close=fgi.previous_close,
        previous_1_week=fgi.previous_1_week,
        previous_1_month=fgi.previous_1_month,
        previous_1_year=fgi.previous_1_year,
        timestamp=fgi.timestamp,
        indicators=[
            IndicatorResponse(
                name=ind.name,
                score=ind.score,
                rating=ind.rating,
                timestamp=ind.timestamp
            )
            for ind in fgi.all_indicators
        ]
    )

@app.get("/score")
async def get_score():
    """Get just the current score and rating."""
    fgi = get_fgi()
    return {"score": fgi.score, "rating": fgi.rating}

@app.get("/signal", response_model=TradingSignalResponse)
async def get_trading_signal():
    """Get a trading signal based on current sentiment."""
    fgi = get_fgi()

    if fgi.score < 20:
        signal, recommendation = "STRONG_BUY", "Extreme fear - potential buying opportunity"
    elif fgi.score < 40:
        signal, recommendation = "BUY", "Fear in market - consider accumulating"
    elif fgi.score < 60:
        signal, recommendation = "HOLD", "Neutral sentiment - maintain positions"
    elif fgi.score < 80:
        signal, recommendation = "SELL", "Greed in market - consider taking profits"
    else:
        signal, recommendation = "STRONG_SELL", "Extreme greed - potential market top"

    return TradingSignalResponse(
        score=fgi.score,
        rating=fgi.rating,
        signal=signal,
        recommendation=recommendation
    )

@app.get("/indicator/{name}")
async def get_indicator(name: str):
    """Get a specific indicator by name."""
    fgi = get_fgi()
    name_lower = name.lower().replace("_", " ").replace("-", " ")

    for ind in fgi.all_indicators:
        if name_lower in ind.name.lower():
            return {
                "name": ind.name,
                "score": ind.score,
                "rating": ind.rating,
                "timestamp": ind.timestamp
            }

    return {"error": f"Indicator '{name}' not found"}

@app.get("/historical")
async def get_historical(limit: int = 30):
    """Get historical data (default last 30 days)."""
    fgi = get_fgi()
    historical = fgi.get_historical_data()[-limit:]
    return [
        {
            "date": datetime.fromtimestamp(d["x"] / 1000).isoformat(),
            "score": d["y"],
            "rating": d["rating"]
        }
        for d in historical
    ]
```

Run the FastAPI server:

```bash
# Install FastAPI if needed
uv add fastapi uvicorn

# Run the server
uv run uvicorn api_server:app --reload --port 8000
```

Then access your API:

```bash
# Get current Fear & Greed data
curl http://localhost:8000/

# Get just the score
curl http://localhost:8000/score

# Get trading signal
curl http://localhost:8000/signal

# Get specific indicator
curl http://localhost:8000/indicator/vix

# Get last 7 days of history
curl http://localhost:8000/historical?limit=7
```

Example response from `/signal`:

```json
{
  "score": 24.4,
  "rating": "extreme fear",
  "signal": "STRONG_BUY",
  "recommendation": "Extreme fear - potential buying opportunity"
}
```

## API Reference

### CNNFearAndGreedIndex

Main class for accessing Fear & Greed data.

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `score` | float | Current index score (0-100) |
| `rating` | str | Current sentiment rating |
| `previous_close` | float | Previous trading day's score |
| `previous_1_week` | float | Score from 1 week ago |
| `previous_1_month` | float | Score from 1 month ago |
| `previous_1_year` | float | Score from 1 year ago |
| `timestamp` | datetime | Last update time |
| `historical_data` | list | Historical data points (1 year) |

**Indicator Attributes:**
| Attribute | Description |
|-----------|-------------|
| `junk_bond_demand` | Junk Bond Demand indicator |
| `market_volatility` | Market Volatility (VIX) indicator |
| `put_call_options` | Put and Call Options indicator |
| `market_momentum` | Market Momentum (S&P 500) indicator |
| `stock_price_strength` | Stock Price Strength indicator |
| `stock_price_breadth` | Stock Price Breadth indicator |
| `safe_haven_demand` | Safe Haven Demand indicator |
| `all_indicators` | List of all indicator objects |

**Methods:**
| Method | Returns | Description |
|--------|---------|-------------|
| `get_score()` | float | Current index score |
| `get_rating()` | str | Current sentiment rating |
| `get_index_summary()` | str | Formatted summary string |
| `get_indicators_report()` | str | All indicators report |
| `get_complete_report()` | str | Full report with all data |
| `get_historical_data()` | list | Historical data points |
| `plot_fear_greed_index(ax)` | Axes | Plot historical chart |
| `plot_all_indicators(fig)` | Figure | Plot indicators bar chart |
| `plot_all_charts(fig)` | Figure | Plot complete dashboard |

### FearAndGreedIndicator

Individual indicator class.

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Indicator name |
| `score` | float | Indicator score (0-100) |
| `rating` | str | Indicator sentiment |
| `timestamp` | datetime | Last update time |
| `historical_data` | list | Historical data for this indicator |

**Methods:**
| Method | Returns | Description |
|--------|---------|-------------|
| `get_score()` | float | Indicator score |
| `get_rating()` | str | Indicator rating |
| `get_name()` | str | Indicator name |
| `get_report()` | str | Formatted report string |

## Understanding the Index

| Score Range | Rating | Market Sentiment |
|-------------|--------|------------------|
| 0-25 | Extreme Fear | Investors are very worried |
| 25-45 | Fear | Investors are worried |
| 45-55 | Neutral | Market is balanced |
| 55-75 | Greed | Investors are confident |
| 75-100 | Extreme Greed | Investors are very confident |

### The 7 Indicators Explained

1. **Junk Bond Demand**: Spread between junk bond yields and investment-grade bonds
2. **Market Volatility (VIX)**: CBOE Volatility Index measuring expected S&P 500 volatility
3. **Put/Call Options**: Ratio of put option volume to call option volume
4. **Market Momentum**: S&P 500 vs its 125-day moving average
5. **Stock Price Strength**: Number of stocks hitting 52-week highs vs lows
6. **Stock Price Breadth**: McClellan Volume Summation Index
7. **Safe Haven Demand**: Stock vs bond returns over 20 trading days

### Trading Implications

- **Extreme Fear** often signals potential buying opportunities (contrarian indicator)
- **Extreme Greed** may indicate market tops or overvaluation
- Use alongside other technical and fundamental analysis

## Data Source

### CNN Fear & Greed Index

- **Website**: https://www.cnn.com/markets/fear-and-greed
- **API Endpoint**: `https://production.dataviz.cnn.io/index/fearandgreed/graphdata`

> **Note**: The API endpoint is CNN's internal API used by their website. It is not officially documented and may change without notice. This library abstracts the API details so your code remains stable.

### API Response Structure

The CNN API returns JSON with the following structure:

```json
{
  "fear_and_greed": {
    "score": 24.37,
    "rating": "extreme fear",
    "timestamp": "2025-12-02T23:59:56+00:00",
    "previous_close": 23.03,
    "previous_1_week": 17.03,
    "previous_1_month": 44.63,
    "previous_1_year": 65.31
  },
  "fear_and_greed_historical": {
    "data": [{"x": 1733184000000, "y": 59.57, "rating": "greed"}, ...]
  },
  "junk_bond_demand": {"score": 0.4, "rating": "extreme fear", ...},
  "market_volatility_vix": {"score": 50.0, "rating": "neutral", ...},
  "put_call_options": {"score": 22.2, "rating": "extreme fear", ...},
  "market_momentum_sp500": {"score": 41.0, "rating": "fear", ...},
  "stock_price_strength": {"score": 11.4, "rating": "extreme fear", ...},
  "stock_price_breadth": {"score": 18.0, "rating": "extreme fear", ...},
  "safe_haven_demand": {"score": 27.6, "rating": "fear", ...}
}
```

## MCP Server (AI Integration)

This library includes an MCP (Model Context Protocol) server that allows AI assistants like Claude, Cursor, and VS Code to query Fear & Greed data using natural language.

### Quick Reference Command

Use the `/mcp-tools` slash command in Claude Code to list all available MCP tools:

```bash
/mcp-tools
```

This displays a complete reference of all Fear & Greed Index and Alpaca trading tools available through the MCP servers.

To set up the custom command, create `~/.claude/commands/mcp-tools.md` with your tool documentation.

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `get_fear_greed_score` | Get current score and rating |
| `get_fear_greed_indicators` | Get all 7 individual indicators |
| `get_fear_greed_comparison` | Compare with previous periods |
| `get_trading_signal` | Get trading signal with recommendation |
| `get_fear_greed_history` | Get historical data (configurable days) |
| `get_complete_report` | Get full comprehensive report |

### Quick Test

Verify the MCP server works before configuring your IDE:

```bash
# Test the server starts without errors
uv run python fgi_mcp_server.py

# You should see the server waiting for input (press Ctrl+C to exit)
```

### Configure for Claude Code

Create a `.mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "fear-greed-index": {
      "command": "uv",
      "args": ["run", "python", "fgi_mcp_server.py"],
      "cwd": "/path/to/fear-greed-index",
      "env": {
        "PATH": "${PATH}"
      }
    }
  }
}
```

Verify the server is loaded:

```bash
claude mcp list
```

### Configure for Claude Desktop

Add to your Claude Desktop config (`~/.config/Claude/claude_desktop_config.json` on Linux, `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "fear-greed-index": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/fear-greed-index", "python", "fgi_mcp_server.py"]
    }
  }
}
```

### Configure for Cursor / VS Code

Add to your MCP settings:

```json
{
  "mcp.servers": {
    "fear-greed-index": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/fear-greed-index", "python", "fgi_mcp_server.py"]
    }
  }
}
```

### Example AI Prompts

Once configured, you can ask your AI assistant:

- "What's the current Fear & Greed Index?"
- "Give me a trading signal based on market sentiment"
- "How has sentiment changed over the past week?"
- "Show me all the individual market indicators"

## Alpaca Trading Integration

Combine Fear & Greed sentiment data with [Alpaca's MCP Server](https://github.com/alpacahq/alpaca-mcp-server) for AI-powered trading workflows.

### Setup Both MCP Servers

**For Claude Code**, create a `.mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "fear-greed-index": {
      "command": "uv",
      "args": ["run", "python", "fgi_mcp_server.py"],
      "cwd": "/path/to/fear-greed-index",
      "env": {
        "PATH": "${PATH}"
      }
    },
    "alpaca": {
      "command": "uvx",
      "args": ["alpaca-mcp-server", "serve"],
      "env": {
        "ALPACA_API_KEY": "${APCA_API_KEY_ID}",
        "ALPACA_SECRET_KEY": "${APCA_API_SECRET_KEY}"
      }
    }
  }
}
```

**For Claude Desktop**, add to your config file:

```json
{
  "mcpServers": {
    "fear-greed-index": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/fear-greed-index", "python", "fgi_mcp_server.py"]
    },
    "alpaca": {
      "command": "uvx",
      "args": ["alpaca-mcp-server", "serve"],
      "env": {
        "ALPACA_API_KEY": "your_alpaca_api_key",
        "ALPACA_SECRET_KEY": "your_alpaca_secret_key"
      }
    }
  }
}
```

### Example Combined Workflows

With both servers configured, you can use natural language for sophisticated trading workflows:

**Sentiment-Based Trading:**
```
"Check the Fear & Greed Index. If it's in Extreme Fear territory,
buy 10 shares of SPY using my Alpaca account."
```

**Portfolio Rebalancing:**
```
"Get my current Alpaca positions and the Fear & Greed trading signal.
If the signal is STRONG SELL and I'm holding SPY, close half my position."
```

**Market Analysis:**
```
"Show me the Fear & Greed indicators and get the latest SPY quote from Alpaca.
Should I be adding to my position?"
```

### Alpaca MCP Server Features

The [Alpaca MCP Server](https://github.com/alpacahq/alpaca-mcp-server) provides:

- **Trading**: Stocks, ETFs, crypto, and options
- **Market Data**: Real-time quotes, bars, and historical data
- **Account Management**: Positions, balances, buying power
- **Order Management**: Market, limit, stop, trailing-stop orders
- **Options Trading**: Single and multi-leg strategies

### Installation

```bash
# Install Alpaca MCP Server
uvx alpaca-mcp-server init

# Or clone the repository
git clone https://github.com/alpacahq/alpaca-mcp-server.git
cd alpaca-mcp-server
python3 install.py
```

### Resources

- [Alpaca MCP Server GitHub](https://github.com/alpacahq/alpaca-mcp-server)
- [Alpaca MCP Documentation](https://docs.alpaca.markets/docs/alpaca-mcp-server)
- [Building Trading Workflows with MCP](https://alpaca.markets/learn/mcp-trading-with-claude-alpaca-google-sheets)

### Acknowledgments

Special thanks to **Satoshi Ido** for his excellent contributions to the [Alpaca Markets MCP Server](https://github.com/alpacahq/alpaca-mcp-server), which enables seamless AI-powered trading workflows.

## Testing

Run the test suite to verify all features work correctly:

```bash
# Run all tests
uv run pytest -v

# Run README examples validation (tests all code examples from documentation)
uv run pytest tests/test_readme_examples.py -v

# Run core functionality tests
uv run pytest tests/test_core.py -v

# Run CLI tests
uv run pytest tests/test_cli.py -v

# Run MCP server tests
uv run pytest tests/test_mcp_server.py -v
```

## Disclaimer

**THIS SOFTWARE IS PROVIDED FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- This library is not affiliated with, endorsed by, or connected to CNN or Warner Bros. Discovery.
- The Fear & Greed Index data is sourced from CNN's public-facing API, which may change or become unavailable at any time.
- **This is NOT financial or investment advice.** The trading signals, recommendations, and analysis examples in this documentation are for illustrative purposes only.
- Past performance and sentiment indicators do not guarantee future results.
- Always conduct your own research and consult with a qualified financial advisor before making any investment decisions.
- The authors and contributors of this software are not responsible for any financial losses, damages, or other consequences resulting from the use of this software.
- Use at your own risk.

## License

MIT License
