from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from pymongo import MongoClient
import remove_emoji
import gzip
import email.utils
import datetime
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)

client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
z = 0
f = gzip.open('/home/sabet/Desktop/twitsDb/Euro2016_Tweets.txt.gz', 'r')
for line in f:
    try:
        line_in = line.decode().split(';')  # Split string to list on semicolon
        line_in = [x.rstrip() for x in line_in]  # strip whitespace from the right of each element
        parts = email.utils.parsedate_tz(line_in[0])
        dt = datetime.datetime(*parts[:6]) - datetime.timedelta(seconds=parts[-1])

        z = z + 1
        twitText = line_in[1].lower()
        removedEmojiesText = remove_emoji.remove_emoji(twitText)
        word_tokens = word_tokenize(removedEmojiesText)
        hashtagsList = []
        lemetizedList = []
        if z % 1000 == 0:
            print(z)
            print(line_in)
        i = 0
        for x in word_tokens :
            if not lemetizedList.__contains__(x):
                lemetizedList.append(lmtzr.lemmatize(x))
            if x == '#':
                if i+1 != len(word_tokens):
                    if not hashtagsList.__contains__(word_tokens[i+1]):
                        hashtagsList.append(word_tokens[i+1])
            i = i + 1
        stop_words = set(stopwords.words('english'))
        filtered_sentence = []
        for w in lemetizedList:
            if w not in stop_words:
                if len(w) > 1 and not w.startswith('/'):
                    removedUrlText = re.sub(r'http.*$', "", w)
                    if removedUrlText != '':
                        if not filtered_sentence.__contains__(removedUrlText):
                            filtered_sentence.append(removedUrlText)

        data = {
            'twitId': z,
            'twitText': twitText,
            'twitDate': ((dt - epoch).total_seconds() * 1), # /seconds -- >  *1000 = ms
            'twitHashtags': hashtagsList ,
            'twitTokens': filtered_sentence,
            'tokensFeeling': [],
            'NegativeFeelings': 0,
            'positiveFeelings': 0,
        }
        result = twits.insert_one(data)
        if z % 1000:
            print(z)
            print(' twits inserted')
    except:
        print("failed")

