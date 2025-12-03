"""Tests for MCP Server."""

import pytest
import asyncio
from fgi_mcp_server import list_tools, call_tool


class TestMCPServer:
    """Tests for MCP Server tools."""

    @pytest.fixture
    def event_loop(self):
        """Create event loop for async tests."""
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()

    @pytest.mark.asyncio
    async def test_list_tools_count(self):
        """Test that all tools are listed."""
        tools = await list_tools()
        assert len(tools) == 6

    @pytest.mark.asyncio
    async def test_list_tools_names(self):
        """Test that expected tools are present."""
        tools = await list_tools()
        tool_names = [t.name for t in tools]

        expected = [
            "get_fear_greed_score",
            "get_fear_greed_indicators",
            "get_fear_greed_comparison",
            "get_trading_signal",
            "get_fear_greed_history",
            "get_complete_report"
        ]

        for name in expected:
            assert name in tool_names

    @pytest.mark.asyncio
    async def test_get_fear_greed_score(self):
        """Test get_fear_greed_score tool."""
        result = await call_tool("get_fear_greed_score", {})
        assert len(result) == 1
        assert "Score:" in result[0].text
        assert "Rating:" in result[0].text

    @pytest.mark.asyncio
    async def test_get_fear_greed_indicators(self):
        """Test get_fear_greed_indicators tool."""
        result = await call_tool("get_fear_greed_indicators", {})
        assert len(result) == 1
        assert "Junk Bond" in result[0].text

    @pytest.mark.asyncio
    async def test_get_fear_greed_comparison(self):
        """Test get_fear_greed_comparison tool."""
        result = await call_tool("get_fear_greed_comparison", {})
        assert len(result) == 1
        assert "Previous Close" in result[0].text
        assert "1 Week Ago" in result[0].text

    @pytest.mark.asyncio
    async def test_get_trading_signal(self):
        """Test get_trading_signal tool."""
        result = await call_tool("get_trading_signal", {})
        assert len(result) == 1
        assert "Trading Signal:" in result[0].text

        valid_signals = ["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"]
        assert any(signal in result[0].text for signal in valid_signals)

    @pytest.mark.asyncio
    async def test_get_fear_greed_history(self):
        """Test get_fear_greed_history tool."""
        result = await call_tool("get_fear_greed_history", {"days": 5})
        assert len(result) == 1
        assert "History" in result[0].text

    @pytest.mark.asyncio
    async def test_get_fear_greed_history_default(self):
        """Test get_fear_greed_history with default days."""
        result = await call_tool("get_fear_greed_history", {})
        assert len(result) == 1
        assert "Last 10 Days" in result[0].text

    @pytest.mark.asyncio
    async def test_get_complete_report(self):
        """Test get_complete_report tool."""
        result = await call_tool("get_complete_report", {})
        assert len(result) == 1
        assert len(result[0].text) > 200

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        """Test handling of unknown tool."""
        result = await call_tool("unknown_tool_name", {})
        assert len(result) == 1
        assert "Unknown tool" in result[0].text
