from enum import Enum, auto


class Environment(Enum):
    DEVELOPMENT = auto()
    DEMO = auto()

    def __str__(self):
        return self.name


class Config:

    ENVIRONMENT: Environment | None = None
    PORT: int | None = None
    PRESHARED_KEY: str | None = None
    ADMIN_NAME: str | None = None
    ADMIN_EMAIL: str | None = None
    ADMIN_PASSWORD: str | None = None
    USE_CUSTOM_SUBDOMAIN: bool | None = None
    SUBDOMAIN: str | None = None
    DATABASE_PATH: str | None = None

    @classmethod
    def get(cls, config_option: str) -> str | None:
        return getattr(cls, config_option)

    @classmethod
    def useConfig(cls, env: Environment):
        cls.ENVIRONMENT = env
        cls.PORT = 8000
        cls.PRESHARED_KEY = "PRESHARED_KEY"
        cls.ADMIN_NAME="admin"
        cls.ADMIN_EMAIL="admin@org.com"
        cls.ADMIN_PASSWORD="admin"

        if env == Environment.DEVELOPMENT:
            cls.USE_CUSTOM_SUBDOMAIN = False
            cls.SUBDOMAIN = None
            cls.DATABASE_PATH = ":memory:"
        
        elif env == Environment.DEMO:
            cls.USE_CUSTOM_SUBDOMAIN = True
            cls.SUBDOMAIN = "eee4113f-group-41-penguin-weighing"
            cls.DATABASE_PATH = "database.sqlite"