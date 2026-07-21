from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_DIR / 'ecommerce.db'}"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")