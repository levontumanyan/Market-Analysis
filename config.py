from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project paths
ROOT_DIR = Path(__file__).parent
BENCHMARKS_PATH = ROOT_DIR / "benchmarks.json"
CACHE_DIR = ROOT_DIR / "cache" / "yfinance"
PROFILES_PATH = ROOT_DIR / "profiles.json"
