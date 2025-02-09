import tweepy
import time
import os
from datetime import datetime

# Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)  # Enable rate limit handling

# Function to tweet a message
def tweet(message):
    try:
        api.update_status(message)
        print(f"Tweeted: {message}")
    except tweepy.TweepyException as e:
        print(f"Error tweeting: {e}")

# Function to reply to mentions
def reply_to_mentions():
    try:
        # Fetch the latest mentions
        mentions = api.mentions_timeline(count=5)
        for mention in mentions:
            if not mention.favorited:  # Avoid replying to the same mention twice
                tweet_text = f"@{mention.user.screen_name} Thanks for mentioning me!"
                api.update_status(tweet_text, in_reply_to_status_id=mention.id)
                api.create_favorite(mention.id)  # Like the mention
                print(f"Replied to mention from @{mention.user.screen_name}")
    except tweepy.TweepyException as e:
        print(f"Error replying to mentions: {e}")

# Function to retweet and like tweets based on a keyword
def retweet_and_like(keyword):
    try:
        # Search for tweets containing the keyword
        tweets = api.search(q=keyword, count=5, result_type="recent")
        for tweet in tweets:
            if not tweet.retweeted:  # Avoid retweeting the same tweet twice
                api.retweet(tweet.id)
                api.create_favorite(tweet.id)  # Like the tweet
                print(f"Retweeted and liked tweet by @{tweet.user.screen_name}: {tweet.text}")
    except tweepy.TweepyException as e:
        print(f"Error retweeting/liking: {e}")

# Function to log rate limit status
def log_rate_limit_status():
    try:
        rate_limit_status = api.rate_limit_status()
        print("Rate limit status:")
        print(rate_limit_status)
    except tweepy.TweepyException as e:
        print(f"Error checking rate limits: {e}")

# Main loop
if __name__ == "__main__":
    while True:
        try:
            # Tweet a message
            tweet("Hello, Twitter! This is a test tweet from my bot. #TwitterBot")

            # Reply to mentions
            reply_to_mentions()

            # Retweet and like tweets with a specific keyword
            retweet_and_like("Python")

            # Log rate limit status
            log_rate_limit_status()

            # Wait for 15 minutes before the next iteration (to avoid rate limits)
            print("Waiting for 15 minutes...")
            time.sleep(900)  # 15 minutes = 900 seconds

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait 1 minute before retrying