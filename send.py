import requests
import markdown
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timezone

load_dotenv()

API_KEY = os.environ.get("BEEHIIV_API_KEY")
PUBLICATION_ID = os.environ.get("BEEHIIV_PUBLICATION_ID")
MARKDOWN_FILE_PATH = "newsletter/2025-03-20.md" # Path to your newsletter file

if API_KEY:
    print(API_KEY)
if PUBLICATION_ID:
    print(PUBLICATION_ID)



# --- API Details ---
API_BASE_URL = "https://api.beehiiv.com/v2"
POSTS_ENDPOINT = f"{API_BASE_URL}/publications/{PUBLICATION_ID}/posts"

# --- Read and Convert Markdown ---
try:
    with open(MARKDOWN_FILE_PATH, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    html_content = markdown_content
except Exception as e:
    print(f"Error reading or converting markdown file: {e}")
    exit()

# --- Prepare Post Data ---
post_title = "Your Awesome Newsletter Title" # Change this!
email_subject = "This Week's Newsletter Update" # Change this!

# Data payload for the API request
# Setting 'status' to 'confirmed' triggers immediate sending
# 'platform_delivery' ensures it goes out via email
# 'audience' set to 'all' targets all subscribers
payload = {
    "title": post_title,
    "subtitle": "", # Optional: Add a subtitle if desired
    "content_html": html_content,
    # "content_markdown": markdown_content, # You could send markdown too, but HTML is often preferred for email clients
    # "email_subject": email_subject,
    "status": "confirmed", # Set to 'confirmed' to send immediately upon creation
    "platform_delivery": ["web"], # Send via email and show on web publication
    "audience": "all", # Target all subscribers
    # "scheduled_at": None, # Omit or set to None/past time for immediate send with 'confirmed' status
    # "thumbnail_url": "https://example.com/image.jpg", # Optional: Add a thumbnail URL
    # "author_id": "usr_xxxx", # Optional: Specify author if needed, defaults to primary user
    # "show_author": True, # Optional: Defaults usually fine
    # "split_test": False, # Optional
    # "content_tags": ["tag1", "tag2"] # Optional: Add tags
}

# --- Prepare Headers ---
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# --- Make API Request ---
print(f"Attempting to create and send post '{post_title}'...")

try:
    response = requests.post(POSTS_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

    # --- Process Response ---
    response_data = response.json()
    post_id = response_data.get("data", {}).get("id")
    post_status = response_data.get("data", {}).get("status")

    print("\n--- Success! ---")
    print(f"Post created successfully with ID: {post_id}")
    print(f"Post Status: {post_status}")
    if post_status == 'confirmed':
        print("The post has been queued for immediate delivery to all subscribers.")
    else:
        print(f"Post created with status '{post_status}'. It might not be sending immediately. Check Beehiiv dashboard.")
    # print("\nFull API Response:")
    # print(json.dumps(response_data, indent=2))


except requests.exceptions.RequestException as e:
    print(f"\n--- Error ---")
    print(f"API Request Failed: {e}")
    if e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        try:
            error_details = e.response.json()
            print("Error Details:")
            print(json.dumps(error_details, indent=2))
        except json.JSONDecodeError:
            print(f"Response Content: {e.response.text}")
except Exception as e:
     print(f"\n--- An unexpected error occurred ---")
     print(e)