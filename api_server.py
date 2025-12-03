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
