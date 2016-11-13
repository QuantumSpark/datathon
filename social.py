from twitter.api import Api
from datetime import datetime
from urllib import quote

TWITTER_AUTH = {
    'consumer_key': 'EyiAckD8mrBDYQyUsDOV4oJR1',
    'consumer_secret': 'bUhd8f41wZaFKHoJFwIPhbwuvm8zzQnersO47b4SyeuhZ9Xa3h',
    'access_token_key': '215525968-ocHo0kyrS5q2DGSGUqNmKEI7BhRKeFxYOdLia8ix',
    'access_token_secret': 'IhDJdGOpeiHmC5Hqhmq5aOOnN7gNNyiwKbxqPYL3GpGpH'}

class TwitterApi(object):
    def __init__(self, user='CityofSurrey', lat=49.124576, lng=-122.790747, rad='10km'):
        self.__api = Api(**TWITTER_AUTH)
        self.user = user
        self.lat = lat
        self.lng = lng
        self.rad = rad
        self.__geocode = '{0},{1},{2}'.format(lat, lng, rad)

    def surrey_mentions(self, since=None, until=None):
        """
        Returns tweets mentioning City of Surrey between optional since/until
        parameters. `since` and `until` are datetime objects.
        """
        params = {'to': self.user}
        if since: params['since'] = self.__format_date(since)
        if until: params['until'] = self.__format_date(until)

        return self.__api.GetSearch(raw_query=self.__construct_query(**params))

    def surrey_location(self, since=None, until=None):
        """
        Returns tweets sent from within the City of Surrey between optional since/until
        parameters. `since` and `until` are datetime objects.
        """
        params = {'geocode': self.__geocode}
        if since: params['since'] = self.__format_date(since)
        if until: params['until'] = self.__format_date(until)

        return self.__api.GetSearch(raw_query=self.__construct_query(**params))

    def __construct_query(self, **kwargs):
        return reduce(lambda q, p: q + quote('{0}:{1} '.format(p[0], p[1])), kwargs.items(), 'q=')

    def __format_date(self, dt):
        return dt.strftime('%Y-%m-%d')
