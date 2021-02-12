import csv
import tweepy
import os
from collections import OrderedDict
import ssl
from decouple import config

def tweetAPI():
    auth = tweepy.OAuthHandler(config('CONSUMER_KEY'), config('CONSUMER_SECRET'))
    auth.set_access_token(config('OAUTH_TOKEN'), config('OAUTH_TOKEN_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def getReplies(tweet_id):
    api = tweetAPI()
    #tweet_id = '1345375036149014530'
    user = api.get_status(tweet_id)
#    print(user)
    user_name = user.user.screen_name

    # update these for whatever tweet you want to process replies to
    replies = []
    for tweet in tweepy.Cursor(api.search, q='to:'+user_name, result_type='recent', timeout=999999, tweet_mode="extended").items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet)

    return replies
    #print(replies)

def getTweet(tweet_id):
    api = tweetAPI()
    tweet = api.get_status(tweet_id)
    return tweet

def saveCSV(tweet_id, replies):
    # Zu Testzwecken CSV-Datei vorher löschen
    csv_file = tweet_id + ".csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)

    # Schreibe Datei in CSV-Datei
    with open(csv_file, 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=['user', 'text'])
        csv_writer.writeheader()
        for tweet in replies:
            print(tweet.user.screen_name)
            tw_text = tweet.full_text.strip().replace("\r","").replace("\n","")
            print(tw_text)
            row = {'user': tweet.user.screen_name, 'text': tw_text}
            csv_writer.writerow(row)
