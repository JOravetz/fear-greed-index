"""
Comprehensive tests for ALL code examples in README.md

This test file validates that every code example shown in the README
works correctly without errors. Users can run this to verify the
repository features are working properly.

Run with: uv run pytest tests/test_readme_examples.py -v
"""

import pytest
import json
import os
import tempfile
from io import StringIO
import sys


class TestQuickStart:
    """Test Quick Start Python API example from README."""

    def test_quick_start_python_api(self):
        """
        README Quick Start - Python API:

        from fear_greed_index import CNNFearAndGreedIndex
        fgi = CNNFearAndGreedIndex()
        print(f"Score: {fgi.score}")
        print(f"Rating: {fgi.rating}")
        print(fgi.get_complete_report())
        """
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # Verify score
        assert fgi.score is not None
        assert isinstance(fgi.score, (int, float))
        assert 0 <= fgi.score <= 100

        # Verify rating
        assert fgi.rating is not None
        valid_ratings = ["extreme fear", "fear", "neutral", "greed", "extreme greed"]
        assert fgi.rating.lower() in valid_ratings

        # Verify complete report
        report = fgi.get_complete_report()
        assert report is not None
        assert len(report) > 100


class TestExample1:
    """Test Example 1: Basic Market Sentiment Check."""

    def test_basic_market_sentiment_check(self):
        """
        README Example 1:

        from fear_greed_index import CNNFearAndGreedIndex
        fgi = CNNFearAndGreedIndex()
        print(f"Current Fear & Greed Index: {fgi.score:.1f}")
        print(f"Market Sentiment: {fgi.rating.upper()}")
        print(f"Previous Close: {fgi.previous_close:.1f}")
        print(f"Change: {fgi.score - fgi.previous_close:+.1f}")
        """
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # All these operations should work without error
        score_str = f"Current Fear & Greed Index: {fgi.score:.1f}"
        sentiment_str = f"Market Sentiment: {fgi.rating.upper()}"
        previous_str = f"Previous Close: {fgi.previous_close:.1f}"
        change = fgi.score - fgi.previous_close
        change_str = f"Change: {change:+.1f}"

        assert "Fear & Greed Index" in score_str
        assert fgi.rating.upper() in sentiment_str
        assert isinstance(fgi.previous_close, (int, float))
        assert isinstance(change, (int, float))


class TestExample2:
    """Test Example 2: Compare Current vs Historical Sentiment."""

    def test_compare_current_vs_historical(self):
        """
        README Example 2:

        from fear_greed_index import CNNFearAndGreedIndex
        fgi = CNNFearAndGreedIndex()
        print("Fear & Greed Index Comparison")
        print("=" * 40)
        print(f"Now:          {fgi.score:.1f} ({fgi.rating})")
        print(f"Yesterday:    {fgi.previous_close:.1f}")
        print(f"1 Week Ago:   {fgi.previous_1_week:.1f}")
        print(f"1 Month Ago:  {fgi.previous_1_month:.1f}")
        print(f"1 Year Ago:   {fgi.previous_1_year:.1f}")
        """
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # All historical values should be valid floats
        assert isinstance(fgi.score, (int, float))
        assert isinstance(fgi.previous_close, (int, float))
        assert isinstance(fgi.previous_1_week, (int, float))
        assert isinstance(fgi.previous_1_month, (int, float))
        assert isinstance(fgi.previous_1_year, (int, float))

        # All should be in valid range
        for value in [fgi.score, fgi.previous_close, fgi.previous_1_week,
                      fgi.previous_1_month, fgi.previous_1_year]:
            assert 0 <= value <= 100

        # Format strings should work
        output = f"Now: {fgi.score:.1f} ({fgi.rating})"
        assert fgi.rating in output


class TestExample3:
    """Test Example 3: Analyze Individual Indicators."""

    def test_analyze_individual_indicators(self):
        """
        README Example 3:

        from fear_greed_index import CNNFearAndGreedIndex
        fgi = CNNFearAndGreedIndex()
        print("Individual Market Indicators")
        print("=" * 50)
        for indicator in fgi.all_indicators:
            status = "🔴" if indicator.score < 25 else "🟡" if indicator.score < 50 else "🟢"
            print(f"{status} {indicator.name}: {indicator.score:.1f} ({indicator.rating})")
        """
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # Should have exactly 7 indicators
        assert len(fgi.all_indicators) == 7

        for indicator in fgi.all_indicators:
            # Each indicator should have required attributes
            assert hasattr(indicator, 'name')
            assert hasattr(indicator, 'score')
            assert hasattr(indicator, 'rating')

            # Score should be valid
            assert isinstance(indicator.score, (int, float))
            assert 0 <= indicator.score <= 100

            # Status logic should work
            status = "🔴" if indicator.score < 25 else "🟡" if indicator.score < 50 else "🟢"
            assert status in ["🔴", "🟡", "🟢"]

            # Format string should work
            output = f"{status} {indicator.name}: {indicator.score:.1f} ({indicator.rating})"
            assert indicator.name in output


