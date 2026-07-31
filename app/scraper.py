import requests
import time
from bs4 import BeautifulSoup
from app.config import URL


def safe_get(url, headers=None, retries=3, delay=5, timeout=10):
    for attempt in range(1, retries + 1):
        try:
            return requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed for {url}: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise


def fetch_jobs(pages=2):
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://www.fresheroffcampus.com"
    jobs = []
    for page in range(1, pages + 1):
        url = f"{base_url}/page/{page}/" if page > 1 else base_url
        res = safe_get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        # This is the MOST reliable selector
        for post in soup.select("h2.entry-title a, h1.entry-title a"):
            title = post.get_text(strip=True)
            link = post["href"]
            jobs.append({
                "title": title,
                "link": link
            })
    return jobs


def get_job_date(link):
    from datetime import datetime
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = safe_get(link, headers=headers, retries=2, delay=3, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        time_tag = soup.select_one("time.ct-meta-element-date")
        if time_tag and time_tag.get("datetime"):
            return datetime.fromisoformat(time_tag["datetime"]).date()
    except requests.exceptions.Timeout:
        print("Timeout:", link)
    except Exception as e:
        print("Error:", link)
    return None
