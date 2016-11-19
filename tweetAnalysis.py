from textblob import TextBlob
from predictor import predict
import pickle


file = open("CityofSurrey_tweets.pk",'rb')
tweets = pickle.load(file)
print (len(tweets))


def get_tweets_forAgency(agency):
    for tweet in tweets:
        text = str(tweet[2])
        if "b'RT" not in text: 
            sentiment = TextBlob(text).sentiment.polarity
            if sentiment <= 0:
                if agency == predict(text):
                    print (text)

            


get_tweets_forAgency("ROADS")


