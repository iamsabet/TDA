from flask import Flask
import re
import remove_emoji
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Twits Extract and Analysis'

@app.route('/cleaner')
def cleaner():
    # query to get specific list of twits ...
    # list of strings we play here ... :
    # mockedData ...
    print('Remove Stop Words , Emojies , Emoticons , Url')
    twitText = "hello i have :'((( :(((( just seen it shiiiittt :) https://example.com/some"
    print(twitText)  # with emojies
    removedEmojiesText  = remove_emoji.remove_emoji(twitText)
    print(removedEmojiesText) # removed emojies
    wordsArray = removedEmojiesText.split(' ');
    removedURLs = [];
    y = 0 ;
    for x in range (0,len(wordsArray)): # remove emoticons and urls both
        removedUrlText = re.sub(r':.*$', "", wordsArray[x])
        print(removedURLsgi)
        if removedUrlText!="":
            removedURLs.append(wordsArray[x]);
            y += 1;

    print(removedURLs); # remove urls

    print(len(removedURLs))  # removed emojies -- emoticons and smileis like :) - :( mus be removed too

    return 'Twits Extract and Analysis'

if __name__ == '__main__':
    app.run()
