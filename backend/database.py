import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic_settings import BaseSettings, SettingsConfigDict
from routers.profile import Profile
from pathlib import Path


class MyConfig(BaseSettings):
    connect_string: str
    # hardcoding the env file path to the root because it keeps giving errors
    env_file: Path = str(Path(__file__).parent.parent / ".env")
    print(env_file)
    model_config = SettingsConfigDict(env_file=env_file)

async def initialize_database():
    setting = MyConfig()
    client = AsyncIOMotorClient(setting.connect_string)
    await init_beanie(database=client["clash_of_colonies"], document_models=[Profile])


