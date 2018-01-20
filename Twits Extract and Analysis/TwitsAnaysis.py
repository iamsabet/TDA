from googletrans import Translator
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
# 134100000
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
hashtags4 = ["germany", "euro2016", "euro", "gerita","itager","itagerman","italy", "itavsger", "gervsita", "italyvsgermany","italyvsgerman","captain","soon","goal","score","scores","penalty","penalties","shoot","miss","misses","german","germanyvsitaly","1-1","shot","germanitaly","save","greate","luck"]
hashtags1 = ["por","porfra","frapor","porvsfra","fravspor","france","cr7","ronaldo","cristiano","cris","cristianoronaldo","portugal","francevsportugal","euro","euro2016","portugalvsfrance","1-0","goal","final","finale","2016","eurofinal","win","wins","champion","winner","cup","tonight"]


def twitsManipulator(left, right):
    tweets = twits.find({"twitmiliSeconds": {"$gt": left, "$lt": right}},
    {"twitDate": 1,"twitmiliSeconds": 1, "twitHashtags": 1, "twitText": 1, "twitId": 1})
    successfull = 0
    failed = 0
    translator = Translator()
    z = 0
    for tweet in tweets:
        z += 1
        stop_words = set(stopwords.words('english'))
        try:
            ids = tweet["twitId"]
            translatedTwitText = translator.translate(tweet["twitText"], dest='en')
            translated = translatedTwitText.text
            removedEmojiesText = remove_emoji.remove_emoji(translated)
            word_tokens = word_tokenize(removedEmojiesText)
            lemetizedList = []
            sid = SentimentIntensityAnalyzer()
            removedUser = re.sub(r'@.*$', "", translated)
            ss = sid.polarity_scores(removedUser)
            posFeeling = ss["pos"]
            negFeeling = ss["neg"]
            compoundFeeling = ss["compound"]
            neuFeeling = ss["neu"]
            i = 0
            for x in word_tokens:
                if not lemetizedList.__contains__(x):
                    lemetizedList.append(lmtzr.lemmatize(x))
                i = i + 1
            filtered_sentence = []
            for w in lemetizedList:
                if w not in stop_words:
                    if len(w) > 2 and not w.startswith('/'):
                        removedUrlText = re.sub(r'http.*$', "", w)
                        if removedUrlText != '':
                            if not filtered_sentence.__contains__(removedUrlText):
                                filtered_sentence.append(removedUrlText)
            data = {
                'tweetId': ids,
                'tweetText': removedUser,
                'tweetTokens': filtered_sentence,
                'tweetMiliSec onds': tweet["twitmiliSeconds"],
                'tweetDate': tweet["twitDate"],
                'tweetHashtags': tweet["twitHashtags"],
                'posFeeling': posFeeling,
                'negFeeling': negFeeling,
                'compoundFeeling': compoundFeeling,
                'neuFeeling': neuFeeling
            }
            translatedTweets.insert_one(data)
            successfull += 1
            print("successfulls : ", successfull)

        except:
            failed += 1
            print("fails : ", failed)
            print("Thread ", left, right, " -- ", "successfuls : ", successfull)

    print("Finished")
    print("Thread ", left, right, " -- ", "successfuls : ", successfull)
    print("fails : ", failed)
