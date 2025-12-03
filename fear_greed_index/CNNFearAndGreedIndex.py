"""Fear and Greed Index Class"""
__docformat__ = "numpy"

from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from fear_greed_index import scrape_cnn
from fear_greed_index.FearAndGreedIndicator import FearAndGreedIndicator


class CNNFearAndGreedIndex:
    """CNN Fear and Greed Index

    Attributes
    ----------
    score : float
        Current Fear and Greed Index score (0-100)
    rating : str
        Current sentiment rating
    previous_close : float
        Previous close score
    previous_1_week : float
        Score from 1 week ago
    previous_1_month : float
        Score from 1 month ago
    previous_1_year : float
        Score from 1 year ago
    timestamp : datetime
        When the index was last updated
    junk_bond_demand : FearAndGreedIndicator
        Junk Bond Demand indicator
    market_volatility : FearAndGreedIndicator
        Market Volatility (VIX) indicator
    put_call_options : FearAndGreedIndicator
        Put and Call Options indicator
    market_momentum : FearAndGreedIndicator
        Market Momentum (S&P 500) indicator
    stock_price_strength : FearAndGreedIndicator
        Stock Price Strength indicator
    stock_price_breadth : FearAndGreedIndicator
        Stock Price Breadth indicator
    safe_haven_demand : FearAndGreedIndicator
        Safe Haven Demand indicator
    """

    # Mapping from API keys to indicator names
    _INDICATOR_MAP = {
        "junk_bond_demand": "Junk Bond Demand",
        "market_volatility_vix": "Market Volatility (VIX)",
        "put_call_options": "Put and Call Options",
        "market_momentum_sp500": "Market Momentum (S&P 500)",
        "stock_price_strength": "Stock Price Strength",
        "stock_price_breadth": "Stock Price Breadth",
        "safe_haven_demand": "Safe Haven Demand",
    }

    def __init__(self):
        """Constructor"""
        self.score = 0.0
        self.rating = "N/A"
        self.previous_close = 0.0
        self.previous_1_week = 0.0
        self.previous_1_month = 0.0
        self.previous_1_year = 0.0
        self.timestamp = None
        self.historical_data = []

        self.junk_bond_demand = None
        self.market_volatility = None
        self.put_call_options = None
        self.market_momentum = None
        self.stock_price_strength = None
        self.stock_price_breadth = None
        self.safe_haven_demand = None

        self._load_fear_and_greed()

    def _load_fear_and_greed(self):
        """Load Fear and Greed Index from CNN API"""
        data = scrape_cnn._get_fear_greed_data()

        # Load main index data
        fg_data = data.get("fear_and_greed", {})
        self.score = fg_data.get("score", 0.0)
        self.rating = fg_data.get("rating", "N/A")
        self.previous_close = fg_data.get("previous_close", 0.0)
        self.previous_1_week = fg_data.get("previous_1_week", 0.0)
        self.previous_1_month = fg_data.get("previous_1_month", 0.0)
        self.previous_1_year = fg_data.get("previous_1_year", 0.0)

        timestamp_str = fg_data.get("timestamp")
        if timestamp_str:
            self.timestamp = datetime.fromisoformat(timestamp_str.replace("+00:00", "+0000"))

        # Load historical data
        fg_historical = data.get("fear_and_greed_historical", {})
        self.historical_data = fg_historical.get("data", [])

        # Load indicators
        self.junk_bond_demand = FearAndGreedIndicator(
            self._INDICATOR_MAP["junk_bond_demand"],
            data.get("junk_bond_demand")
        )
        self.market_volatility = FearAndGreedIndicator(
            self._INDICATOR_MAP["market_volatility_vix"],
            data.get("market_volatility_vix")
        )
        self.put_call_options = FearAndGreedIndicator(
            self._INDICATOR_MAP["put_call_options"],
            data.get("put_call_options")
        )
        self.market_momentum = FearAndGreedIndicator(
            self._INDICATOR_MAP["market_momentum_sp500"],
            data.get("market_momentum_sp500")
        )
        self.stock_price_strength = FearAndGreedIndicator(
            self._INDICATOR_MAP["stock_price_strength"],
            data.get("stock_price_strength")
        )
        self.stock_price_breadth = FearAndGreedIndicator(
            self._INDICATOR_MAP["stock_price_breadth"],
            data.get("stock_price_breadth")
        )
        self.safe_haven_demand = FearAndGreedIndicator(
            self._INDICATOR_MAP["safe_haven_demand"],
            data.get("safe_haven_demand")
        )

    @property
    def all_indicators(self) -> list:
        """Get all indicators as a list"""
        return [
            self.junk_bond_demand,
            self.market_volatility,
            self.put_call_options,
            self.market_momentum,
            self.stock_price_strength,
            self.stock_price_breadth,
            self.safe_haven_demand,
        ]

    def get_score(self) -> float:
        """Get current Fear and Greed Index score"""
        return self.score

    def get_rating(self) -> str:
        """Get current sentiment rating"""
        return self.rating

    def get_junk_bond_demand(self) -> FearAndGreedIndicator:
        """Get Junk Bond Demand indicator"""
        return self.junk_bond_demand

    def get_market_volatility(self) -> FearAndGreedIndicator:
        """Get Market Volatility indicator"""
        return self.market_volatility

    def get_put_call_options(self) -> FearAndGreedIndicator:
        """Get Put and Call Options indicator"""
        return self.put_call_options

    def get_market_momentum(self) -> FearAndGreedIndicator:
        """Get Market Momentum indicator"""
        return self.market_momentum

    def get_stock_price_strength(self) -> FearAndGreedIndicator:
        """Get Stock Price Strength indicator"""
        return self.stock_price_strength

    def get_stock_price_breadth(self) -> FearAndGreedIndicator:
        """Get Stock Price Breadth indicator"""
        return self.stock_price_breadth

    def get_safe_haven_demand(self) -> FearAndGreedIndicator:
        """Get Safe Haven Demand indicator"""
        return self.safe_haven_demand

    def get_index_summary(self) -> str:
        """Get index summary"""
        summary = f"Fear & Greed Now: {self.score:.1f} ({self.rating.title()})\n"
        summary += f"   Previous Close: {self.previous_close:.1f}\n"
        summary += f"   1 Week Ago: {self.previous_1_week:.1f}\n"
        summary += f"   1 Month Ago: {self.previous_1_month:.1f}\n"
        summary += f"   1 Year Ago: {self.previous_1_year:.1f}"
        return summary

    def get_indicators_report(self) -> str:
        """Get all indicators report"""
        reports = []
        for indicator in self.all_indicators:
            reports.append(indicator.get_report())
        return "\n".join(reports)

    def get_complete_report(self) -> str:
        """Get complete Fear and Greed report"""
        return f"{self.get_index_summary()}\n\n{self.get_indicators_report()}"

    def get_historical_data(self) -> list:
        """Get historical Fear and Greed Index data"""
        return self.historical_data

    def plot_fear_greed_index(self, ax: plt.Axes = None) -> plt.Axes:
        """Plot Fear and Greed Index historical chart

        Parameters
        ----------
        ax : plt.Axes, optional
            Matplotlib axes to plot on. If None, creates new figure.

        Returns
        -------
        plt.Axes
            Matplotlib axes with the chart
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))

        if not self.historical_data:
            return ax

        # Extract dates and values
        dates = [datetime.fromtimestamp(d["x"] / 1000) for d in self.historical_data]
        values = [d["y"] for d in self.historical_data]

        # Create color gradient (red=fear, green=greed)
        cmap = LinearSegmentedColormap.from_list("fear_greed", ["#8B0000", "#FF4500", "#FFD700", "#90EE90", "#006400"])

        # Plot with color based on value
        for i in range(len(dates) - 1):
            color = cmap(values[i] / 100)
            ax.plot(dates[i:i+2], values[i:i+2], color=color, linewidth=2)

        # Add horizontal bands for sentiment zones
        ax.axhspan(0, 25, alpha=0.1, color='red', label='Extreme Fear')
        ax.axhspan(25, 45, alpha=0.1, color='orange', label='Fear')
        ax.axhspan(45, 55, alpha=0.1, color='yellow', label='Neutral')
        ax.axhspan(55, 75, alpha=0.1, color='lightgreen', label='Greed')
        ax.axhspan(75, 100, alpha=0.1, color='green', label='Extreme Greed')

        ax.set_ylim(0, 100)
        ax.set_xlabel("Date")
        ax.set_ylabel("Fear & Greed Index")
        ax.set_title(f"CNN Fear & Greed Index - Current: {self.score:.1f} ({self.rating.title()})")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=8)

        return ax

    def plot_all_indicators(self, fig: plt.Figure = None) -> plt.Figure:
        """Plot all indicator scores as a bar chart

        Parameters
        ----------
        fig : plt.Figure, optional
            Matplotlib figure to plot on. If None, creates new figure.

        Returns
        -------
        plt.Figure
            Matplotlib figure with the chart
        """
        if fig is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        else:
            ax = fig.add_subplot(111)

        names = [ind.name for ind in self.all_indicators]
        scores = [ind.score for ind in self.all_indicators]

        # Color based on score
        colors = []
        for score in scores:
            if score < 25:
                colors.append('#8B0000')  # Extreme Fear - dark red
            elif score < 45:
                colors.append('#FF4500')  # Fear - orange red
            elif score < 55:
                colors.append('#FFD700')  # Neutral - gold
            elif score < 75:
                colors.append('#90EE90')  # Greed - light green
            else:
                colors.append('#006400')  # Extreme Greed - dark green

        bars = ax.barh(names, scores, color=colors)
        ax.set_xlim(0, 100)
        ax.set_xlabel("Score")
        ax.set_title(f"Fear & Greed Indicators - Overall: {self.score:.1f} ({self.rating.title()})")

        # Add score labels on bars
        for bar, score in zip(bars, scores):
            ax.text(score + 2, bar.get_y() + bar.get_height()/2, f'{score:.1f}',
                    va='center', fontsize=9)

        ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
        plt.tight_layout()

        return fig

    def plot_all_charts(self, fig: plt.Figure = None) -> plt.Figure:
        """Plot comprehensive Fear and Greed dashboard

        Parameters
        ----------
        fig : plt.Figure, optional
            Matplotlib figure to plot on. If None, creates new figure.

        Returns
        -------
        plt.Figure
            Matplotlib figure with all charts
        """
        if fig is None:
            fig = plt.figure(figsize=(14, 10))

        # Main index chart (top)
        ax1 = fig.add_subplot(2, 1, 1)
        self.plot_fear_greed_index(ax1)

        # Indicators bar chart (bottom)
        ax2 = fig.add_subplot(2, 1, 2)
        names = [ind.name for ind in self.all_indicators]
        scores = [ind.score for ind in self.all_indicators]

        colors = []
        for score in scores:
            if score < 25:
                colors.append('#8B0000')
            elif score < 45:
                colors.append('#FF4500')
            elif score < 55:
                colors.append('#FFD700')
            elif score < 75:
                colors.append('#90EE90')
            else:
                colors.append('#006400')

        bars = ax2.barh(names, scores, color=colors)
        ax2.set_xlim(0, 100)
        ax2.set_xlabel("Score")
        ax2.set_title("Individual Indicators")

        for bar, score in zip(bars, scores):
            ax2.text(score + 2, bar.get_y() + bar.get_height()/2, f'{score:.1f}',
                    va='center', fontsize=9)

        ax2.axvline(x=50, color='gray', linestyle='--', alpha=0.5)

        plt.tight_layout()
        return fig
