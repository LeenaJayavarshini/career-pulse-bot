import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.fresheroffcampus.com/"

DATA_FILE = "data/jobs.json"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")