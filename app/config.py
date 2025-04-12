from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "fastapi_db"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
