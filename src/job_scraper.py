import requests
from bs4 import BeautifulSoup

def fetch_jobs(query="Supply Chain Analyst", location="Texas, United States", time_period="24h"):
    """
    Fetches job listings from LinkedIn (Non-logged in guest search).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    jobs = []
    
    # Direct LinkedIn Search (Non-logged in)
    search_query = query.replace(" ", "%20")
    search_location = location.replace(" ", "%20")
    
    # f_TPR=r86400 is the LinkedIn filter for last 24 hours (86400 seconds)
    url = f"https://www.linkedin.com/jobs/search?keywords={search_query}&location={search_location}"
    
    if time_period == "24h":
        url += "&f_TPR=r86400"
        
    try:
        print(f"Searching LinkedIn (Guest Access): {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # LinkedIn Guest Search Card Selectors
        job_cards = soup.select("div.base-card")
        
        if not job_cards:
            print("No job cards found. LinkedIn might be rate-limiting or requiring a login.")
            return []

        for result in job_cards:
            title_tag = result.select_one("h3.base-search-card__title")
            company_tag = result.select_one("h4.base-search-card__subtitle")
            location_tag = result.select_one("span.job-search-card__location")
            link_tag = result.select_one("a.base-card__full-link")
            
            if title_tag and link_tag:
                jobs.append({
                    "title": title_tag.text.strip(),
                    "company": company_tag.text.strip() if company_tag else "N/A",
                    "location": location_tag.text.strip() if location_tag else location,
                    "link": link_tag['href'].split('?')[0],
                    "match_score": 98
                })
                
        print(f"Successfully retrieved {len(jobs)} LinkedIn roles.")
        
    except Exception as e:
        print(f"LinkedIn Fetch Error: {e}")

    return jobs