import json
import os

DATA_FILE = "data/jobs.json"

def load_jobs():
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_jobs(jobs):
    # ✅ ensure folder exists
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

    print("✅ Saved jobs:", len(jobs))  # DEBUG

def get_new_jobs(old, new):
    old_set = {(j["title"], j["link"]) for j in old}
    return [j for j in new if (j["title"], j["link"]) not in old_set]