# AI Job Discovery Agent

This agent automates the process of finding jobs, summarizing them using Azure OpenAI, and emailing a professional report.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file (see example in project) with:
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_DEPLOYMENT` (e.g., `gpt-4o-mini`)
   - `EMAIL_USER` (your Gmail)
   - `EMAIL_PASSWORD` (App password)
   - `EMAIL_RECEIVER`

## Usage

Run the agent with custom job titles, locations, and sources:

```bash
python src/main.py --query "Supply Chain Analyst" --location "Texas" --source "indeed" --limit 10
```

### Options:

- `--query`: Job title or keywords (default: "Supply Chain Analyst")
- `--location`: Location (default: "Texas, United States")
- `--source`: Source of jobs. Use "indeed" for Indeed-specific results or "google" for general results. (default: "indeed")
- `--limit`: Number of jobs to include in the report (default: 10)

## Project Structure

- `src/main.py`: Entry point and orchestration logic.
- `src/job_scraper.py`: Handles job fetching (scrapes Google Search).
- `src/ai_generator.py`: Generates the HTML report using Azure OpenAI.
- `src/email_sender.py`: Sends the report via SMTP.
