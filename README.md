# Job Outreach Automation - RAY Case Study

## Overview
Automated pipeline that discovers Executive Assistant and Admin Assistant job postings, validates them based on criteria, generates personalized outreach messages using AI, and saves results to CSV and Google Sheets.

## Features
- ✅ Web scraping from Remotive job board (API-based, reliable)
- ✅ Automatic job validation (remote, English, role relevance)
- ✅ AI-powered personalized outreach messages (Cloudflare Llama 3.1 8B)
- ✅ CSV export with all job details
- ✅ Google Sheets integration for sales team dashboard
- ✅ Daily automation scheduling
- ✅ Comprehensive error handling

## Installation

### 1. Install Dependencies
```bash
cd RAY-AI-SCRIPT
pip install requests beautifulsoup4 gspread google-auth google-auth-oauthlib google-auth-httplib2 schedule python-dotenv
```

Or use the virtual environment:
```bash
./venv/bin/pip install -r requirements.txt
```

### 2. Configure Cloudflare AI
Edit `.env` file:
```
CLOUDFLARE_ACCOUNT_ID=9f3fe533797c89e316271830e6bcb1f9
CLOUDFLARE_API_TOKEN=your-token-here
```

Get your token at: https://dash.cloudflare.com/profile/api-tokens

### 3. Configure Google Sheets
1. Go to https://console.cloud.google.com/
2. Enable Google Sheets API and Google Drive API
3. Create OAuth credentials (Desktop app)
4. Download as `credentials.json`
5. Add yourself as test user in OAuth consent screen
6. Create a Google Sheet named "Job Outreach Tracker"

## Usage

### Run Once
```bash
./venv/bin/python job_outreach_automation.py
```

### Enable Daily Automation
Edit `job_outreach_automation.py` and uncomment:
```python
# start_scheduler()
```

## Configuration

### Change LLM Prompt
Edit `OUTREACH_PROMPT_TEMPLATE` at the top of the script to test different tones.

### Change Job Source
Edit `JOB_BOARD_URL` to use different job boards or categories.

### Adjust Validation Criteria
Modify keyword lists:
- `REMOTE_KEYWORDS`
- `ENGLISH_KEYWORDS`
- `ROLE_KEYWORDS`

## Output

### CSV File
`job_outreach_results.csv` contains:
- Job Posting URL
- Job Title
- Company Name
- Location
- Job Description
- LLM Generated Outreach Message

### Google Sheet
Same columns as CSV, accessible by sales team for quick application.

## Troubleshooting

### Google Sheets OAuth Error
Add your email as test user:
1. Go to https://console.cloud.google.com/apis/credentials/consent
2. Add test users
3. Run script again

### No Jobs Found
- Check if job board URL is accessible
- Verify internet connection
- Try different job category

### Cloudflare API Error
- Verify API token in `.env`
- Check account ID is correct
- Ensure Workers AI is enabled

## Architecture

```
scrape_jobs() → validate_job() → generate_outreach_message() → save_to_csv() + save_to_google_sheets()
```

## Files
- `job_outreach_automation.py` - Main script
- `.env` - API credentials
- `credentials.json` - Google OAuth config
- `job_outreach_results.csv` - Output data
- `README.md` - This file
