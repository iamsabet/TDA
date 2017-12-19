from __future__ import division, unicode_literals

import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from itertools import islice
import datetime
import tokenize
from threading import Thread
import nltk
import tfidf
import math
import tf as tf
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob as textBlob
from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

lmtzr = WordNetLemmatizer()
epoch = datetime.datetime.utcfromtimestamp(0)
client = MongoClient('mongodb://localhost:27017')
db = client.twitsDb
twits = db.twits
translatedTweets = db.translatedTweets
events = db.events



class tfIdf():
    def tf_idf(self):
        z = 0
        left = 1468168200000
        right = 1468177200000
        tops = []
        step = 120000  # 2 Minute Window
        for x in range(0, 74):
            right = left + step
            tweets = translatedTweets.find({"tweetMiliSeconds": {"$gt": left, "$lt": right}},
                                           {"tweetTokens": 1, "tweetHashtags": 1, "tweetMiliSeconds": 1, "tweetText": 1})
            left = left + step
            document = ""
            title = str(x)
            print(left, right)
            z = 0
            for tweet in tweets:
                z += 1
                print(z)
                document += tweet["tweetText"]

            print("x:) - ", x, "-", document)
            if document != "":
                cleaned_document = tfidf.clean_document(document)
                doc = tfidf.remove_stop_words(cleaned_document)
                data = [' '.join(document)]
                # Merge corpus data and new document data
                train_data = set(data + [doc])

                count_vect = CountVectorizer()
                count_vect = count_vect.fit(train_data)
                freq_term_matrix = count_vect.transform(train_data)
                feature_names = count_vect.get_feature_names()
                print(feature_names)
                tfidff = TfidfTransformer(norm="l2")
                tfidff.fit(freq_term_matrix)

                # Get the dense tf-idf matrix for the document
                story_freq_term_matrix = count_vect.transform([doc])

                story_tfidf_matrix = tfidff.transform(story_freq_term_matrix)
                story_dense = story_tfidf_matrix.todense()
                doc_matrix = story_dense.tolist()[0]

                top_sents = tfidf.rank_sentences(doc, doc_matrix, feature_names)
                print(doc_matrix.index(top_sents[0][0]))
                summary = '.'.join([cleaned_document.split('.')[i]
                                    for i in [pair[0] for pair in top_sents]])
                summary = ' '.join(summary.split())
                print(summary)

        f = 1
        for x in tops:
            print(f," ) ",x)


if __name__ == '__main__':
    obj = tfIdf()        # 74 * 2minutes ==> 148 reltive -> 120+3 // 9 to 11:30pm 07-10-2016
    obj.tf_idf()
    print("Finished")




