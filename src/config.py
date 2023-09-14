from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'postgresql://postgres:postgres@localhost:5432/substation_planning'

    class Config:
        env_file = ".env"
