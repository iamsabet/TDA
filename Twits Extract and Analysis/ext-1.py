import gzip
import email.utils
import datetime

f = gzip.open('D:\Euro2016\Euro2016_Tweets.txt.gz', 'r')
import pymysql
import pymysql.cursors
cnx = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='euro2016', charset='utf8',cursorclass = pymysql.cursors.SSCursor)
import  json
cursor=cnx.cursor()
#path = "D://Euro2016//euro2016.json"
#jsonfiles=open (path,encoding='utf8',mode='w')
insert_tweet = ("INSERT INTO euro "
                "(publicationTime, title) "
                "VALUES (%(publicationTime)s, %(title)s)")
for line in f:

    try:
        line_in = line.decode().split(';')  # Split string to list on semicolon
        line_in = [x.rstrip() for x in line_in]  # strip whitespace from the right of each element
        parts = email.utils.parsedate_tz(line_in[0])
        dt = datetime.datetime(*parts[:6]) - datetime.timedelta(seconds=parts[-1])
        tweet_data = {
            'title': line_in[1],
            'publicationTime': str(dt),
        }
        cursor.execute(insert_tweet, tweet_data)
        cnx.commit()
        print(line_in[0]+"\n"+line_in[1])
        #jsonfiles.writelines(line_in)
    except:
        continue
#Now push the line to a database table or whatever else you want to do with it.
cursor.close()
