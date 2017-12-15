from pymongo import MongoClient
import datetime
from nltk.stem.wordnet import WordNetLemmatizer
from googletrans import Translator
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
events = db.events

tweets = twits.find({"twitHashtags": {"$in": ["1-0","goal","gol","goaall","goals","gool","captain","referre","penalty","foul","portugal", "cr7", "cristianoronaldo", "ronaldo", "pepe", "por", "france", "fra",
            "euro2016", "final", "amp", "supporting", "euro" , "support"]},
            "twitmiliSeconds": {"$gt": 1468108920000, "$lt": 1468117860000}}, {"twitTokens": 1, "twitmiliSeconds": 1, "positiveFeelings" : 1, "NegativeFeelings": 1, "twitId" : 1,"twitText": 1,"tokensFeeling":1})

successfull = 0
failed = 0
translator = Translator()
z = 0
for tweet in tweets:
    z += 1
    if z > 102:
        translatedTokens = []
        try:
            twitText = tweet["twitText"]
            translatedTwitText = translator.translate(tweet["twitText"], dest='en')

            for twitToken in tweet["twitTokens"]:
                translated = translator.translate(twitToken, dest='en')
                translatedTokens.append(translated.text)

            twits.update_one(
                {"twitId": tweet["twitId"]},
                    {
                    "$set": {
                        "twitTokens": translatedTokens,
                        "twitText": translatedTwitText.text
                    }
                }
            )
            successfull += 1
            print("successFulls : ", successfull)
        except:
            failed += 1
            print("faileds : ", failed)

print("Finished \n")
print("successFulls : ", successfull)
print("faileds : " , failed)

# Predict
