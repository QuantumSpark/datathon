import social
from datetime import date


twitter = social.TwitterApi()

since = date(2016, 6, 1)
until = date.today()

tweets = twitter.surrey_mentions(since = since, until = until)
print type(tweets[0])

for tweet in tweets:
    print tweet.text