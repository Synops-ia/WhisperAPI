from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    openai_api_key: str

    model_config = SettingsConfigDict(env_file=find_dotenv())

settings = Settings()
