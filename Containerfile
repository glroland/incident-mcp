FROM python:3.13-slim

RUN useradd --create-home app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

USER app

# Server
ENV INCIDENT_MCP_HOST=0.0.0.0
ENV INCIDENT_MCP_PORT=8080
ENV INCIDENT_MCP_TRANSPORT=streamable-http
ENV INCIDENT_MCP_LOG_LEVEL=INFO

# ServiceNow — required, must be overridden at runtime
ENV INCIDENT_MCP_SNOW_INSTANCE=""
ENV INCIDENT_MCP_SNOW_USERNAME=""
ENV INCIDENT_MCP_SNOW_PASSWORD=""
ENV INCIDENT_MCP_API_TIMEOUT=30

EXPOSE 8080

WORKDIR /app/src
CMD ["python", "-m", "server"]
