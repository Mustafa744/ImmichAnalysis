from dotenv import load_dotenv
import os
from pathlib import Path

# Load from .env file at the project root
ROOT_DIR = Path(__file__).resolve().parents[4]
load_dotenv(dotenv_path=ROOT_DIR / ".env")

IMMICH_URL = os.getenv("IMMICH_URL")
API_KEY = os.getenv("IMMICH_API_KEY")
DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Shared Paths
DATA_DIR = ROOT_DIR / "data"
PHOTOS_CSV = DATA_DIR / "photos.csv"
CACHE_PATH = DATA_DIR / "thumbnails_analysis.json"

# General App Settings
MAX_WORKERS = 8
