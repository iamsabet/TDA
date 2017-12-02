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
events = db.events

