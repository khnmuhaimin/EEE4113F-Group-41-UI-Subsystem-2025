from enum import Enum, auto
import os

from dotenv import load_dotenv
load_dotenv()

class Environment(Enum):
    DEVELOPMENT = auto()
    DEMO = auto()

    def __str__(self):
        return self.name
    
    @classmethod
    def parse(cls, string: str):
        try:
            return cls[string.upper()]
        except KeyError:
            raise ValueError(f"Invalid environment: {string}")


class Config:

    ENVIRONMENT = Environment.parse(os.environ["ENVIRONMENT"])
    SERVER_PORT = int(os.environ["SERVER_PORT"])
    UI_PORT = int(os.environ["UI_PORT"])
    REVERSE_PROXY_PORT = int(os.environ["REVERSE_PROXY_PORT"])
    PRESHARED_KEY = os.environ["PRESHARED_KEY"]
    ADMIN_NAME = os.environ["ADMIN_NAME"]
    ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
    USE_CUSTOM_SUBDOMAIN = os.environ["USE_CUSTOM_SUBDOMAIN"] == "TRUE"
    SUBDOMAIN = os.environ["SUBDOMAIN"]
    BASE_URL=f'https://{SUBDOMAIN}'
    DATABASE_PATH = os.environ["DATABASE_PATH"]

        
