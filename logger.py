'''
    Manuel Hernández (@manherna) 03/04/2020 
    Logger classes are used by the logic of the game to notify
    changes in game status.
    There are currently 2 implementations of Loggers:
        ConsoleLogger: Used mainly for debugging code locally
        TweetLogger: Used to update the game status in twitter
'''

import tweepy
import yaml
class Logger ():
    def _print(self, str):
        pass

class ConsoleLogger(Logger):
    def __init__(self):
        pass
    def _print(self, str):
        print(str)

class TweetLogger(Logger):
    def __init__(self, config_yaml_url):
        with open(config_yaml_url) as config_yaml:
            cfg = yaml.load(config_yaml, Loader=yaml.Loader)

        consumer_key = cfg["tweepy"]["consumer_key"]
        consumer_secret = cfg["tweepy"]["consumer_secret"]
        access_token = cfg["tweepy"]["access_token"]
        access_token_secret = cfg["tweepy"]["access_token_secret"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, 
            wait_on_rate_limit_notify=True)
        try:
            self.api.verify_credentials()
        except Exception as e:
            print("Error creating API")
            raise e
        print ("---------------------- API Started ----------------------")

    def _print(self, str):
        print ("---------------------- Tweeting ----------------------")
        self.api.update_status(str)