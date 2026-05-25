import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASE_NAME = os.getenv("DATABASE_NAME")

DB_PASSWORD = os.getenv("DB_PASSWORD")