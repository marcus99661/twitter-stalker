from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

import twitter_credentials

false = "false"
true = "true"
null = "null"

def twitter_text(data):
    full_tweet = eval(data) ### full_tweet is the entire tweet in a dictionary
    '''
    ENTER NEW FUNCTIONS HERE
    '''

class TwitterStreamer():
    
    def stream_tweets(self, fetched_tweets_filename): 
        listener = StdOutListener(fetched_tweets_filename)
        
        while True:
            try:
                auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
                auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)       
                stream = Stream(auth, listener)
#                stream.filter(track=["hashtag1", "hashtag2"]) ### Filter by hashtags
                stream.filter(follow=["TWITTER_ACCOUNT_ID"]) ### Filter by specific Twitter acount in real-time. Get the account Twitter ID here:https://tweeterid.com/ 
            except Exception as e: ### If "Read timed out" error occures reconnect in 15min
                print(e)
                time.sleep(60 * 15)
                continue
    
class StdOutListener(StreamListener):
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            twitter_text(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    
    def on_error(self, status):
        if status == 420:
            print(status)
            print("ERROR 420")
            # Returning False on_data method in case rate limit occurs.
            return False
        else:
            print(status)
        
if __name__ == "__main__":
    
#    hash_tag_list = ["databreach", "dataleak"]
    fetched_tweets_filename = "tweets.json"
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename)
