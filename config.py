import os
import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    sys.exit("ভুল: .env ফাইলে BOT_TOKEN পাওয়া যায়নি!")

try:
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
except ValueError:
    sys.exit("ভুল: OWNER_ID একটি সঠিক নিউমেরিক আইডি হতে হবে!")

ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "DefaultSecret@2026")
DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "nirvoy_guard.db")
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "bn")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SESSION_EXPIRY_MINUTES = 30
MAX_WARNS_DEFAULT = 3

# AI কনফিগারেশন
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
GEMINI_AUTO_MODEL = os.getenv("GEMINI_AUTO_MODEL", "true").strip().lower() in {"1", "true", "yes", "on"}