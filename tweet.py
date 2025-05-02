from agents.tweet_creator_agent import create_tweet

from datetime import datetime
import os

# today = datetime.now().strftime("%d-%m-%Y") # Change this. yyy-mm-dd is the format
date = "2025-04-23"
today = date
base_dir = "knowledgebase"

today_dir = os.path.join(base_dir, today)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)

research_notes_path = os.path.join(today_dir, "research_notes.md")

# print(newsletter_path)

summaries = []
with open(research_notes_path, 'r', encoding='utf-8') as file:
    content = file.read()
    # Split content by "Summary" to get individual summaries
    split_summaries = content.split("Summary")[1:]  # Skip empty first element
    for summary in split_summaries:
        if summary.strip():  # Only append non-empty summaries
            summaries.append(f"Summary{summary}")


# We have tweet creation, images, and summary notes ready.
# What we need is, an agent which will look into the images and choose right one (only one)
# An agent which will read the whole summary notes and create a schedule for posting
# Twitter api and Posting in community

# Post for 30 days continuously and see the results. 10-20 posts a day
print(summaries[4])
create_tweet(summaries[4])

