import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')



def post_tweet(text: str, img_path: str) -> str:
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if img_path is not None:
        media = api.media_upload(img_path)
        media_id = media.media_id_string
        response = client.create_tweet(text=text, media_ids=[media_id])
    else:
        response = client.create_tweet(text=text)

    tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
    return f"Tweet posted successfully: {tweet_url}"

# post_tweet("hello, I am an agent! ", None)