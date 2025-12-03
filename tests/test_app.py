"""Tests for Streamlit app functions."""

import pytest
import sys

# Mock streamlit for testing
class MockStreamlit:
    def set_page_config(self, **kwargs): pass
    def cache_data(self, **kwargs): return lambda f: f
    def title(self, *args): pass
    def markdown(self, *args, **kwargs): pass
    def columns(self, *args): return [None, None]
    def spinner(self, *args): return self
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def plotly_chart(self, *args, **kwargs): pass
    def metric(self, *args, **kwargs): pass
    def divider(self): pass
    def button(self, *args): return False
    cache_data = staticmethod(lambda **kw: lambda f: f)

sys.modules['streamlit'] = MockStreamlit()

from app import get_color_for_score, create_gauge, create_historical_chart, create_indicators_chart
from fear_greed_index import CNNFearAndGreedIndex


class TestAppHelpers:
    """Tests for app helper functions."""

    def test_get_color_extreme_fear(self):
        """Test color for extreme fear score."""
        assert get_color_for_score(10) == "#8B0000"

    def test_get_color_fear(self):
        """Test color for fear score."""
        assert get_color_for_score(35) == "#FF4500"

    def test_get_color_neutral(self):
        """Test color for neutral score."""
        assert get_color_for_score(50) == "#FFD700"

    def test_get_color_greed(self):
        """Test color for greed score."""
        assert get_color_for_score(65) == "#32CD32"

    def test_get_color_extreme_greed(self):
        """Test color for extreme greed score."""
        assert get_color_for_score(85) == "#006400"


class TestCharts:
    """Tests for chart creation functions."""

    @pytest.fixture
    def fgi(self):
        """Create FGI instance for tests."""
        return CNNFearAndGreedIndex()

    def test_create_gauge(self, fgi):
        """Test gauge chart creation."""
        fig = create_gauge(fgi.score, "Test")
        assert fig is not None

    def test_create_gauge_with_different_scores(self):
        """Test gauge with various scores."""
        for score in [0, 25, 50, 75, 100]:
            fig = create_gauge(score, f"Score {score}")
            assert fig is not None

    def test_create_historical_chart(self, fgi):
        """Test historical chart creation."""
        fig = create_historical_chart(fgi.historical_data[:10])
        assert fig is not None

    def test_create_historical_chart_empty(self):
        """Test historical chart with minimal data."""
        fig = create_historical_chart([{"x": 1701475200000, "y": 50}])
        assert fig is not None

    def test_create_indicators_chart(self, fgi):
        """Test indicators chart creation."""
        fig = create_indicators_chart(fgi.all_indicators)
        assert fig is not None
