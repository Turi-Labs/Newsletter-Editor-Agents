from helper_functions.hn_scrapper import write_hn_posts
from helper_functions.filter import filter
from helper_functions.summarize import *
from agents.newsletter_agent import craft_newsletter


from datetime import datetime
import os

# today = datetime.now().strftime("%d-%m-%Y") # Change this. yyy-mm-dd is the format
date = "2025-03-12"
today = date
base_dir = "knowledgebase"

today_dir = os.path.join(base_dir, today)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)

## File paths. I want to add them in a folder named by the date yyy-mm-dd.
hn_posts_path = os.path.join(today_dir, "hn_posts.md")
filtered_posts = os.path.join(today_dir, "filtered_posts.md")
research_notes_path = os.path.join(today_dir, "research_notes.md")
newsletter_path = os.path.join(today_dir, "newsletter.md")
print(newsletter_path)

write_hn_posts(date, 5, hn_posts_path)

filter(hn_posts_path, filtered_posts)

# append all summaries to a txt file
l = get_links(filtered_posts)
print("Links extracted successfully")
c = get_link_content(l)
print("Content extracted from links")
s = send_to_ai(c)
print("AI summaries generated")
# print(s)

# Write the AI response to a text file
with open(research_notes_path, 'w', encoding='utf-8') as file:
    for i, summary in enumerate(s, 1):
        file.write(f"Summary {i}:\n")
        file.write(f"{summary}\n")
        file.write("\n")

content = ''
with open(research_notes_path, 'r') as file:
    content = file.read()

craft_newsletter(content, newsletter_path)