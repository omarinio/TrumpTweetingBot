import tweepy
import csv
import re
from keys import *

def get_all_tweets(screen_name):
    all_tweets = []
    new_tweets = []

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    client = tweepy.API(auth)
    new_tweets = client.user_timeline(screen_name=screen_name, count=200)

    while len(new_tweets) > 0:
        for tweet in new_tweets:
            all_tweets.append(tweet.text.encode("utf-8"))

        print( "We've got %s tweets so far" % (len(all_tweets)))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(screen_name=screen_name,
                                          count=200, max_id=max_id)

    return all_tweets

def clean_tweet(tweet):
    tweet = re.sub(b"https?\:\/\/", b"", tweet)   #links
    tweet = re.sub(b"#\S+", b"", tweet)           #hashtags
    tweet = re.sub(b"\.?@", b"", tweet)           #at mentions
    tweet = re.sub(b"RT.+", b"", tweet)           #Retweets
    tweet = re.sub(b"Video\:", b"", tweet)        #Videos
    tweet = re.sub(b"\n", b"", tweet)             #new lines
    tweet = re.sub(b"&", b"and", tweet)       #encoded ampersands
    return tweet

def write_tweets_to_csv(tweets):
    with open('tweets.csv', 'w') as f:
        writer = csv.writer(f)
        for tweet in tweets:
            tweet = clean_tweet(tweet)
            if tweet:
                writer.writerow([tweet])

if __name__ == "__main__":
    tweets = get_all_tweets("realdonaldtrump")
    write_tweets_to_csv(tweets)