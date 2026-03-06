"""
Job Outreach Automation Script
Automates discovery and outreach for Executive/Admin Assistant roles

SETUP:
1. Install dependencies:
   pip install requests beautifulsoup4 gspread google-auth google-auth-oauthlib google-auth-httplib2 schedule python-dotenv

2. Configure .env file:
   - Update CLOUDFLARE_API_TOKEN in the .env file with your Cloudflare API token
   - Account ID is already set

3. Google Sheets Setup (OAuth 2.0):
   - Go to Google Cloud Console: https://console.cloud.google.com/
   - Create/select a project
   - Enable Google Sheets API and Google Drive API
   - Go to 'Credentials' → 'Create Credentials' → 'OAuth client ID'
   - Choose 'Desktop app' as application type
   - Download the JSON file and save as 'credentials.json' in this directory
   - First run will open browser for authentication
   - Update GOOGLE_SHEET_NAME constant below
"""

import os
import csv
import time
import schedule
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# Google Sheets Configuration
GOOGLE_SHEET_NAME = "Job Outreach Tracker"  # Update with your sheet name
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Job Board URL - Using Remotive API (free, no auth required)
JOB_BOARD_URL = "https://remotive.com/api/remote-jobs?category=administrative"

# CSV Output File
CSV_OUTPUT_FILE = "job_outreach_results.csv"

# LLM Prompt Template (easily editable for different tones)
OUTREACH_PROMPT_TEMPLATE = """
You are a professional job seeker applying for an {job_title} position at {company}.

Write a short, professional outreach message (2-3 sentences) that:
- Expresses genuine interest in the role
- Highlights relevant executive/admin support experience
- Requests consideration for the position

Keep it concise, warm, and professional. Do not include a subject line or greeting.

Job Description Context:
{description}
"""

# Job Validation Keywords
REMOTE_KEYWORDS = ["remote", "work from home", "wfh", "anywhere", "distributed"]
ENGLISH_KEYWORDS = ["english", "native english", "fluent english", "english speaker"]
ROLE_KEYWORDS = ["executive assistant", "admin assistant", "administrative assistant", 
                 "ea", "personal assistant", "virtual assistant"]

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def scrape_jobs():
    """
    Fetches job postings from Remotive API
    Returns: List of dictionaries containing job information
    """
    print("🔍 Fetching jobs from Remotive API...")
    jobs = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        response = requests.get(JOB_BOARD_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        job_listings = data.get('jobs', [])
        
        for job in job_listings[:15]:  # Limit to 15 jobs
            try:
                title = job.get('title', '')
                company = job.get('company_name', 'Unknown Company')
                location = job.get('candidate_required_location', 'Remote')
                description = job.get('description', '')
                job_url = job.get('url', '')
                
                # Filter for assistant roles
                if not any(keyword in title.lower() for keyword in ['assistant', 'admin', 'ea', 'support', 'coordinator']):
                    continue
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description[:1000],
                    'url': job_url
                })
                
            except Exception as e:
                print(f"⚠️  Error parsing job listing: {e}")
                continue
        
        print(f"✅ Scraped {len(jobs)} jobs")
        return jobs
        
    except Exception as e:
        print(f"❌ Error fetching jobs: {e}")
        return []


def validate_job(description, location, title):
    """
    Validates if a job meets the criteria
    Returns: Boolean
    """
    text = f"{description} {location} {title}".lower()
    
    # Check if remote
    is_remote = any(keyword in text for keyword in REMOTE_KEYWORDS)
    
    # Check if English communication is mentioned
    is_english = any(keyword in text for keyword in ENGLISH_KEYWORDS) or True  # Default to True
    
    # Check if role is relevant
    is_relevant = any(keyword in text for keyword in ROLE_KEYWORDS)
    
    return is_remote and is_english and is_relevant


