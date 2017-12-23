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

events = events.find({},
        {"matchId": 1, "eventName": 1, "subject": 1, "eventKey": 1, "object": 1, "eventTime": 1}
)
print("start")
z = 0
x = 0
for event in events:
    try:
        datex = temp = datetime.datetime.fromtimestamp(event['eventTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S-0')
        cursor.execute("INSERT INTO events VALUES(%s,%s,%s,%s,%s,%s)", (event["matchId"],event['eventName'], event["subject"], event["eventKey"],event['eventTime'],datex))
        print(z, " successed!")
        z += 1
    except:
        x += 1
        print("failed : ", x)

