
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource
)

from libs.file_utils import search_file_upwards

from .middleware import MiddlewareConfig
from .feature import FeatureConfig
from .deploy import DeploymentConfig

class AppConfig(
    DeploymentConfig,
    MiddlewareConfig,
    FeatureConfig
):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        # ignore extra attributes
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,  # init in hand
        env_settings: PydanticBaseSettingsSource,  # from os.environ
        dotenv_settings: PydanticBaseSettingsSource,  # from model_config.env_file
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(
                settings_cls=settings_cls,
                toml_file=search_file_upwards(
                    base_dir_path=Path(__file__).parent,
                    target_file_name="pyproject.toml",
                    max_search_parent_depth=2,
                ),
            )
        )
