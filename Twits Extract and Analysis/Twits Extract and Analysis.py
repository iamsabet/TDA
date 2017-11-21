from flask import Flask
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import remove_emoji
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from nltk.stem import WordNetLemmatizer

import pymysql
app = Flask(__name__)


userpass = 'mysql+pymysql://root:@'
basedir  = '192.168.53.236'
dbname   = '/soccer'
socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
db = SQLAlchemy(app)


engine = sqlalchemy.create_engine('mysql+pymysql://root:147852@localhost/soccer')

@app.route('/')
def hello_world():
    return 'Twits Extract and Analysis'


@app.route('/cleaner')
def cleaner():
    lem = WordNetLemmatizer()
    result = engine.execute('select eventText FROM soccerevents')
    if result:
        for x in result:
            print('Remove Stop Words , Emojies , Emoticons , Urls ... and tokenize')
            twitText = x[0]
            print(twitText)  # with     emojies
            removedEmojiesText = remove_emoji.remove_emoji(twitText)
            print(removedEmojiesText)
            word_tokens = word_tokenize(removedEmojiesText)
            print(word_tokens)

            stop_words = set(stopwords.words('english'))
            print(stop_words)
            filtered_sentence = []
            for w in word_tokens:
                if w not in stop_words:
                    if len(w) > 1 and not w.startswith('/'):
                        removedUrlText = re.sub(r'http.*$', "", w);
                        if(removedUrlText != ''):
                            filtered_sentence.append(removedUrlText)

            print('Word tokens : ')
            print(word_tokens)
            print('filtered Scentence : ')

            stempedlist = []
            for i in word_tokens:
                stemword=lem.lemmatize(i)
                stempedlist.append(stemword)

            print(stempedlist)



    return jsonify(filtered_sentence)


if __name__ == '__main__':
    app.run()
