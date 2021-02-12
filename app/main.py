#!/bin/python

#title:         main.py
#description:   Get better insight into reactions to `Twitter posts` with this FLASK-app.
#author:        Michael Muyakwa
#created:       2020-12-02
#updated:       2021-02-12
#version:       1.8
#license:       MIT

from flask.globals import current_app
from datetime import datetime
# Regular Expression Python module
import re
# TextBlob - Python library for processing textual data
from textblob import TextBlob
# Matplotlib - plotting library to create graphs and charts
import matplotlib.pyplot as plt
from flask import (Flask, render_template, request)
from replies import *
from calcdates import *
from markupsafe import escape
from decouple import config
# WordCloud - Python linrary for creating image wordclouds
from wordcloud import (WordCloud, STOPWORDS)
import pybase64
from io import BytesIO
from concurrent import futures

# configuration
DEBUG = config('DEBUG')

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    tweet_id = ''
    if request.method == 'POST':
        tweet_id = escape(request.form['tweet_id']).split('/')[-1]
        print('Tweet_Id =' + tweet_id)
    return tweetSearchHTML(tweet_id)

def tweetSearchHTML(tweet_id):
    if tweet_id != '':
        #tweet = getTweet(tweet_id)
        #replies = getReplies(tweet_id)
        with futures.ThreadPoolExecutor(max_workers=2) as ex:
            ftweet = ex.submit(getTweet, tweet_id)
            freplies = ex.submit(getReplies, tweet_id)
        #print(tweet)
        #print(replies)
        #with open("../output.txt", "w") as outfile:
        #    outfile.write("\n".join(str(item) for item in replies))
        tweet = ftweet.result()
        replies = freplies.result()
        wordcloud = ''
        if (len(replies) > 0):
            wordcloud = buildWordCloud(replies)
        return render_template('index.html', tweet=tweet ,len = len(replies), replies = replies, tweet_id = tweet_id, wordcloud = wordcloud)
    else:
        return render_template('index.html')

def buildWordCloud(replies):
#    try:
    words = ''
    for i in range(0, len(replies)):
        words = words + ''.join(replies[i].full_text.strip().replace("\r","").replace("\n","").replace("@" + replies[i].in_reply_to_screen_name,""))
    #print(words)
    if len(words) > 0:
        words = cleanUpTweet(words)
        # Creating a word cloud
        stopwords = set(STOPWORDS)
        print("Words: " + words)
        wordCloud = WordCloud(width=600, height=400, max_words=200, stopwords=stopwords, background_color='white', random_state=1).generate(words)
        # GEHEIM-TIP! - "plt.switch_backend('agg')" damit ich "matplotlib" auch in Flask nutzen kann.
        plt.switch_backend('agg')
        plt.imshow(wordCloud, interpolation='bilinear')
        plt.axis("off")
        buf = BytesIO()
        plt.savefig(buf, format="png")
        # Embed the result in the html output.
        data = pybase64.b64encode(buf.getbuffer()).decode("ascii")
        return data
    else:
        return None
#    except:
#        None

def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    # Remove hashtags
    txt = re.sub(r'#', '', txt)
    # Remove retweets:
    txt = re.sub(r'RT : ', '', txt)
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    return txt

@app.context_processor
def my_utility_processor():

    #def date_now(format="%d.m.%Y %H:%M:%S"):
    def date_now():
        format = "%Y"
        CopyrightDate = '2021'
        currentYear = datetime.now().strftime(format)
        if currentYear != CopyrightDate:
            CopyrightDate = '2021 - ' + currentYear
        return CopyrightDate

    def name():
        return "Michael Muyakwa"

    def getTextSubjectivity(txt):
        return round(TextBlob(txt).sentiment.subjectivity, 2)

    def getTextPolarity(txt):
        return round(TextBlob(txt).sentiment.polarity, 2)

    def formatDate(dateSent):
        return dateSent.strftime("%c")

    def tweetDates(tweet_date, reply_date):
        #return getDuration(tweet_date, reply_date, 'minutes')
        return getDuration(tweet_date, reply_date)

    return dict(date_now=date_now, company=name, subjectivity=getTextSubjectivity, polarity=getTextPolarity, formatDate=formatDate, tweetDates=tweetDates)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=DEBUG, port=5000)
