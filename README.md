# incident-mcp

An MCP (Model Context Protocol) service for interacting with a ServiceNow incident management system. Built with [FastMCP](https://github.com/jlowin/fastmcp) and served over streamable HTTP.

## Tools

| Tool | Description |
|---|---|
| `search` | Search incidents by hostname, date range, or both |
| `get_incident` | Retrieve a single incident by number, including its full timeline |
| `add_timeline_entry` | Append a work note to an incident's timeline |

## Requirements

- Python 3.11+
- A ServiceNow instance with API access

## Setup

1. Create and activate a virtual environment, then install dependencies:

```bash
make install
```

2. Copy `.env.example` to `.env` and fill in your ServiceNow credentials:

```bash
cp .env.example .env
```

```ini
INCIDENT_MCP_API_URL=https://myinstance.service-now.com
INCIDENT_MCP_API_USERNAME=svc_mcp_user
INCIDENT_MCP_API_PASSWORD=your-password-here
```

## Running

```bash
make run
```

The server binds to `0.0.0.0:8080` by default and speaks the MCP streamable HTTP protocol. Override host and port via environment variables:

```ini
INCIDENT_MCP_HOST=127.0.0.1
INCIDENT_MCP_PORT=9090
```

## Configuration

All configuration is via environment variables (or `.env`). Every variable is prefixed `INCIDENT_MCP_`.

| Variable | Default | Required | Description |
|---|---|---|---|
| `INCIDENT_MCP_API_URL` | — | yes | ServiceNow instance base URL |
| `INCIDENT_MCP_API_USERNAME` | — | yes | ServiceNow username |
| `INCIDENT_MCP_API_PASSWORD` | — | yes | ServiceNow password |
| `INCIDENT_MCP_API_TIMEOUT` | `30` | no | HTTP timeout in seconds |
| `INCIDENT_MCP_HOST` | `0.0.0.0` | no | Server bind host |
| `INCIDENT_MCP_PORT` | `8080` | no | Server bind port |
| `INCIDENT_MCP_LOG_LEVEL` | `INFO` | no | Log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

## Project Structure

```
src/
├── server.py          # FastMCP server entry point
├── settings.py        # Pydantic settings (env / .env)
├── logger.py          # Logging configuration
├── models.py          # Pydantic models (Incident, TimelineEntry)
├── servicenow.py      # Shared ServiceNow HTTP client and field mappings
└── tools/
    ├── search.py
    ├── get_incident.py
    └── add_timeline_entry.py

tests/
├── test_server.py
└── tools/
    ├── test_search.py
    ├── test_get_incident.py
    └── test_add_timeline_entry.py
```

## Development

```bash
make test      # run tests
make lint      # ruff check
make format    # ruff format + fix
```
