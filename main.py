from helper_functions.hn_scrapper import write_hn_posts
from helper_functions.filter import filter
from helper_functions.summarize import *
from agents.newsletter_agent import craft_newsletter


from datetime import datetime
import os

today = datetime.now().strftime("%d-%m-%Y")

if not os.path.exists(today):
    os.makedirs(today)

## File paths. I want to add them in a folder named by the date dd-mm-yyyy.
hn_posts_path = os.path.join(today, "hn_posts.md")
filtered_posts = os.path.join(today, "filtered_posts.md")
research_notes_path = os.path.join(today, "research_notes.md")
newsletter_path = os.path.join(today, "newsletter.md")


write_hn_posts("2025-03-20", 100, hn_posts_path)

filter(hn_posts_path, filtered_posts)

# append all summaries to a txt file
l = get_links(filtered_posts)
c = get_link_content(l)
s = send_to_ai(c)
print(s)

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