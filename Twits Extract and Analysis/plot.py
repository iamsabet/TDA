from flask import json, jsonify
from pymongo import MongoClient
import datetime
from flask_cors import CORS
from flask import Flask
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)
#1468168200000 France - Portugal ( Final ) - 154 mins (1)
#1468177440000

#1467909000000	France - Germany (Semi Final) 111mins (2)
#1467915720000

#1467563400000	France - Iceland (Quarter Final) 108mins (3)
#1467570000000

#1467483720000	Germany Italy - ( 1/8 ) 158 mins (1 - 1) penalties (6 - 5) 
#1467493200000 
app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
translatedTweets = db.translatedTweets
plots = db.plots
events = db.events
left = 1467909000000
right = 1467915720000


@app.route('/plot/')
def main():
    tweets = translatedTweets.find({"tweetMiliSeconds": {"$gt": left, "$lt": right}})
    print(tweets)
    eventsList = events.find({"matchId": 2})
    classedTweets = []
    posSums = []
    negSums = []
    neusSums = []
    compsSums = []
    minutes = int((right - left)/60000)
    for x in range(0, minutes):
        classedTweets.append([])
        posSums.append(0.0)
        negSums.append(0.0)
        neusSums.append(0.0)
        compsSums.append(0.0)
    m = 0
    eventsLists = []
    for event in eventsList:
        eventsLists.append(event)
        print(event["eventKey"])
    try:
        for tweet in tweets:
            minutes = int((right - tweet["tweetMiliSeconds"]) / 60000)  # 1 minutes Step
            classedTweets[minutes].append({"pos": tweet["posFeeling"], "neu": tweet["neuFeeling"], "neg": tweet["negFeeling"], "comp": tweet["compoundFeeling"]})
            posSums[minutes] += tweet["posFeeling"]
            negSums[minutes] += tweet["negFeeling"]
            neusSums[minutes] += tweet["neuFeeling"]
            compsSums[minutes] += tweet["compoundFeeling"]
            print(" ___ ", posSums[minutes], "- ((())) -", negSums[minutes] , "neuSums : ", neusSums[minutes] , "compSums : ", compsSums[minutes])
            print(m, "(0-v-0)", minutes, " ----- ", tweet["tweetId"], "- Miliseconds - ", tweet["tweetMiliSeconds"], "")
            m += 1
    except:
        print("((())) --->  ", m, "  --- failed !!!!")
    finally:
        plots.insert_one({"matchId": 2, "matchTeams": "France Portugal", "neus": neusSums, "poses": posSums, "negs": negSums, "comps": compsSums, "classedTweets": classedTweets, "events": eventsLists})
        return "true"


if __name__ == '__main__':
    app.run()






