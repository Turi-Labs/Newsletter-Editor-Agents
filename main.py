from helper_functions.hn_scrapper import write_hn_posts
from helper_functions.filter import filter
from helper_functions.summarize import *
from agents.newsletter_agent import craft_newsletter
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# today = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
today = "2025-05-9"

base_dir = "knowledgebase"

today_dir = os.path.join(base_dir, today)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)

## File paths. I want to add them in a folder named by the date yyy-mm-dd.
hn_posts_path = os.path.join(today_dir, "hn_posts.md")
filtered_posts = os.path.join(today_dir, "filtered_posts.md")
research_notes_path = os.path.join(today_dir, "research_notes.md")
newsletter_path = os.path.join(today_dir, "newsletter.md")
logger.info(f"Newsletter will be saved to: {newsletter_path}")

write_hn_posts(today, 5, hn_posts_path)

filter(hn_posts_path, filtered_posts)

# append all summaries to a txt file
l = get_links(filtered_posts)
logger.info("Links extracted successfully")
c = get_link_content(l)
logger.info("Content extracted from links")
s = send_to_ai(c)
logger.info("AI summaries generated")

# Write the AI response to a text file
logger.info("Started writing summaries to research_notes.md")
with open(research_notes_path, 'w', encoding='utf-8') as file:
    for i, summary in enumerate(s, 1):
        file.write(f"Summary {i}:\n")
        file.write(f"{summary}\n")
        file.write("\n")

content = ''
with open(research_notes_path, 'r') as file:
    content = file.read()

logger.info("Newsletter Generation started")
craft_newsletter(content, newsletter_path)
logger.info("Newsletter successfully generated and saved")
