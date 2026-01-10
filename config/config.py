from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class LogSettings:
    level: str
    format: str

@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: str
    user: str
    password: str

@dataclass
class Config:
    bot: TgBot
    log: LogSettings
    db: DatabaseSettings
    ai: str
    channel_id: str

def load_config(path: str | None = None):
    env = Env()
    env.read_env()

    token = env('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN must not be empty")
    
    db = DatabaseSettings(
        name=env("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
    )

    return Config(
        bot=TgBot(token=token),
        log=LogSettings(
            level=env('LOG_LEVEL'),
            format=env('LOG_FORMAT')
        ),
        db=db,
        ai=env('DEEPSEEK_API_KEY'),
        channel_id=env('CHANNEL_ID')
    )