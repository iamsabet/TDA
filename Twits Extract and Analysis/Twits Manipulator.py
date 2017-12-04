from pymongo import MongoClient
import datetime
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.classify import NaiveBayesClassifier
from googletrans import Translator
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
events = db.events

tweets = twits.find({"twitHashtags": {"$in": ["1-0","portugal", "cr7", "cristianoronaldo", "ronaldo", "pepe", "por", "france", "fra",
            "euro2016", "final", "amp", "supporting", "euro" , "support"]},
            "twitmiliSeconds": {"$gt": 1468108920000, "$lt": 1468117860000}}, {"twitTokens": 1, "twitmiliSeconds": 1, "positiveFeelings" : 1, "NegativeFeelings": 1, "twitId" : 1})
print(tweets)
x = 0
translator = Translator()
for tweet in tweets:
        translateds = translator.translate(tweet["twitTokens"], dest='en')
        for translated in translateds:
            print(translated.text)
            x += 1

# Predict
