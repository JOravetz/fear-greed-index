# CNN Fear & Greed Index

A Python library and web dashboard for fetching and visualizing CNN's Fear & Greed Index, a popular indicator of market sentiment.

## Features

- **Real-time data** from CNN's Fear & Greed Index API
- **7 market indicators**: Junk Bond Demand, Market Volatility (VIX), Put/Call Options, Market Momentum (S&P 500), Stock Price Strength, Stock Price Breadth, Safe Haven Demand
- **Historical data** with 1-year trend analysis
- **Interactive web dashboard** built with Streamlit and Plotly
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

# Access individual indicators
print(f"VIX: {fgi.market_volatility.score} ({fgi.market_volatility.rating})")
print(f"S&P 500 Momentum: {fgi.market_momentum.score}")

# Get historical data for analysis
historical = fgi.get_historical_data()
for point in historical[-5:]:  # Last 5 data points
    print(f"{point['x']}: {point['y']:.1f} ({point['rating']})")
```

### Web Dashboard

Launch the interactive dashboard:

```bash
uv run streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## API Reference

### CNNFearAndGreedIndex

Main class for accessing Fear & Greed data.

**Attributes:**
- `score` (float): Current index score (0-100)
- `rating` (str): Current sentiment ("extreme fear", "fear", "neutral", "greed", "extreme greed")
- `previous_close` (float): Previous trading day's score
- `previous_1_week` (float): Score from 1 week ago
- `previous_1_month` (float): Score from 1 month ago
- `previous_1_year` (float): Score from 1 year ago
- `historical_data` (list): List of historical data points

**Indicator Attributes:**
- `junk_bond_demand`
- `market_volatility`
- `put_call_options`
- `market_momentum`
- `stock_price_strength`
- `stock_price_breadth`
- `safe_haven_demand`

**Methods:**
- `get_score()` - Returns current score
- `get_rating()` - Returns current rating
- `get_index_summary()` - Returns formatted summary string
- `get_indicators_report()` - Returns all indicators report
- `get_complete_report()` - Returns full report with all data
- `get_historical_data()` - Returns historical data points

### FearAndGreedIndicator

Individual indicator class.

**Attributes:**
- `name` (str): Indicator name
- `score` (float): Indicator score (0-100)
- `rating` (str): Indicator sentiment
- `timestamp` (datetime): Last update time
- `historical_data` (list): Historical data for this indicator

**Methods:**
- `get_score()` - Returns score
- `get_rating()` - Returns rating
- `get_report()` - Returns formatted report string

## Understanding the Index

| Score Range | Rating | Market Sentiment |
|-------------|--------|------------------|
| 0-25 | Extreme Fear | Investors are very worried |
| 25-45 | Fear | Investors are worried |
| 45-55 | Neutral | Market is balanced |
| 55-75 | Greed | Investors are confident |
| 75-100 | Extreme Greed | Investors are very confident |

### Trading Implications

- **Extreme Fear** often signals potential buying opportunities (contrarian indicator)
- **Extreme Greed** may indicate market tops or overvaluation
- Use alongside other technical and fundamental analysis

## Data Source

Data is fetched from CNN Business Fear & Greed Index:
https://www.cnn.com/markets/fear-and-greed

## License

MIT License
