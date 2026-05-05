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
    log_level: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")

    # Incident management system
    api_url: str = Field(description="Base URL of the incident management API")
    api_key: str = Field(description="API key for authenticating with the incident management API")
    api_timeout: int = Field(default=30, description="HTTP timeout in seconds for API calls")


settings = Settings()
