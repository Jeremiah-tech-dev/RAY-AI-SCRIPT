*🚀 Job Outreach Automation — RAY Case Study*
🔎 Overview

Job Outreach Automation is a Python-based automation pipeline that discovers Executive Assistant and Administrative Assistant job postings, validates them against defined criteria, generates personalized outreach messages using an AI model, and stores results for operational use.

The system reduces manual job discovery and message drafting by automatically collecting relevant job opportunities and generating tailored outreach messages ready for immediate submission.

⚡ Key Features

✅ Automated job discovery using the Remotive job board API

✅ Job validation based on role relevance, language, and remote criteria

✅ AI-generated personalized outreach messages using Cloudflare Llama 3.1 8B

✅ Structured CSV export for reporting and tracking

✅ Google Sheets integration for collaborative workflows

✅ Scheduled automation for daily execution

✅ Robust error handling and retry logic

🏗 System Architecture

The automation pipeline follows a sequential processing flow:

scrape_jobs()
      ↓
validate_job()
      ↓
generate_outreach_message()
      ↓
save_to_csv()
      ↓
save_to_google_sheets()

Each stage performs a dedicated responsibility to maintain data quality, reliability, and automation efficiency.

📁 Project Structure
RAY-AI-SCRIPT/
│
├── job_outreach_automation.py
├── README.md
├── job_outreach_results.csv
├── credentials.json
├── .env
└── requirements.txt
File Descriptions

job_outreach_automation.py
Primary automation script containing scraping, validation, AI message generation, and export logic.

.env
Stores environment variables used for secure API authentication.

credentials.json
Google OAuth configuration for Google Sheets access.

job_outreach_results.csv
Generated dataset containing discovered jobs and AI-generated outreach messages.

⚙ Installation
1️⃣ Install Dependencies

Navigate to the project directory and install dependencies:

cd RAY-AI-SCRIPT
pip install requests beautifulsoup4 gspread google-auth google-auth-oauthlib google-auth-httplib2 schedule python-dotenv

Or install using the virtual environment:

./venv/bin/pip install -r requirements.txt
🔐 Configuration
Cloudflare AI Setup

Create an API token and configure environment variables.

.env

CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_API_TOKEN=your-api-token

API tokens can be generated from the Cloudflare dashboard.

Google Sheets Setup

Open Google Cloud Console

Enable:

Google Sheets API

Google Drive API

Create OAuth credentials (Desktop App)

Download the file as credentials.json

Add your email as a test user in the OAuth consent screen

Create a Google Sheet named Job Outreach Tracker

▶ Running the Automation
Run Once

Execute the script manually:

./venv/bin/python job_outreach_automation.py
Enable Scheduled Automation

Inside the script, enable the scheduler:

start_scheduler()

This allows the pipeline to run automatically on a daily schedule.

🛠 Customization
Adjust AI Outreach Tone

Modify the AI prompt template:

OUTREACH_PROMPT_TEMPLATE

This allows testing different outreach styles and tones.

Modify Job Validation Rules

Filtering logic can be adjusted using keyword lists:

REMOTE_KEYWORDS

ENGLISH_KEYWORDS

ROLE_KEYWORDS

These filters ensure only relevant job postings are processed.

📊 Output
CSV Export

job_outreach_results.csv includes:

Job Posting URL

Job Title

Company Name

Location

Job Description

AI-generated Outreach Message

Google Sheets Dashboard

Data is also pushed to Google Sheets so teams can:

Review discovered job opportunities

Track outreach progress

Collaborate on job applications

🧰 Troubleshooting
Google Sheets OAuth Error

Add your email as a test user:

Open Google Cloud Console

Navigate to OAuth Consent Screen

Add your email under Test Users

No Jobs Found

Possible causes:

Job board API unavailable

Internet connection issues

Job category mismatch

Cloudflare API Errors

Verify:

API token validity

Correct account ID

Workers AI access enabled

🧑‍💻 Technologies Used

Python

REST APIs

Cloudflare Workers AI

Google Sheets API

Automation scheduling

Environment-based configuration

🎯 Use Case

This automation pipeline reduces manual job discovery and message drafting, enabling faster, scalable outreach workflows for job applications and opportunity tracking.
