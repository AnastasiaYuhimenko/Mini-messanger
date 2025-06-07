from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    HOST: str
    PORT: str
    RELOAD: bool

    class Config:
        env_file = ".env"


settings = Settings()
