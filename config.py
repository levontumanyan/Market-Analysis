from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project paths
ROOT_DIR = Path(__file__).parent
CONFIG_DIR = ROOT_DIR / "benchmarks"
SECTORS_PATH = CONFIG_DIR / "sectors.json"
CACHE_DIR = ROOT_DIR / "cache" / "openbb"
PROFILES_PATH = ROOT_DIR / "profiles" / "investor_profiles.json"
