Job Outreach Automation — RAY Case Study
Overview

Job Outreach Automation is a Python-based automation pipeline that discovers Executive Assistant and Administrative Assistant job postings, validates them against defined criteria, generates personalized outreach messages using an AI model, and stores results for operational use.

The system was designed to streamline outbound job outreach by reducing manual discovery and message drafting. The pipeline automatically collects relevant job opportunities and generates tailored outreach messages ready for immediate use.

Key Features

Automated job discovery using the Remotive job board API

Job validation based on role relevance, language, and remote criteria

AI-generated personalized outreach messages using Cloudflare Llama 3.1 8B

Structured CSV export for reporting and data tracking

Google Sheets integration for collaborative workflows

Scheduled automation for daily execution

Robust error handling and retry logic

System Architecture

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

Each stage performs a specific responsibility to ensure data quality and maintain pipeline reliability.

Project Structure
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
Primary automation script containing scraping, validation, AI message generation, and data export logic.

.env
Environment variables used for API credentials and secure configuration.

credentials.json
OAuth configuration used for Google Sheets authentication.

job_outreach_results.csv
Structured export of discovered jobs and generated outreach messages.

Installation
1. Install Dependencies

Navigate to the project directory and install dependencies.

cd RAY-AI-SCRIPT
pip install requests beautifulsoup4 gspread google-auth google-auth-oauthlib google-auth-httplib2 schedule python-dotenv

Alternatively install using a virtual environment.

./venv/bin/pip install -r requirements.txt
Configuration
Cloudflare AI Setup

Create an API token and configure environment variables.

.env

CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_API_TOKEN=your-api-token

API tokens can be generated from the Cloudflare dashboard.

Google Sheets Setup

Open the Google Cloud Console

Enable:

Google Sheets API

Google Drive API

Create OAuth credentials (Desktop Application)

Download the credentials file as credentials.json

Add your email as a test user in the OAuth consent screen

Create a Google Sheet titled Job Outreach Tracker

Running the Automation
Run Once

Execute the script manually.

./venv/bin/python job_outreach_automation.py
Enable Scheduled Automation

Inside the script, enable the scheduler.

start_scheduler()

This allows the pipeline to run automatically at scheduled intervals.

Customization
Adjust AI Outreach Tone

Edit the prompt template used by the AI model.

OUTREACH_PROMPT_TEMPLATE

This allows customization of messaging tone and structure.

Modify Job Validation Rules

Job filtering logic can be adjusted by editing keyword lists:

REMOTE_KEYWORDS

ENGLISH_KEYWORDS

ROLE_KEYWORDS

These filters ensure only relevant jobs are processed.

Output
CSV Export

job_outreach_results.csv includes:

Job Posting URL

Job Title

Company Name

Location

Job Description

AI-generated Outreach Message

Google Sheets Dashboard

The same data is pushed to Google Sheets, allowing teams to:

review opportunities

track outreach

collaborate on job applications

Troubleshooting
Google Sheets OAuth Errors

Ensure your email is added as a test user in the OAuth consent configuration.

No Jobs Found

Possible causes:

Job board API unavailable

Network connectivity issues

Job category mismatch

Cloudflare API Errors

Verify the following:

API token validity

Correct account ID

Workers AI access enabled

Technologies Used

Python

REST APIs

Cloudflare Workers AI

Google Sheets API

Automation scheduling

Environment-based configuration

Use Case

This automation reduces manual job discovery and message drafting, enabling faster and more scalable outreach workflows for job applications or sales pipelines.
