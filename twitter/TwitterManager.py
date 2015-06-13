from TwitterSearch import *
import ConfigParser
import time

"""
Class used to manage the TwitterSearch library
"""
class TwitterManager(object):

    """
    Initialize a connection by instanciating a TwitterSearch object
    using the parameters given in your config file.
    If an error is encountered an exception is raised.
    If you haven't created your configuration file yet, just create a new file
    in the main directory and copy and past the following lines with
    your information:
    [twitter]
    consumer_key =
    consumer_secret =
    access_token =
    access_token_secret =
    """
    def __init__(self, filename="config.cfg"):
        try:
            config = ConfigParser.ConfigParser()
            config.read(filename)
            consumer_key        = config.get("twitter", "consumer_key")
            consumer_secret     = config.get("twitter", "consumer_secret")
            access_token        = config.get("twitter", "access_token")
            access_token_secret = config.get("twitter", "access_token_secret")
            self.ts = TwitterSearch(consumer_key, consumer_secret, access_token, access_token_secret)
            self.requests_limit = None
        except TwitterSearchException as e:
            print(e)
            raise

    """
    Create a search request to get tweets according to the keywords given
    as parameters (must be a list) and the language in what we want to get them.
    A list of available language is given in the code of the TwitterSearch library
    in the TwitterSearchOrder.py file.
    tweets_per_page has to be from 1 to 100.
    result_type mixed meaning both recent and popular tweets.
    Return the search request
    """
    def makeSearchRequest(self, keywords, tweets_per_page=100, language='en'):
        try:
            tso = TwitterSearchOrder()
            tso.set_keywords(keywords)
            tso.set_language(language)
            tso.set_count(tweets_per_page)
            tso.set_include_entities(False)
            tso.set_result_type('mixed')
        except TwitterSearchException as e:
            print(e)
        return tso

    """
    Callback used to avoid being rate-limited by twitter
    Every 5th call to the twitter API, the callback activates a delay of
    60 seconds.
    """
    def avoidRateLimit(self, current_ts_instance):
        waiting_time = 60
        queries, tweets_seen = current_ts_instance.get_statistics()
        if self.requests_limit and queries > self.requests_limit:
            print('Number of limited requests reached : %d' % self.requests_limit)
            self.stop_gathering_tweet = True
        else:
            print('Tweets gathered... queries: %d' % queries)
            if queries > 0 and (queries % 5) == 0:
                print('Wait %ds to avoid being rate-limited...' % waiting_time)
                time.sleep(waiting_time)

    """
    Get tweets from a search request.
    """
    def getTweetFromSearchRequest(self, request, requests_limit=None):
        self.tweets                 = []
        self.requests_limit         = requests_limit
        self.stop_gathering_tweet   = False
        try:
            for tweet in self.ts.search_tweets_iterable(request, callback=self.avoidRateLimit):
                if self.stop_gathering_tweet == True:
                    break
                self.tweets.append(tweet)
        except TwitterSearchException as e:
            if e.code == 1011:
                print("No more tweets to get")
            else:
                print (e)
        return self.tweets
