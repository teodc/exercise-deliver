import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.environ.get("APP_ENV")
APP_HOST = os.environ.get("APP_HOST")
APP_PORT = int(os.environ.get("APP_PORT"))

FRONTEND_URL = os.environ.get("FRONTEND_URL")
