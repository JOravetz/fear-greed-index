"""Fear and Greed Indicator Class"""
__docformat__ = "numpy"

from datetime import datetime
from typing import Optional


class FearAndGreedIndicator:
    """Fear and Greed Indicator

    Attributes
    ----------
    name : str
        Indicator name (e.g., "Market Momentum", "Stock Price Strength")
    score : float
        Numeric score (0-100)
    rating : str
        Sentiment rating (e.g., "extreme fear", "fear", "neutral", "greed", "extreme greed")
    timestamp : datetime
        When the indicator was last updated
    historical_data : list
        Historical data points with x (timestamp), y (value), and rating
    """

    def __init__(self, name: str, data: Optional[dict] = None):
        """Constructor

        Parameters
        ----------
        name : str
            Indicator name
        data : dict, optional
            API response data for this indicator
        """
        self.name = name
        self.score = 0.0
        self.rating = "N/A"
        self.timestamp = None
        self.historical_data = []

        if data:
            self._load_from_data(data)

    def _load_from_data(self, data: dict):
        """Load indicator data from API response"""
        self.score = data.get("score", 0.0)
        self.rating = data.get("rating", "N/A")

        timestamp_ms = data.get("timestamp")
        if timestamp_ms:
            self.timestamp = datetime.fromtimestamp(timestamp_ms / 1000)

        self.historical_data = data.get("data", [])

    def get_score(self) -> float:
        """Get indicator score"""
        return self.score

    def get_rating(self) -> str:
        """Get indicator rating"""
        return self.rating

    def get_name(self) -> str:
        """Get indicator name"""
        return self.name

    def get_timestamp(self) -> Optional[datetime]:
        """Get indicator timestamp"""
        return self.timestamp

    def get_historical_data(self) -> list:
        """Get historical data"""
        return self.historical_data

    def get_report(self) -> str:
        """Get indicator report"""
        timestamp_str = self.timestamp.strftime("%b %d at %I:%M%p") if self.timestamp else "N/A"
        report = f"{self.name}: {self.rating.title()} ({self.score:.1f})"
        report += f"{(80-len(report))*' '}[Updated {timestamp_str}]"
        return report
