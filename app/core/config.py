from pathlib import Path
from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseConfig(BaseModel):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )


class CorsConfig(BaseModel):
    allowed_origins: list[str]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_nested_delimiter="__",
    )

    db: DataBaseConfig
    cors: CorsConfig


settings = Settings()
