from twitter.api import Api
import csv
from datetime import date

#Twitter API credentials
TWITTER_AUTH = {
    'consumer_key': 'EyiAckD8mrBDYQyUsDOV4oJR1',
    'consumer_secret': 'bUhd8f41wZaFKHoJFwIPhbwuvm8zzQnersO47b4SyeuhZ9Xa3h',
    'access_token_key': '215525968-ocHo0kyrS5q2DGSGUqNmKEI7BhRKeFxYOdLia8ix',
    'access_token_secret': 'IhDJdGOpeiHmC5Hqhmq5aOOnN7gNNyiwKbxqPYL3GpGpH'}


def get_all_tweets(screen_name):
    api = Api(**TWITTER_AUTH)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.GetSearch(term=screen_name, count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.GetSearch(term = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
    #write the pickle
    with open('%s_tweets.pk' % screen_name, 'wb') as f:
        import pickle
        pickle.dump(outtweets, f, protocol = 2)
    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass


if __name__ == '__main__':
    get_all_tweets("CityofSurrey")
