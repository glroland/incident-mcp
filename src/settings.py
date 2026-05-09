from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="INCIDENT_MCP_",
        extra="ignore",
    )

    # Server
    host: str = Field(default="0.0.0.0", description="Bind host for the MCP server")
    port: int = Field(default=8080, description="Bind port for the MCP server")
    transport: Literal["streamable-http", "sse", "http"] = Field(
        default="streamable-http", description="MCP transport protocol"
    )
    log_level: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")

    # ServiceNow
    snow_instance: str = Field(description="ServiceNow instance name (e.g. myinstance)")
    snow_username: str = Field(description="ServiceNow username for basic auth")
    snow_password: str = Field(description="ServiceNow password for basic auth")
    api_timeout: int = Field(default=30, description="HTTP timeout in seconds for API calls")

    @property
    def api_url(self) -> str:
        return f"https://{self.snow_instance}.service-now.com"


settings = Settings()
