from pymongo import MongoClient
import datetime
from nltk.stem.wordnet import WordNetLemmatizer

import matplotlib.pyplot as plt
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
events = db.events

tweets = twits.find(
    {"twitmiliSeconds": {"$gt": 1468108920000, "$lt": 1468118160000}})  # 5 mins after the game


# 1min = 60000ms

lastStep = 1468108920000
minutes = 0
lastMode = 0
twitsCounter = 0
twitNumbers = []
eventCounter = 0
eventList = events.find({})
axis = [0]

for tweet in tweets:
    if (tweet["twitmiliSeconds"] - lastStep) > 60000:
        minutes += 1
        axis.append(minutes)
        twitNumbers.append(twitsCounter)
        lastStep += 60000  # 1min shift
        twitsCounter = 0
    else:
        twitsCounter += 1

lastPlace = 0
eventTimeLine = []
y = 0
for x in range(0,minutes):

    eventList = events.find({"relativeTime": x})
    for event in eventList:
        if event["relativeTime"]:
            eventTimeLine.append({"eventTime": x, "name": event["eventName"],"subject": event["subject"]})


print(twitNumbers)
print(eventTimeLine)

plt.plot(axis,twitNumbers, 'ro')
plt.axis([0, 6, 0, 20])
plt.show()
