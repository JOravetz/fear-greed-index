"""Tests for core Fear & Greed Index library."""

import pytest
from datetime import datetime
from fear_greed_index import CNNFearAndGreedIndex
from fear_greed_index.FearAndGreedIndicator import FearAndGreedIndicator


class TestFearAndGreedIndicator:
    """Tests for FearAndGreedIndicator class."""

    def test_init_empty(self):
        """Test creating indicator without data."""
        indicator = FearAndGreedIndicator("Test Indicator")
        assert indicator.name == "Test Indicator"
        assert indicator.score == 0.0
        assert indicator.rating == "N/A"
        assert indicator.timestamp is None
        assert indicator.historical_data == []

    def test_init_with_data(self):
        """Test creating indicator with data."""
        data = {
            "score": 75.5,
            "rating": "greed",
            "timestamp": 1701475200000,  # Example timestamp
            "data": [{"x": 1701475200000, "y": 75.5}]
        }
        indicator = FearAndGreedIndicator("Test Indicator", data)
        assert indicator.score == 75.5
        assert indicator.rating == "greed"
        assert indicator.timestamp is not None
        assert len(indicator.historical_data) == 1

    def test_get_methods(self):
        """Test getter methods."""
        indicator = FearAndGreedIndicator("VIX", {"score": 50, "rating": "neutral"})
        assert indicator.get_score() == 50
        assert indicator.get_rating() == "neutral"
        assert indicator.get_name() == "VIX"

    def test_get_report(self):
        """Test report generation."""
        indicator = FearAndGreedIndicator("VIX", {"score": 50, "rating": "neutral"})
        report = indicator.get_report()
        assert "VIX" in report
        assert "Neutral" in report
        assert "50.0" in report


class TestCNNFearAndGreedIndex:
    """Tests for CNNFearAndGreedIndex class."""

    @pytest.fixture
    def fgi(self):
        """Create FGI instance for tests."""
        return CNNFearAndGreedIndex()

    def test_instantiation(self, fgi):
        """Test that FGI can be instantiated."""
        assert fgi is not None

    def test_score_range(self, fgi):
        """Test score is within valid range."""
        assert 0 <= fgi.score <= 100

    def test_rating_valid(self, fgi):
        """Test rating is one of valid values."""
        valid_ratings = ["extreme fear", "fear", "neutral", "greed", "extreme greed"]
        assert fgi.rating.lower() in valid_ratings

    def test_historical_comparisons(self, fgi):
        """Test historical comparison values exist."""
        assert isinstance(fgi.previous_close, (int, float))
        assert isinstance(fgi.previous_1_week, (int, float))
        assert isinstance(fgi.previous_1_month, (int, float))
        assert isinstance(fgi.previous_1_year, (int, float))

    def test_all_indicators_count(self, fgi):
        """Test that all 7 indicators are present."""
        assert len(fgi.all_indicators) == 7

    def test_indicator_scores_valid(self, fgi):
        """Test all indicator scores are in valid range."""
        for indicator in fgi.all_indicators:
            assert 0 <= indicator.score <= 100, f"{indicator.name} score out of range"

    def test_specific_indicators_exist(self, fgi):
        """Test specific indicators are accessible."""
        assert fgi.junk_bond_demand is not None
        assert fgi.market_volatility is not None
        assert fgi.put_call_options is not None
        assert fgi.market_momentum is not None
        assert fgi.stock_price_strength is not None
        assert fgi.stock_price_breadth is not None
        assert fgi.safe_haven_demand is not None

    def test_historical_data_not_empty(self, fgi):
        """Test historical data is available."""
        historical = fgi.get_historical_data()
        assert len(historical) > 0

    def test_historical_data_format(self, fgi):
        """Test historical data has correct format."""
        historical = fgi.get_historical_data()
        for point in historical[:5]:  # Check first 5 points
            assert "x" in point
            assert "y" in point
            assert "rating" in point

    def test_get_score(self, fgi):
        """Test get_score method."""
        assert fgi.get_score() == fgi.score

    def test_get_rating(self, fgi):
        """Test get_rating method."""
        assert fgi.get_rating() == fgi.rating

    def test_get_index_summary(self, fgi):
        """Test index summary generation."""
        summary = fgi.get_index_summary()
        assert len(summary) > 10
        assert "Fear & Greed" in summary or str(fgi.score) in summary

    def test_get_complete_report(self, fgi):
        """Test complete report generation."""
        report = fgi.get_complete_report()
        assert len(report) > 100
