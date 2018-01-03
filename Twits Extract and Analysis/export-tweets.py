from __future__ import print_function
import pymysql
from pymongo import MongoClient
import datetime
from nltk.stem.wordnet import WordNetLemmatizer

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='147852',
                             db='tweetsDb',
                             autocommit=True
                             )

cursor = connection.cursor()
print("writing to db")
lmtzr = WordNetLemmatizer()

epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
translatedTweets = db.translatedTweets
events = db.events

tweets = translatedTweets.find(
    {"tweetMiliSeconds": {"$gt": 1467563400000,"$lt": 1467570000000}
                                },
        {"tweetTokens": 1, "tweetMiliSeconds": 1, "tweetId": 1, "tweetText": 1, "tweetHashtags": 1,"posFeeling": 1,"negFeeling": 1,"tweetDate":1,"neuFeeling": 1,"compoundFeeling":1, "$maxScan": 100000000, "$max": 100000000})
print("start")
z = 0
x = 0
for tweet in tweets:
    try:
        datex = temp = datetime.datetime.fromtimestamp(tweet['tweetMiliSeconds'] / 1000).strftime('%Y-%m-%d %H:%M:%S-0')
        cursor.execute("INSERT INTO tweets VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",("3",tweet['tweetId'], tweet["tweetText"], datex, tweet['tweetMiliSeconds'], tweet['posFeeling'], tweet['negFeeling'], tweet['compoundFeeling'], tweet['neuFeeling']))
        for hashtag in range(0, len(tweet["tweetHashtags"])):
            cursor.execute("INSERT INTO hashtags VALUES(%s,%s,%s,%s)", ("3", tweet["tweetId"], tweet["tweetHashtags"][hashtag], datex))
        for token in range(0, len(tweet["tweetTokens"])):
            cursor.execute("INSERT INTO tokens VALUES(%s,%s,%s,%s)", ("3", tweet['tweetId'], tweet["tweetTokens"][token], datex))
        print(z, " successed!")
        z += 1
    except:
        x += 1
        print("failed : ", x)

