import os
from dotenv import load_dotenv

from config import Config, Environment

def print_config():
    load_dotenv()
    environment = os.getenv("ENVIRONMENT")
    if environment is None:
        raise Exception("Could not find the definition for ENVIRONMENT.")
    environment = environment.upper()
    if environment not in Environment.values():
        raise Exception(f"ENVIRONMENT must be defined as one of: {Environment.values()}.")
    
    Config.useConfig(Environment[environment])
    print(Config.dotenv_format())


if __name__ == "__main__":
    print_config()