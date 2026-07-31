import requests
from bs4 import BeautifulSoup
from app.config import URL

import requests
from bs4 import BeautifulSoup

def fetch_jobs(pages=2):
    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://www.fresheroffcampus.com"

    jobs = []

    for page in range(1, pages + 1):
        url = f"{base_url}/page/{page}/" if page > 1 else base_url

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ This is the MOST reliable selector
        for post in soup.select("h2.entry-title a, h1.entry-title a"):
            title = post.get_text(strip=True)
            link = post["href"]

            jobs.append({
                "title": title,
                "link": link
            })

    return jobs

def get_job_date(link):
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(link, headers=headers, timeout=(3, 3))  # 🔥 connect + read timeout
        soup = BeautifulSoup(res.text, "html.parser")

        time_tag = soup.select_one("time.ct-meta-element-date")

        if time_tag and time_tag.get("datetime"):
            return datetime.fromisoformat(time_tag["datetime"]).date()

    except requests.exceptions.Timeout:
        print("Timeout:", link)
    except Exception as e:
        print("Error:", link)

    return None