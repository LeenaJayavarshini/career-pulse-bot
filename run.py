from app.scraper import fetch_jobs
from app.storage import load_jobs, save_jobs, get_new_jobs
from app.notifier import send_message
from app.subscribers import check_new_subscribers

def run():
    old_jobs = load_jobs()
    check_new_subscribers()
    jobs = fetch_jobs(pages=2)
    print("Total jobs fetched:", len(jobs))

    new_jobs = get_new_jobs(old_jobs, jobs)
    print("New jobs (not seen before):", len(new_jobs))

    for job in new_jobs:
        send_message(job)

    save_jobs(old_jobs + new_jobs)

if __name__ == "__main__":
    run()