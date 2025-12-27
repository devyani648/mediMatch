from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str = "postgresql://medimatch:medimatch@localhost:5432/medimatch"
    device: str = "cpu"
    upload_dir: str = str(Path.cwd() / "uploads")
    data_dir: str = str(Path.cwd() / "data")
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
