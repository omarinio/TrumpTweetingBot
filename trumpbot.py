import tweepy
import markovify

from keys import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

with open("tweets.csv") as f:
    text = f.read()

text_model = markovify.Text(text)

model_tweet = text_model.make_sentence()

print(model_tweet)

api.update_status(model_tweet)