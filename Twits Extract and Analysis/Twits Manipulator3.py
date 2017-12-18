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
                     "twitmiliSeconds": {"$gt": 1468838760000, "$lt": 1469375160000}},
                    {"twitTokens": 1, "twitmiliSeconds": 1, "twitId": 1,
                     "twitText": 1, "twitDate": 1,"twitHashtags":1,"$maxScan":1000000000000,"$max":1000000000000})
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
                'tweetText': translated,
                'tweetTokens': filtered_sentence,
                'tweetMiliSeconds': tweet["twitmiliSeconds"],
                'tweetDate': tweet["twitDate"],
                'tweetHashtags': tweet["twitHashtags"],
                'posFeeling': posFeeling,
                'negFeeling': negFeeling,
                'compoundFeeling': compoundFeeling,
                'neuFeeling': neuFeeling
        }

        translatedTweets.insert_one(data, "twitId = :", ids)
        successfull += 1

    except:
        failed += 1
        print("fails : ", failed)
        print("successfuls : ", successfull)


print("Finished")
print("successes : ", successfull)
print("fails : ", failed)



