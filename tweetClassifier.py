import social
from datetime import date


twitter = social.TwitterApi()

#YYYY-MM-DD

since = date(2015, 1, 1)
until = date.today()

ids = []
tweets = (twitter.surrey_mentions(since = since, until = until, count = 100))
print len(tweets)
#print tweets

for tweet in tweets:
    ids.append(tweet.id)
    #print tweet.id

min_id = min(ids)
print "max"
print min_id
tweets = tweets + twitter.surrey_mentions(since = since, until = until, count = 100, max_id = min_id-1)
print len(tweets)


for tweet in tweets:
    print tweet.text
    print "**************************************"