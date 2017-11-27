from flask import Flask
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from pymongo import MongoClient
import string
import remove_emoji
import gzip
import email.utils
import datetime
import datetime
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)
client = MongoClient()

import pymysql
cnx = pymysql.connect(host='localhost', port=3306, user='root', passwd='147852', db='twitsDb', charset='utf8',cursorclass = pymysql.cursors.SSCursor)
cursor=cnx.cursor()
client = MongoClient('mongodb://localhost:27017')
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Twits Extract and Analysis'


@app.route('/extractor')
def extractor():
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
            i = 0 ;
            for x in word_tokens :
                if(not lemetizedList.__contains__(x)):
                    lemetizedList.append(lmtzr.lemmatize(x))
                if(x == '#'):
                    if(i+1 != len(word_tokens)):
                        if(not hashtagsList.__contains__(word_tokens[i+1])):
                            hashtagsList.append(word_tokens[i+1])
                i = i + 1
            stop_words = set(stopwords.words('english'))
            filtered_sentence = []
            for w in lemetizedList:
                if w not in stop_words:
                    if len(w) > 1 and not w.startswith('/'):
                        removedUrlText = re.sub(r'http.*$', "", w);
                        if(removedUrlText != ''):
                            if(not filtered_sentence.__contains__(removedUrlText)):
                                filtered_sentence.append(removedUrlText)
            if(z % 1000 == 0):
                print(z)
            data = {
                'twitId': z,
                'twitText': twitText,
                'twitDate': ((str(dt) - epoch).total_seconds() * 1), # /seconds -- >  *1000 = ms
                'twitHashtags': hashtagsList ,
                'twitTokens': filtered_sentence,
                'tokensFeeling': [],
                'NegativeFeelings': 0,
                'positiveFeelings': 0,
            }
            db = client.twitsDb
            twits = db.twits
            result = twits.insert_one(data)
            print('One post -'.format(result.inserted_id))
         except :
             print("failed")

     return jsonify(z)

if __name__ == '__main__':
    app.run()
