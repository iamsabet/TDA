from googletrans import Translator
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import re
from pymongo import MongoClient
import remove_emoji
import datetime
from nltk.stem.wordnet import WordNetLemmatizer


lmtzr = WordNetLemmatizer()

epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
translatedTweets = db.translatedTweets
events = db.events

tweets = twits.find({"twitHashtags": {
    "$in": ["1-0", "portugal", "cr7", "cristianoronaldo", "ronaldo", "pepe", "por", "france", "fra", "euro2016",
            "final", "porfra", "frapor"]},
                     "twitmiliSeconds": {"$gt": 1468168200000, "$lt": 1468704600000}},
                    {"twitTokens": 1, "twitmiliSeconds": 1, "twitId": 1,
                     "twitText": 1, "twitDate": 1,"twitHashtags":1})

successfull = 0
failed = 0
translator = Translator()
z = 0
for tweet in tweets:
    z += 1
    translatedTokens = []
    stop_words = set(stopwords.words('english'))
    try:
        ids = tweet["twitId"]
        translatedTwitText = translator.translate(tweet["twitText"], dest='en')



    except:
        failed += 1
        print("fails : ", failed)
        print("successfuls : ", successfull)


print("Finished")
print("successes : ", successfull)
print("fails : ", failed)



