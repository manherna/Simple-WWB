'''
    Manuel Hernández (@manherna) 03/04/2020 
    Lambda function consumed by AWS Lambda.

    Each time it is called, it loads the current state of the game
    and performs a single update.

'''

from logic import Logic 
from logger import TweetLogger, ConsoleLogger
from persistence import DBPersistence
from time import sleep

def lambda_handler(event, context):
    dbPers = DBPersistence("config.yaml")
    twlogger = TweetLogger("config.yaml")
    logic = Logic(dbPers, twlogger)

    if (logic.IsGameFinished() is not True):
        logic.Update()
    else:
        print ("Game already finished")
    return 200
