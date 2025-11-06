from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    DB_URL: str = os.getenv("DB_URL", "sqlite:///piggyback_insider_trading.db")
    SEC_USER_AGENT: str = os.getenv("SEC_USER_AGENT", "CHANGE_ME you@example.com")
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

HEADERS = {
    "User-Agent": settings.SEC_USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.sec.gov",
}
