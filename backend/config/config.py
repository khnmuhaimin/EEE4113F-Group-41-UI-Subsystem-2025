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
    DOMAIN=os.environ["DOMAIN"]
    PRESHARED_KEY = os.environ["PRESHARED_KEY"]
    ADMIN_NAME = os.environ["ADMIN_NAME"]
    ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
    BASE_URL=f'https://{DOMAIN}'
    DATABASE_PATH = os.environ["DATABASE_PATH"]

        