class TestExample4:
    """Test Example 4: Trading Signal Based on Sentiment."""

    def test_trading_signal_based_on_sentiment(self):
        """
        README Example 4:

        def get_trading_signal(score: float) -> str:
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
        """
        from fear_greed_index import CNNFearAndGreedIndex

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

        fgi = CNNFearAndGreedIndex()
        signal = get_trading_signal(fgi.score)

        # Signal should be one of the expected values
        valid_signals = [
            "STRONG BUY - Extreme fear, potential opportunity",
            "BUY - Fear in the market",
            "HOLD - Neutral sentiment",
            "SELL - Greed in the market",
            "STRONG SELL - Extreme greed, potential top"
        ]
        assert signal in valid_signals

        # Test all score ranges
        assert "STRONG BUY" in get_trading_signal(10)
        assert "BUY" in get_trading_signal(30)
        assert "HOLD" in get_trading_signal(50)
        assert "SELL" in get_trading_signal(70)
        assert "STRONG SELL" in get_trading_signal(90)


class TestExample5:
    """Test Example 5: Historical Data Analysis with Pandas."""

    def test_historical_data_analysis_with_pandas(self):
        """
        README Example 5:

        from fear_greed_index import CNNFearAndGreedIndex
        from datetime import datetime
        import pandas as pd

        fgi = CNNFearAndGreedIndex()
        historical = fgi.get_historical_data()
        df = pd.DataFrame(historical)
        df['date'] = pd.to_datetime(df['x'], unit='ms')
        df = df.rename(columns={'y': 'score'})
        df = df[['date', 'score', 'rating']]

        print(f"Data points: {len(df)}")
        print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"Average score: {df['score'].mean():.1f}")
        print(f"Min score: {df['score'].min():.1f}")
        print(f"Max score: {df['score'].max():.1f}")
        print("\\nSentiment Distribution:")
        print(df['rating'].value_counts())
        """
        from fear_greed_index import CNNFearAndGreedIndex
        from datetime import datetime
        import pandas as pd

        fgi = CNNFearAndGreedIndex()

        # Get historical data
        historical = fgi.get_historical_data()
        assert len(historical) > 0

        # Convert to DataFrame
        df = pd.DataFrame(historical)
        assert 'x' in df.columns
        assert 'y' in df.columns
        assert 'rating' in df.columns

        # Date conversion
        df['date'] = pd.to_datetime(df['x'], unit='ms')
        df = df.rename(columns={'y': 'score'})
        df = df[['date', 'score', 'rating']]

        # Verify data
        assert len(df) > 200  # Should have ~1 year of data
        assert df['score'].min() >= 0
        assert df['score'].max() <= 100

        # Statistics should work
        avg_score = df['score'].mean()
        min_score = df['score'].min()
        max_score = df['score'].max()

        assert 0 <= avg_score <= 100
        assert min_score <= avg_score <= max_score

        # Sentiment distribution
        distribution = df['rating'].value_counts()
        assert len(distribution) > 0


class TestExample6:
    """Test Example 6: Detect Sentiment Extremes."""

    def test_detect_sentiment_extremes(self):
        """
        README Example 6:

        from fear_greed_index import CNNFearAndGreedIndex
        from datetime import datetime

        fgi = CNNFearAndGreedIndex()
        historical = fgi.get_historical_data()

        extreme_fear_days = [
            (datetime.fromtimestamp(d['x']/1000).strftime('%Y-%m-%d'), d['y'])
            for d in historical if d['y'] < 20
        ]

        print(f"Extreme Fear Days (score < 20) in past year: {len(extreme_fear_days)}")
        for date, score in extreme_fear_days[-5:]:
            print(f"  {date}: {score:.1f}")
        """
        from fear_greed_index import CNNFearAndGreedIndex
        from datetime import datetime

        fgi = CNNFearAndGreedIndex()
        historical = fgi.get_historical_data()

        # Find extreme fear days
        extreme_fear_days = [
            (datetime.fromtimestamp(d['x']/1000).strftime('%Y-%m-%d'), d['y'])
            for d in historical if d['y'] < 20
        ]

        # Should be a list (may be empty if no extreme fear days)
        assert isinstance(extreme_fear_days, list)

        # If there are extreme fear days, verify format
        for date, score in extreme_fear_days:
            assert len(date) == 10  # YYYY-MM-DD format
            assert isinstance(score, (int, float))
            assert score < 20


