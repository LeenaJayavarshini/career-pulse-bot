import requests
from app.config import BOT_TOKEN
from app.subscribers import load_subscribers

def send_message(job):
    msg = f"""New Job!
{job['title']}
{job['link']}
"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    subs = load_subscribers()
    for sub in subs:
        requests.post(url, json={
            "chat_id": sub["chat_id"],
            "text": msg
        })