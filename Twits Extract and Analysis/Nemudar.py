from pymongo import MongoClient
import datetime
from nltk.stem.wordnet import WordNetLemmatizer
import json
from nltk.classify import NaiveBayesClassifier
from googletrans import Translator

lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
events = db.events

tweets = twits.find(
    {"twitHashtags": {"$in": ["1-0", "portugal", "cr7", "cristianoronaldo", "ronaldo", "pepe", "por", "france", "fra",
                              "euro2016", "final", "amp", "supporting", "euro", "support"]},
     "twitmiliSeconds": {"$gt": 1468108920000, "$lt": 1468118160000}}) # 5 mins after the game


# 1min = 60000ms

lastStep = 1468108920000
minutes = 0
lastMode = 0
twitsCounter = 0
twitNumbers = []
eventCounter = 0
eventList = events.find({})
for tweet in tweets:
    if (tweet["twitmiliSeconds"] - lastStep) > 60000:
        minutes += 1
        twitNumbers.append({"minute":minutes,"amount":twitsCounter})
        lastStep += 60000  # 1min shift
        twitsCounter = 0
    else:
        twitsCounter += 1

lastPlace = 0
eventTimeLine = []

for x in range (0,minutes):
    eventList = events.find({"relativeTime": x})
    for event in eventList:
        if event["relativeTime"]:
            eventTimeLine.append({"eventTime": x, "name": event["eventName"],"subject": event["subject"]})

print(twitNumbers)
print(eventTimeLine)
# Predict
