from flask import Flask
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from pymongo import MongoClient
import string
import remove_emoji
from random import *
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
     db = pymysql.connect(host='localhost', port=3306, user='root',password='147852' ,db='twitsDb')
     query = ("select twitId,twitText,twitDate FROM twitsDatas where twitId < 100000")
     cur = db.cursor(pymysql.cursors.DictCursor)
     cur.execute(query);
     if cur:
         for row in cur:
            print(z)
            z = z + 1
            twitText = row['twitText'].lower()
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
            print('filtered Scentence : ')
            print(filtered_sentence)
            print('hashtagsList : ')
            print(hashtagsList)
            min_char = 10
            max_char = 16
            allchar = string.ascii_letters + string.punctuation + string.digits
            password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
            data = {
                'twitId': password,
                'twitText': row['twitText'],
                'twitDate': ((row['twitDate'] - epoch).total_seconds() * 1), # /seconds -- >  *1000 = ms
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

     return jsonify(z)

if __name__ == '__main__':
    app.run()
