from pydantic import BaseModel
from pydantic_settings import BaseSettings


class StartConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class Settings(BaseSettings):
    run: StartConfig = StartConfig()
    host: str
    port: int
    db_url: str


settings = Settings()
