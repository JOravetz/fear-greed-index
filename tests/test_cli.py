"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner
from fgi_cli import cli, get_color_for_score, get_emoji_for_score, create_gauge


class TestCLIHelpers:
    """Tests for CLI helper functions."""

    def test_get_color_extreme_fear(self):
        """Test color for extreme fear score."""
        assert get_color_for_score(10) == "red"

    def test_get_color_fear(self):
        """Test color for fear score."""
        assert get_color_for_score(35) == "orange1"

    def test_get_color_neutral(self):
        """Test color for neutral score."""
        assert get_color_for_score(50) == "yellow"

    def test_get_color_greed(self):
        """Test color for greed score."""
        assert get_color_for_score(65) == "green"

    def test_get_color_extreme_greed(self):
        """Test color for extreme greed score."""
        assert get_color_for_score(85) == "dark_green"

    def test_get_emoji_extreme_fear(self):
        """Test emoji for extreme fear score."""
        assert get_emoji_for_score(10) == "🔴"

    def test_get_emoji_fear(self):
        """Test emoji for fear score."""
        assert get_emoji_for_score(35) == "🟠"

    def test_get_emoji_neutral(self):
        """Test emoji for neutral score."""
        assert get_emoji_for_score(50) == "🟡"

    def test_get_emoji_greed(self):
        """Test emoji for greed score."""
        assert get_emoji_for_score(65) == "🟢"

    def test_get_emoji_extreme_greed(self):
        """Test emoji for extreme greed score."""
        assert get_emoji_for_score(85) == "💚"

    def test_create_gauge(self):
        """Test gauge creation."""
        gauge = create_gauge(50, width=20)
        assert "█" in gauge
        assert "░" in gauge


class TestCLICommands:
    """Tests for CLI commands."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_help(self, runner):
        """Test --help option."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "CNN Fear & Greed Index CLI" in result.output

    def test_score_command(self, runner):
        """Test score command."""
        result = runner.invoke(cli, ["score"])
        assert result.exit_code == 0
        # Output should contain score and rating

    def test_signal_command(self, runner):
        """Test signal command."""
        result = runner.invoke(cli, ["signal"])
        assert result.exit_code == 0
        assert "TRADING SIGNAL" in result.output

    def test_json_command(self, runner):
        """Test json command."""
        result = runner.invoke(cli, ["json"])
        assert result.exit_code == 0
        assert "score" in result.output
        assert "rating" in result.output

    def test_history_command(self, runner):
        """Test history command."""
        result = runner.invoke(cli, ["history", "--limit", "5"])
        assert result.exit_code == 0
        assert "Historical Data" in result.output

    def test_dashboard_command(self, runner):
        """Test dashboard command."""
        result = runner.invoke(cli, ["dashboard"])
        assert result.exit_code == 0
        assert "FEAR & GREED" in result.output

    def test_indicators_command(self, runner):
        """Test indicators command."""
        result = runner.invoke(cli, ["indicators"])
        assert result.exit_code == 0
        # Should show individual indicators
