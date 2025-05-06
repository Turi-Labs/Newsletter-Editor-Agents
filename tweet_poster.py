from helper_functions.tweet import post_tweet
import json
import os

def post_next_tweet():
    json_file_path = 'generated_tweets.json'
    
    # Check if the file exists
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} does not exist.")
        return False
    
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            tweets = json.load(file)
        # print(tweets)
        
        # Check if there are any tweets
        if not tweets:
            print("No tweets available in the JSON file.")
            return False
        
        # Get the first tweet
        tweet = tweets[0]
        # print(tweet)
        
        # Extract tweet text and image path
        tweet_text = tweet.get('tweet', '')
        image_path = tweet.get('image_path', None)

        # Post the tweet
        post_tweet(tweet_text, image_path)
        print(f"Posted tweet: {tweet_text}")
        
        # Remove the posted tweet from the list
        tweets.pop(0)
        
        # Write the updated list back to the file
        with open(json_file_path, 'w') as file:
            json.dump(tweets, file, indent=4)
        
        return True
    
    except Exception as e:
        print(f"Error posting tweet: {str(e)}")
        return False

if __name__ == "__main__":
    post_next_tweet()