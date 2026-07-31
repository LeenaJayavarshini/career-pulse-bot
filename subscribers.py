import json
import os
import requests
from app.config import BOT_TOKEN

SUB_FILE = "data/subscribers.json"

def load_subscribers():
    if not os.path.exists(SUB_FILE):
        return []
    try:
        with open(SUB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_subscribers(subs):
    os.makedirs("data", exist_ok=True)
    with open(SUB_FILE, "w") as f:
        json.dump(subs, f, indent=2)

def welcome_message(chat_id, name):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    text = f"Hi {name}! You're now subscribed to CareerPulse. You'll get a message here whenever a new fresher job is posted."
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

def check_new_subscribers():
    subs = load_subscribers()
    known_ids = {s["chat_id"] for s in subs}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    data = response.json()

    for update in data.get("result", []):
        message = update.get("message", {})
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        name = chat.get("first_name", "there")

        if chat_id and chat_id not in known_ids:
            subs.append({"chat_id": chat_id, "name": name})
            known_ids.add(chat_id)
            print(f"New subscriber added: {name} ({chat_id})")
            welcome_message(chat_id, name)

    save_subscribers(subs)
    return subs