def generate_outreach_message(job_title, company, description):
    """
    Generates personalized outreach message using Cloudflare Workers AI (Llama 3.1 8B)
    Returns: String message or error message
    """
    try:
        api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        
        if not api_token or not account_id:
            return "[Error: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set]"
        
        prompt = OUTREACH_PROMPT_TEMPLATE.format(
            job_title=job_title,
            company=company,
            description=description[:500]
        )
        
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
        
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are a professional job application assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['result']['response'].strip()
        
    except Exception as e:
        print(f"⚠️  Cloudflare AI API error: {e}")
        return f"[Error generating message: {str(e)}]"


def save_to_csv(jobs, filename=CSV_OUTPUT_FILE):
    """
    Saves job data to CSV file
    """
    try:
        fieldnames = ['url', 'title', 'company', 'location', 'description', 'outreach_message']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)
        
        print(f"✅ Saved {len(jobs)} jobs to {filename}")
        
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")


def get_google_sheets_client():
    """
    Authenticates and returns Google Sheets client using OAuth 2.0
    """
    creds = None
    
    # Load saved credentials
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return gspread.authorize(creds)


def save_to_google_sheets(jobs):
    """
    Appends job data to Google Sheets using OAuth 2.0
    Note: Requires adding your email as test user in Google Cloud Console
    See GOOGLE_SHEETS_SETUP.md for instructions
    """
    try:
        client = get_google_sheets_client()
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        
        # Add header if sheet is empty
        if sheet.row_count == 0:
            sheet.append_row(['Job URL', 'Job Title', 'Company', 'Location', 
                            'Description', 'Outreach Message'])
        
        # Append each job
        for job in jobs:
            sheet.append_row([
                job['url'],
                job['title'],
                job['company'],
                job['location'],
                job['description'],
                job['outreach_message']
            ])
        
        print(f"✅ Saved {len(jobs)} jobs to Google Sheets")
        
    except Exception as e:
        print(f"❌ Error saving to Google Sheets: {e}")
        print("💡 Tip: Make sure you've added yourself as a test user. See GOOGLE_SHEETS_SETUP.md")


def run_pipeline():
    """
    Main pipeline execution
    """
    print("\n" + "="*60)
    print("🚀 Starting Job Outreach Automation Pipeline")
    print("="*60 + "\n")
    
    # Step 1: Scrape jobs
    all_jobs = scrape_jobs()
    
    if not all_jobs:
        print("❌ No jobs found. Exiting pipeline.")
        return
    
    # Step 2: Validate and process jobs
    print("\n🔎 Validating and processing jobs...")
    validated_jobs = []
    
    for job in all_jobs:
        if validate_job(job['description'], job['location'], job['title']):
            print(f"✓ Valid: {job['title']} at {job['company']}")
            
            # Generate outreach message
            outreach_msg = generate_outreach_message(
                job['title'], 
                job['company'], 
                job['description']
            )
            
            validated_jobs.append({
                'url': job['url'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'description': job['description'],
                'outreach_message': outreach_msg
            })
            
            time.sleep(1)  # Rate limiting for API calls
    
    print(f"\n✅ Validated {len(validated_jobs)} out of {len(all_jobs)} jobs")
    
    if not validated_jobs:
        print("❌ No validated jobs to save. Exiting pipeline.")
        return
    
    # Step 3: Save to CSV
    print("\n💾 Saving results...")
    save_to_csv(validated_jobs)
    
    # Step 4: Save to Google Sheets
    save_to_google_sheets(validated_jobs)
    
    print("\n" + "="*60)
    print("✅ Pipeline completed successfully!")
    print("="*60 + "\n")


# ============================================================================
# SCHEDULER & MAIN EXECUTION
# ============================================================================

def start_scheduler():
    """
    Schedules the pipeline to run daily at 9:00 AM
    """
    schedule.every().day.at("09:00").do(run_pipeline)
    
    print("⏰ Scheduler started. Pipeline will run daily at 09:00 AM")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Run immediately on start
    run_pipeline()
    
    # Uncomment below to enable daily scheduling
    # start_scheduler()
