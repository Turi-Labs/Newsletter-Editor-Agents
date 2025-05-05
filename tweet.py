from agents.tweet_creator_agent import create_tweet
from agents.image_analyzer_agent import image_analyzer
from helper_functions.screenshot import take_and_split_screenshot
import asyncio
from datetime import datetime
import os

# today = datetime.now().strftime("%d-%m-%Y") # Change this. yyy-mm-dd is the format
date = "2025-04-20"
today = date
base_dir = "knowledgebase"

today_dir = os.path.join(base_dir, today)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)

screenshots_dir = "screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

output_base_name = os.path.join(screenshots_dir, "screenshot")

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
# Done -> What we need is, an agent which will look into the images and choose right one (only one)
# An agent which will read the whole summary notes and create a schedule for posting
# Twitter api and Posting in community

# Post for 30 days continuously and see the results. 10-20 posts a day
# print(summaries[4])

out = create_tweet(summaries[14])
tweet = out.tweet

tweet_words = tweet.split()[:5]
tweet_filename = '_'.join(tweet_words)

tweet_filename = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in tweet_filename)
tweet_folder = 'tweet'

if not os.path.exists(tweet_folder):
    os.makedirs(tweet_folder)

tweet_path = os.path.join(tweet_folder, tweet_filename + '.txt')
with open(tweet_path, "w", encoding="utf-8") as f:
    f.write(tweet)

target_url = out.link


# Run the async function
created_files = asyncio.run(take_and_split_screenshot(target_url, output_base_name))

screenshot_files = []
if created_files:
    for f in created_files:
        screenshot_files.append(f)

img = image_analyzer(screenshot_files, tweet)


if img and os.path.exists(img):
    new_path = f"screenshots/{tweet_filename}.png"
    os.rename(img, new_path)
    img = new_path
    # Clean up screenshots
print("\nStarting Cleanup")
screenshot_dir = "screenshots"
if os.path.exists(screenshot_dir):
    for file in os.listdir(screenshot_dir):
        if file.startswith("screenshot"):
            file_path = os.path.join(screenshot_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)





