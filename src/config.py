import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
POLICIES_DIR = DATA_DIR / "policies"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# File paths
CSV_PATH = DATA_DIR / "employees.csv"
DB_PATH = DATA_DIR / "hr_database.db"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
