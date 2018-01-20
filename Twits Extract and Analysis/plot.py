from pymongo import MongoClient
import datetime
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
translatedTweets = db.translatedTweets
plots = db.plots
events = db.events
left = 0
right = 0
for matchId in range(1, 5):
    if matchId == 1:  # France - Portugal ( Final ) - 154 mins (1)
        left = 1468168200000
        right = 1468177440000

    if matchId == 2:  # France - Germany (Semi Final) 111mins (2)
        left = 1467909000000
        right = 1467915720000
    if matchId == 3:
        left = 1467563400000  # France - Iceland (Quarter Final) 108mins (3)
        right = 1467570000000
    if matchId == 4:  # Germany Italy - ( 1/8 ) 158 mins (1 - 1) penalties (6 - 5)
        left = 1467483720000
        right = 1467493200000
    #     Query by words ...
    keyword = ""
    tweets = translatedTweets.find({"tweetText":{"$regex":".*"+keyword+".*"},"tweetMiliSeconds":{"$gt":left,"$lt":right}})
    eventsList = events.find({"matchId": matchId})
    classedTweets = []
    posSums = []
    negSums = []
    neusSums = []
    compsSums = []
    minutes = int((right - left) / 60000)
    for x in range(0, minutes):
        classedTweets.append([])
        posSums.append(0.0)
        negSums.append(0.0)
        neusSums.append(0.0)
        compsSums.append(0.0)
    m = 0
    eventsLists = []
    t = 0
    for event in eventsList:
        eventsLists.append(event)
        print(event["eventKey"])
    try:
        for tweet in tweets:
            minute = int((tweet["tweetMiliSeconds"] - left) / 60000)  # 1 minutes Step
            classedTweets[minute].append({"date": tweet["tweetMiliSeconds"], "pos": tweet["posFeeling"], "neu": tweet["neuFeeling"], "neg": tweet["negFeeling"], "comp": tweet["compoundFeeling"]})
            posSums[minute] += tweet["posFeeling"]
            negSums[minute] += tweet["negFeeling"]
            neusSums[minute] += tweet["neuFeeling"]
            compsSums[minute] += tweet["compoundFeeling"]
            print(" ___ ", posSums[minute], "- ((())) -", negSums[minute], "neuSums : ", neusSums[minute] , "compSums : ", compsSums[minute])
            print(m, "(0-v-0)", minute, " ----- ", tweet["tweetId"], "- Miliseconds - ", tweet["tweetMiliSeconds"])
            m += 1
    except:
        print("((())) --->  ", m, "  --- failed !!!!")
    finally:
        plots.insert_one({"matchId": matchId, "keyword": keyword, "matchTeams": "France Portugal", "neus": neusSums, "poses": posSums, "negs": negSums, "comps": compsSums, "classedTweets": classedTweets, "events": eventsLists})
        print(" matchId  ---> ", matchId, " Finished! ---- t -> ", t)








