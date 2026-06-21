import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
SERVERS = [
    "v2tetotech.onrender.com"
]

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
TIMEOUT = 30.0
MAX_RETRIES = 3
