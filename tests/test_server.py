import pytest
from fastmcp import Client
from src.server import mcp


@pytest.fixture
def client():
    return Client(mcp)


@pytest.mark.asyncio
async def test_server_lists_tools(client):
    async with client:
        tools = await client.list_tools()
        tool_names = {t.name for t in tools}

    assert "search" in tool_names
    assert "get_incident" in tool_names
    assert "update_incident" in tool_names
    assert "add_timeline_entry" in tool_names
