import argparse
import sys
from datetime import datetime
from dotenv import load_dotenv

from job_scraper import fetch_jobs
from ai_generator import generate_job_report
from email_sender import send_job_email

def main():
    # Load environment variables (API keys, email configs)
    load_dotenv()

    # Parse command-line arguments for specific search parameters
    parser = argparse.ArgumentParser(description="AI Job Discovery Agent (LinkedIn Only)")
    parser.add_argument("--query", type=str, default="Supply Chain Analyst", help="Job title to search for (e.g., 'Procurement Analyst')")
    parser.add_argument("--location", type=str, default="Texas, United States", help="Location (e.g., 'Dallas, TX')")
    parser.add_argument("--time", type=str, default="24h", help="Time period filter: '24h' for last 24 hours (default)")
    parser.add_argument("--limit", type=int, default=10, help="Max number of jobs to process")
    args = parser.parse_args()

    print(f"--- AI LinkedIn Discovery Search ---")
    print(f"Keywords: {args.query}")
    print(f"Location: {args.location}")
    print(f"Time    : {args.time if args.time else 'Any'}")
    print(f"Limit   : {args.limit}")
    print(f"--------------------------------------")

    # 1. Fetch LinkedIn Jobs (Guest Mode)
    print(f"Scraping LinkedIn for '{args.query}' in '{args.location}'...")
    jobs = fetch_jobs(args.query, args.location, time_period=args.time)

    if not jobs:
        print("No LinkedIn listings found. LinkedIn may be guest-restricted or rate-limited.")
        return

    # Limit the number of jobs sent for AI processing
    jobs = jobs[:args.limit]
    print(f"Processing {len(jobs)} LinkedIn roles. Generating AI report...")

    # 2. Generate Professional AI Report
    report_html = generate_job_report(jobs)
    
    if not report_html:
        print("AI generation failed. Exiting.")
        return

    # 3. Deliver via Email
    success = send_job_email(report_html)
    
    if success:
        print("Done! Check your email for the discovery report.")
    else:
        print("Email delivery failed.")

if __name__ == "__main__":
    main()