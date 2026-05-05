import uvicorn
from fastmcp import FastMCP

from logger import configure_logging
from settings import settings
from tools.add_timeline_entry import add_timeline_entry
from tools.get_incident import get_incident
from tools.search import search

mcp = FastMCP("Incident Management", instructions="Tools for interacting with the incident management system.")

mcp.tool()(search)
mcp.tool()(get_incident)
mcp.tool()(add_timeline_entry)


def main() -> None:
    configure_logging()
    app = mcp.http_app(transport="streamable-http")
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
