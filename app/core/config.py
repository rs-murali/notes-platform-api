"""
Configuration for the app. This module contains the configuration for the app
using pydantic settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    postgres_url : str = Field(default="", description="Postgres connection URL")