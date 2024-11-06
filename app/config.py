from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_uri: str
    redis_server: str
    redis_port: int
    client_id: str
    client_secret: str
    jwt_secret_key: str
    root_path: str = ""
    logging_level: str = "INFO"
    testing: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()