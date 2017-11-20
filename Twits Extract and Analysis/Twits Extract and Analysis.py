from flask import Flask
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import remove_emoji
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


userpass = 'mysql+pymysql://root:@'
basedir  = '192.168.43.138'
dbname   = '/soccer'
socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Twits Extract and Analysis'


@app.route('/cleaner')
def cleaner():
    if db.session.query('1').from_statement('1').all():
        print(db.session.query('*').from_statement('eventText').all())
        return 'It works.'
    else:
        return 'Something is broken.'

    # query to get specific list of twits ...
    # list of strings we play here ... :
    # mockedData ...
    print('Remove Stop Words , Emojies , Emoticons , Urls ... and tokenize')
    twitText = "Whadddddupppp United fans. Do you remember http://web.ali.com that time when you lost 4-0 at the Bridge and you came back a year later and were lucky enough to only lose 1-0? "
    print(twitText)  # with     emojies
    removedEmojiesText = remove_emoji.remove_emoji(twitText)
    word_tokens = word_tokenize(removedEmojiesText)
    print(word_tokens)

    stop_words = set(stopwords.words('english'))
    print(stop_words)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
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
    print(filtered_sentence)

    return jsonify(filtered_sentence)


if __name__ == '__main__':
    app.run()
