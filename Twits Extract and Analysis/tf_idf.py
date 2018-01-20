from __future__ import division, unicode_literals

import pickle
import redis
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from itertools import islice
import datetime
import tokenize
from threading import Thread
import nltk
import tfidf
import math
import tf as tf
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob as textBlob
from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
import json

lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)
client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
Plots = db.plots
translatedTweets = db.translatedTweets
events = db.events
r = redis.StrictRedis(host='localhost', port=6379, db=0)


class tfIdf():
    def tf_idf(self):
        z = 0
        left = 1468168200000
        right = 1468177200000
        tops = []
        step = 60000  # 1 Minute Window
        for x in range(0, 148):
            right = left + step
            tweets = translatedTweets.find({"tweetMiliSeconds": {"$gt": left, "$lt": right}},
                                           {"tweetTokens": 1, "tweetHashtags": 1, "tweetMiliSeconds": 1,
                                            "tweetText": 1})
            left = left + step
            print(left, right)
            z = 0
            y = 0
            for tweet in tweets:
                z += 1
                print(z, ") Tweets Added!")
                for token in tweet["tweetTokens"]:
                    y += 1
                    if r.zadd('minute-%d' %x, 1, token) == 0:
                        r.zincrby("minute-%d" %x, token, 1)

            tops.append(r.zrangebyscore("mintue-%d" %x, -5, -1))

        Plots.updateOne({"matchId": 1}, {"set":{"top5EachMinuteList": tops}})


if __name__ == '__main__':
    obj = tfIdf()  # 74 * 2minutes ==> 148 reltive -> 120+3 // 9 to 11:30pm 07-10-2016
    obj.tf_idf()
    print("Finished")