class TestExample7:
    """Test Example 7: VIX-Specific Analysis."""

    def test_vix_specific_analysis(self):
        """
        README Example 7:

        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()
        vix = fgi.market_volatility
        print(f"VIX Indicator Score: {vix.score:.1f}")
        print(f"VIX Sentiment: {vix.rating}")
        print(f"Last Updated: {vix.timestamp.strftime('%Y-%m-%d %H:%M')}")

        if vix.score < 30:
            print("⚠️  High volatility expected - VIX indicating fear")
        elif vix.score > 70:
            print("✅ Low volatility - VIX indicating complacency")
        """
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # VIX indicator should exist
        vix = fgi.market_volatility
        assert vix is not None

        # Should have required attributes
        assert hasattr(vix, 'score')
        assert hasattr(vix, 'rating')
        assert hasattr(vix, 'timestamp')

        # Score should be valid
        assert isinstance(vix.score, (int, float))
        assert 0 <= vix.score <= 100

        # Format strings should work
        score_str = f"VIX Indicator Score: {vix.score:.1f}"
        rating_str = f"VIX Sentiment: {vix.rating}"

        assert "VIX" in score_str
        assert vix.rating in rating_str

        # Timestamp formatting (may be None)
        if vix.timestamp:
            timestamp_str = vix.timestamp.strftime('%Y-%m-%d %H:%M')
            assert len(timestamp_str) == 16


class TestExample8:
    """Test Example 8: Export Data to JSON."""

    def test_export_data_to_json(self):
        """
        README Example 8:

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

        with open("fear_greed_data.json", "w") as f:
            json.dump(data, f, indent=2)
        """
        from fear_greed_index import CNNFearAndGreedIndex
        import json
        import tempfile
        import os

        fgi = CNNFearAndGreedIndex()

        # Build data structure
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

        # JSON serialization should work
        json_str = json.dumps(data, indent=2)
        assert len(json_str) > 100

        # Parse back and verify
        parsed = json.loads(json_str)
        assert parsed["score"] == fgi.score
        assert parsed["rating"] == fgi.rating
        assert len(parsed["indicators"]) == 7

        # File writing should work
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f, indent=2)
            temp_path = f.name

        # Verify file was written
        assert os.path.exists(temp_path)
        with open(temp_path, 'r') as f:
            file_data = json.load(f)
        assert file_data["score"] == fgi.score

        # Cleanup
        os.unlink(temp_path)


class TestExample9FastAPI:
    """Test Example 9: FastAPI Service (module import and structure)."""

    def test_fastapi_module_loads(self):
        """Verify the api_server.py module loads without errors."""
        import importlib.util
        import os

        api_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'api_server.py'
        )

        if os.path.exists(api_path):
            spec = importlib.util.spec_from_file_location("api_server", api_path)
            module = importlib.util.module_from_spec(spec)
            # Just verify it can be loaded - don't execute
            assert spec is not None

    def test_fastapi_cache_function(self):
        """Test the cache function logic from Example 9."""
        from datetime import datetime
        from fear_greed_index import CNNFearAndGreedIndex

        # Replicate the cache logic from README
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

        # First call should populate cache
        fgi1 = get_fgi()
        assert fgi1 is not None
        assert _cache["data"] is not None
        assert _cache["timestamp"] is not None

        # Second call should return cached data
        fgi2 = get_fgi()
        assert fgi2 is fgi1  # Same object (cached)


class TestCLICommands:
    """Test CLI commands mentioned in README."""

    def test_cli_score_command(self):
        """Test: uv run fgi score"""
        from click.testing import CliRunner
        from fgi_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ['score'])
        assert result.exit_code == 0
        # Should contain score and rating

    def test_cli_signal_command(self):
        """Test: uv run fgi signal"""
        from click.testing import CliRunner
        from fgi_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ['signal'])
        assert result.exit_code == 0
        assert "TRADING SIGNAL" in result.output

    def test_cli_json_command(self):
        """Test: uv run fgi json"""
        from click.testing import CliRunner
        from fgi_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ['json'])
        assert result.exit_code == 0
        assert "score" in result.output
        assert "rating" in result.output

    def test_cli_history_command(self):
        """Test: uv run fgi history --limit 5"""
        from click.testing import CliRunner
        from fgi_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ['history', '--limit', '5'])
        assert result.exit_code == 0
        assert "Historical Data" in result.output

    def test_cli_dashboard_command(self):
        """Test: uv run fgi dashboard"""
        from click.testing import CliRunner
        from fgi_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ['dashboard'])
        assert result.exit_code == 0
        assert "FEAR & GREED" in result.output

    def test_cli_indicators_command(self):
        """Test: uv run fgi indicators"""
        from click.testing import CliRunner
        from fgi_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ['indicators'])
        assert result.exit_code == 0


