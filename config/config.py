import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

API_TOKEN = os.getenv("TMDB_API_TOKEN")