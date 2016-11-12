from twitter.api import Api
from datetime import datetime
from urllib import quote

TWITTER_AUTH = {
    'consumer_key': 'EyiAckD8mrBDYQyUsDOV4oJR1',
    'consumer_secret': 'bUhd8f41wZaFKHoJFwIPhbwuvm8zzQnersO47b4SyeuhZ9Xa3h',
    'access_token_key': '215525968-ocHo0kyrS5q2DGSGUqNmKEI7BhRKeFxYOdLia8ix',
    'access_token_secret': 'IhDJdGOpeiHmC5Hqhmq5aOOnN7gNNyiwKbxqPYL3GpGpH'}

class TwitterApi(object):
    def __init__(self):
        self.__api = Api(**TWITTER_AUTH)
        self.__user = 'CityofSurrey'

    def surrey_mentions(self, since=None, until=None):
        """
        Returns tweets mentioning City of Surrey between optional since/until
        parameters. `since` and `until` are datetime objects.
        """
        params = {'to': self.__user}
        if since: params['since'] = since
        if until: params['until'] = until

        return self.__api.GetSearch(raw_query=self.__construct_query(**params))

    def __construct_query(self, **kwargs):
        return reduce(lambda q, p: q + quote('{0}:{1}'.format(p[0], p[1])), kwargs.items(), 'q=')

t = TwitterApi()

print t.surrey_mentions()
