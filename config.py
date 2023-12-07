from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = "root"
DB_HOST = getenv("DB_HOST")
BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")

CLOUD_NAME = getenv("CLOUD_NAME")
API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")