# We have tweet creation, images, and summary notes ready.
# Done -> What we need is, an agent which will look into the images and choose right one (only one)
# An agent which will read the whole summary notes and create a schedule for posting
# Twitter api and Posting in community

from agents.tweet_creator_agent import create_tweet
from agents.image_analyzer_agent import image_analyzer
from helper_functions.screenshot import take_and_split_screenshot
import asyncio
from datetime import datetime
import os

# today = datetime.now().strftime("%d-%m-%Y") # Change this. yyy-mm-dd is the format
date = "2025-05-08"
today = date
base_dir = "knowledgebase"

today_dir = os.path.join(base_dir, today)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)

screenshots_dir = "screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

output_base_name = os.path.join(screenshots_dir, "screenshot")

research_notes_path = os.path.join(today_dir, "research_notes.md")
screenshots_dir = os.path.join(today_dir, "screenshots")
output_json_path = os.path.join(today_dir, "generated_tweets.json")

# print(newsletter_path)

summaries = []
index = 0
with open(research_notes_path, 'r', encoding='utf-8') as file:
    content = file.read()
    # Split content by "Summary" to get individual summaries
    split_summaries = content.split("Summary")[1:]  # Skip empty first element
    for summary in split_summaries:
        if summary.strip():  # Only append non-empty summaries
            summaries.append(f"Summary{summary}")
            index += 1

print(index)
# Post for 30 days continuously and see the results. 10-20 posts a day



## We generate a tweet, and we also generate an image. We save the tweet in a file (change this to json), and images in a folder. 
# There will be a json which will contain the tweet and image path. this should be sent to the tweet function randomly.

## Input: summary index.
## Output: JSON containing the tweet and image path.
def generate_tweet_with_image(index, screenshots_dir):
    out = create_tweet(summaries[index])
    tweet = out.tweet

    tweet_words = tweet.split()[:5]
    tweet_filename = '_'.join(tweet_words)

    tweet_filename = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in tweet_filename)

    target_url = out.link

    # Run the async function
    created_files = asyncio.run(take_and_split_screenshot(target_url, output_base_name))

    screenshot_files = []
    if created_files:
        for f in created_files:
            screenshot_files.append(f)

    img = image_analyzer(screenshot_files, tweet)
    image_path = None

    if img and os.path.exists(img):
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        new_path = f"{screenshots_dir}/{tweet_filename}.png"
        os.rename(img, new_path)
        image_path = new_path

    # Clean up screenshots
    print("\nStarting Cleanup\n")
    if os.path.exists(screenshots_dir):
        for file in os.listdir(screenshots_dir):
            if file.startswith("screenshot"):
                file_path = os.path.join(screenshots_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    print("\nCleanup Complete\n")
    # Return tweet and image path directly
    return tweet, image_path


def generate_all_tweets(index, screenshots_dir, output_json_path):
    results = []
    
    ## TODO: Get the total number of indexes (you may need to adjust this based on your data source)
    total_indexes = 4
    
    for index in range(total_indexes):
        try:
            tweet, image_path = generate_tweet_with_image(index, screenshots_dir)
            results.append({
                'index': index,
                'tweet': tweet,
                'image_path': image_path
            })
            print(f"Generated tweet {index+1}/{total_indexes}\n")
        except Exception as e:
            print(f"Error generating tweet for index {index}: {str(e)}")
    
    # Save results to a file
    import json
    with open(output_json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Generated {len(results)} tweets. Results saved to '{output_json_path}'\n")
    return results


## We have a json file with the tweets and image paths.
## An agent which will read the json file, change the order, remove duplicates.
## Output: A json file with the tweets and image paths in the order of posting.def post_planner():




# Generate all tweets
if __name__ == "__main__":
    print(index)
    generate_all_tweets(index, screenshots_dir, output_json_path)

