from src.job_scraper import fetch_jobs

queries = ["Supply chain analyst", "Procurement analyst"]
location = "Texas, United States"

all_jobs = []
for q in queries:
    print(f"Searching for {q}...")
    jobs = fetch_jobs(q, location)
    print(f"Found {len(jobs)} jobs for {q}")
    all_jobs.extend(jobs)

for job in all_jobs[:5]:
    print(f"Title: {job['title']}")
    print(f"Link: {job.get('link')}")
    print("-" * 20)
