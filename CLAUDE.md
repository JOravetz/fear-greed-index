# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python library and Streamlit web dashboard for CNN's Fear & Greed Index. Fetches real-time market sentiment data via CNN's JSON API.

## Development Commands

```bash
# Install dependencies
uv sync

# Run web dashboard
uv run streamlit run app.py

# Run Python tests
uv run python test.py
```

## Architecture

### Core Library (`fear_greed_index/`)

- **CNNFearAndGreedIndex** (`CNNFearAndGreedIndex.py`): Main class aggregating all 7 indicators. Fetches data on instantiation. Key attributes: `score`, `rating`, `historical_data`, and individual indicator objects.

- **FearAndGreedIndicator** (`FearAndGreedIndicator.py`): Single indicator data class with `score`, `rating`, `timestamp`, and `historical_data`.

- **scrape_cnn** (`scrape_cnn.py`): API client fetching from `https://production.dataviz.cnn.io/index/fearandgreed/graphdata`.

### Web App (`app.py`)

Streamlit dashboard with Plotly charts:
- Gauge chart for current score
- Historical trend line chart
- Indicators bar chart
- 5-minute data caching

## API Data Structure

The CNN API returns:
- `fear_and_greed`: Current score, rating, and comparison values
- `fear_and_greed_historical`: 1-year historical data
- Individual indicator keys: `junk_bond_demand`, `market_volatility_vix`, `put_call_options`, `market_momentum_sp500`, `stock_price_strength`, `stock_price_breadth`, `safe_haven_demand`

## Usage

```python
from fear_greed_index import CNNFearAndGreedIndex

fgi = CNNFearAndGreedIndex()
print(fgi.score, fgi.rating)
print(fgi.market_momentum.score)
```
