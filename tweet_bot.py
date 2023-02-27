import openai
import tweepy
import time
import datetime

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Set up Twitter API keys and access tokens
consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define tweet prompts
prompts = [
    "What's new in Thailand's cannabis industry?",
    "How are NFTs changing the cannabis industry?",
    "Why is cannabis hospitality the next big thing?",
]

# Set up tweet intervals (in seconds)
tweet_interval = 3 * 60 * 60 # 3 hours

# Define function to generate and send tweet threads
def generate_tweet_thread(prompt):
    # Generate tweet thread using OpenAI API
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    tweet_thread = response.choices[0].text.strip().split("\n")
    
    # Send tweet thread using Twitter API
    try:
        tweet_ids = []
        for tweet in tweet_thread:
            if tweet == tweet_thread[0]:
                tweet = api.update_status(tweet)
            else:
                tweet = api.update_status(tweet, in_reply_to_status_id=tweet_ids[-1].id)
            tweet_ids.append(tweet)
            print(f'Tweeted: {tweet.text}')
    except tweepy.TweepError as error:
        print(f'Error: {error}')

# Define function to check if it's a new day
def is_new_day():
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0 and now.second == 0:
        return True
    else:
        return False

# Loop through tweet prompts and send tweet threads at specified intervals
while True:
    if is_new_day():
        for prompt in prompts:
            generate_tweet_thread(prompt)
            time.sleep(tweet_interval)
    else:
        time.sleep(60)
