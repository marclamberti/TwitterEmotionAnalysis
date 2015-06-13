import sys
import twitter.TwitterManager as Twitter

""" Main entry point for the script """
def main():
    twitterManager = Twitter.TwitterManager()
    sr = twitterManager.makeSearchRequest(["France"])
    twitterManager.getTweetFromSearchRequest(sr, 5)
    print('Number of tweets gathered: %d' % len(twitterManager.tweets))
    for tweet in twitterManager.tweets:
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

if __name__ == '__main__':
    sys.exit(main())
