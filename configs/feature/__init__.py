
from pydantic import (
    AliasChoices, Field, PositiveInt, computed_field,
)
from pydantic_settings import BaseSettings

class LoggingConfig(BaseSettings):
    """
    Configuration for application logging
    """

    LOG_LEVEL: str = Field(
        description="Logging level, default to INFO. Set to ERROR for production environments.",
        default="INFO",
    )

    LOG_FILE: str | None = Field(
        description="File path for log output.",
        default=None,
    )

    LOG_FILE_MAX_SIZE: PositiveInt = Field(
        description="Maximum file size for file rotation retention, the unit is megabytes (MB)",
        default=20,
    )

    LOG_FILE_BACKUP_COUNT: PositiveInt = Field(
        description="Maximum file backup count file rotation retention",
        default=5,
    )

    LOG_FORMAT: str = Field(
        description="Format string for log messages",
        default=(
            "%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] "
            "[%(filename)s:%(lineno)d] %(trace_id)s - %(message)s"
        ),
    )

    LOG_DATEFORMAT: str | None = Field(
        description="Date format string for log timestamps",
        default=None,
    )

    LOG_TZ: str | None = Field(
        description="Timezone for log timestamps (e.g., 'America/New_York')",
        default="UTC",
    )

class HttpConfig(BaseSettings):
    """
    HTTP-related configurations for the application
    """

    inner_CONSOLE_CORS_ALLOW_ORIGINS: str = Field(
        description="Comma-separated list of allowed origins for CORS in the console",
        validation_alias=AliasChoices("CONSOLE_CORS_ALLOW_ORIGINS", "CONSOLE_WEB_URL"),
        default="",
    )

    @computed_field
    def CONSOLE_CORS_ALLOW_ORIGINS(self) -> list[str]:
        return self.inner_CONSOLE_CORS_ALLOW_ORIGINS.split(",")

class SwaggerUIConfig(BaseSettings):
    SWAGGER_UI_ENABLED: bool = Field(
        description="Whether to enable Swagger UI in api module",
        default=True,
    )

    SWAGGER_UI_PATH: str = Field(
        description="Swagger UI page path in api module",
        default="/swagger-ui.html",
    )

class FeatureConfig(
    LoggingConfig,
    SwaggerUIConfig,
    HttpConfig,
):
    pass
