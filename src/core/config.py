from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn
    algorithm: str
    access_token_expire_minutes: int
    secret_key: str
    project_host: str
    project_port: int


    model_config = SettingsConfigDict(env_file=".env")



app_setting = Settings()