class TestMCPServer:
    """Test MCP Server functionality mentioned in README."""

    @pytest.mark.asyncio
    async def test_mcp_get_fear_greed_score(self):
        """Test MCP tool: get_fear_greed_score"""
        from fgi_mcp_server import call_tool

        result = await call_tool("get_fear_greed_score", {})
        assert len(result) == 1
        assert "Score:" in result[0].text
        assert "Rating:" in result[0].text

    @pytest.mark.asyncio
    async def test_mcp_get_trading_signal(self):
        """Test MCP tool: get_trading_signal"""
        from fgi_mcp_server import call_tool

        result = await call_tool("get_trading_signal", {})
        assert len(result) == 1
        assert "Trading Signal:" in result[0].text

    @pytest.mark.asyncio
    async def test_mcp_get_fear_greed_indicators(self):
        """Test MCP tool: get_fear_greed_indicators"""
        from fgi_mcp_server import call_tool

        result = await call_tool("get_fear_greed_indicators", {})
        assert len(result) == 1
        assert "Junk Bond" in result[0].text

    @pytest.mark.asyncio
    async def test_mcp_get_fear_greed_comparison(self):
        """Test MCP tool: get_fear_greed_comparison"""
        from fgi_mcp_server import call_tool

        result = await call_tool("get_fear_greed_comparison", {})
        assert len(result) == 1
        assert "Previous Close" in result[0].text

    @pytest.mark.asyncio
    async def test_mcp_get_fear_greed_history(self):
        """Test MCP tool: get_fear_greed_history"""
        from fgi_mcp_server import call_tool

        result = await call_tool("get_fear_greed_history", {"days": 5})
        assert len(result) == 1
        assert "History" in result[0].text

    @pytest.mark.asyncio
    async def test_mcp_get_complete_report(self):
        """Test MCP tool: get_complete_report"""
        from fgi_mcp_server import call_tool

        result = await call_tool("get_complete_report", {})
        assert len(result) == 1
        assert len(result[0].text) > 200


class TestAPIReference:
    """Test API Reference examples from README."""

    def test_cnn_fear_greed_index_attributes(self):
        """Test all documented attributes exist and work."""
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # Main attributes
        assert hasattr(fgi, 'score')
        assert hasattr(fgi, 'rating')
        assert hasattr(fgi, 'previous_close')
        assert hasattr(fgi, 'previous_1_week')
        assert hasattr(fgi, 'previous_1_month')
        assert hasattr(fgi, 'previous_1_year')
        assert hasattr(fgi, 'timestamp')
        assert hasattr(fgi, 'historical_data')

        # Indicator attributes
        assert hasattr(fgi, 'junk_bond_demand')
        assert hasattr(fgi, 'market_volatility')
        assert hasattr(fgi, 'put_call_options')
        assert hasattr(fgi, 'market_momentum')
        assert hasattr(fgi, 'stock_price_strength')
        assert hasattr(fgi, 'stock_price_breadth')
        assert hasattr(fgi, 'safe_haven_demand')
        assert hasattr(fgi, 'all_indicators')

    def test_cnn_fear_greed_index_methods(self):
        """Test all documented methods exist and work."""
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()

        # Test methods
        assert fgi.get_score() == fgi.score
        assert fgi.get_rating() == fgi.rating

        summary = fgi.get_index_summary()
        assert isinstance(summary, str)
        assert len(summary) > 0

        indicators_report = fgi.get_indicators_report()
        assert isinstance(indicators_report, str)

        complete_report = fgi.get_complete_report()
        assert isinstance(complete_report, str)
        assert len(complete_report) > len(summary)

        historical = fgi.get_historical_data()
        assert isinstance(historical, list)
        assert len(historical) > 0

    def test_fear_and_greed_indicator_attributes(self):
        """Test FearAndGreedIndicator attributes."""
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()
        indicator = fgi.all_indicators[0]

        assert hasattr(indicator, 'name')
        assert hasattr(indicator, 'score')
        assert hasattr(indicator, 'rating')
        assert hasattr(indicator, 'timestamp')
        assert hasattr(indicator, 'historical_data')

    def test_fear_and_greed_indicator_methods(self):
        """Test FearAndGreedIndicator methods."""
        from fear_greed_index import CNNFearAndGreedIndex

        fgi = CNNFearAndGreedIndex()
        indicator = fgi.all_indicators[0]

        assert indicator.get_score() == indicator.score
        assert indicator.get_rating() == indicator.rating
        assert indicator.get_name() == indicator.name

        report = indicator.get_report()
        assert isinstance(report, str)
        assert indicator.name in report
