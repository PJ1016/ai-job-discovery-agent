import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_job_report(jobs):
    """
    Generates a professional HTML job discovery report using Azure OpenAI.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not api_key or not endpoint or not deployment:
        print("Error: Azure OpenAI configuration missing in .env")
        return None

    client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
        timeout=30
    )

    today = datetime.now().strftime("%B %d, %Y")
    
    jobs_text = ""
    for i, job in enumerate(jobs, start=1):
        jobs_text += f"""
{i}. {job['title']} at {job['company']}
Location: {job['location']}
Match Score: {job.get('match_score', 80)}
Apply: {job.get('link', 'N/A')}
"""

    try:
        response = client.chat.completions.create(
            model=deployment,
            temperature=0.4,
            max_tokens=1200,
            messages=[
                {
                    "role": "system",
                    "content": f"""
You generate daily job discovery email reports.
Today's date is {today}.
Return ONLY valid HTML.
Requirements:
- Professional layout with a modern design
- Include a header with the title "Daily AI Job Discovery Report"
- Include a summary section
- Include a clear table of jobs with links
- Use clean CSS inside a <style> tag
- Output must start with <!DOCTYPE html>
"""
                },
                {
                    "role": "user",
                    "content": f"""
Generate a professional HTML job discovery report for the following jobs:

{jobs_text}

Statistics:
Jobs scanned: {len(jobs)}
Relevant jobs: {len(jobs)}
"""
                }
            ]
        )

        report = response.choices[0].message.content
        return report

    except Exception as e:
        print(f"AI generation failed: {e}")
        return None
