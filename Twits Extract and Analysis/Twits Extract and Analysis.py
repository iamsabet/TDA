from flask import Flask
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import remove_emoji
from pymongo import MongoClient
import aniso8601
client = MongoClient()

import pymysql
cnx = pymysql.connect(host='localhost', port=3306, user='root', passwd='147852', db='twitsDb', charset='utf8',cursorclass = pymysql.cursors.SSCursor)
import  json
cursor=cnx.cursor()
client = MongoClient('mongodb://localhost:27017')
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Twits Extract and Analysis'


@app.route('/extractor')
def extractor():
     x = 0
     db = pymysql.connect(host='localhost', port=3306, user='root',password='147852' ,db='twitsDb')
     query = ("select twitId,twitText,twitDate FROM twitsDatas where twitId < 500")
     cur = db.cursor(pymysql.cursors.DictCursor)
     cur.execute(query);
     if cur:
         for row in cur:
            print(x)
            twitText = row['twitText']
            removedEmojiesText = remove_emoji.remove_emoji(twitText)
            word_tokens = word_tokenize(removedEmojiesText)
            hashtagsList = []
            i = 0 ;
            for x in word_tokens :
                if(x == '#'):
                    if(not hashtagsList.__contains__(word_tokens[i+1])):
                        hashtagsList.append(word_tokens[i+1])
                i = i + 1
            stop_words = set(stopwords.words('english'))
            filtered_sentence = []
            for w in word_tokens:
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
            data = {
                'twitId': row['twitId'],
                'twitText': row['twitText'],
                'twitDate': aniso8601.parse_datetime((row['twitDate'])),
                'twitHashtags':hashtagsList,
                'twitTokens': filtered_sentence,
                'tokensFeeling': [],
                'NegativeFeelings': 0,
                'positiveFeelings': 0,
            }
            db = client.twitsDb
            twits = db.twits
            result = twits.insert_one(data)
            print('One post -'.format(result.inserted_id))

     return jsonify(x)



if __name__ == '__main__':
    app.run()
