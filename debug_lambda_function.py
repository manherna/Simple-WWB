'''
    Script used for local testing of the bot
'''
from logic import Logic
from logger import TweetLogger, ConsoleLogger
from persistence import DBPersistence
from time import sleep

def lambda_handler(event, context):
    dbPers = DBPersistence("config.yaml")
    twlogger = ConsoleLogger()
    #TweetLogger("config.yaml")
    logic = Logic(dbPers, twlogger)

    while (logic.IsGameFinished() is not True):
        logic.Update()
    else:
        print ("Game already finished")
    return 200

if __name__ == "__main__":
    lambda_handler(None, None)