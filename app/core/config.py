from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class StartConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DataBaseSettings(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: StartConfig = StartConfig()
    db: DataBaseSettings


settings = Settings()
