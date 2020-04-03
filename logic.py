'''
    Manuel Hernández (@manherna) 03/04/2020 
    This script handles all the logic of the game, including start, polling for users and a reason to kill
    and managing state update thorugh given persistence.

    This logic is implemented to be called by a AWS Lambda function, so each time it is called it will be initialized
    and will handle one update. 
'''

import csv
import random
import time
from persistence import Persistence
from models import KillReason, User
from logger import Logger


class Logic:
    def __init__(self, persistance: Persistence, logger: Logger):
        self.persistance =  persistance
        self.logger = logger
        print ("---------------------- Logic started ----------------------")
    
    def Update(self):
        if (self.IsGameFinished() is not True):
            # A Winner and loser is picker randomly by persistence system
            winner, loser = self.persistance.GetTwoRandomUsers()
            # A random reason is picked
            reason = self.persistance.GetRandomReason()

            # State update for loser, winner and reason used
            loser.isActive = False 
            winner.kills = winner.kills + 1 
            winner.isActive = True
            reason.isActive = False
            
            # State saving 
            if (self.persistance.UpdateUserStatus(loser) is not True):
                print("Something went wrong updating loser status")
            if(self.persistance.UpdateUserStatus(winner) is not True):
                print("Something went wrong updating winner status")
                            
            if(self.persistance.UpdateReasonStatus(reason) is not True):
                print("Something went wrong updating kill reason status")

            # Notify through given logger who killed who and why
            killstr = str(winner.name + " " +  reason.text + " " +  loser.name)
            self.logger._print(killstr)

            # After each round we should check if the game was finished
            if(self.IsGameFinished()):
                # Get the last user and print it (doesn't matter if it's random, as it is the last active user)
                lastU = self.persistance.GetRandomActiveUser()
                self.logger._print(lastU.name + ' ha ganado el Fisicas Battle Royale!')
                
                # Calculate kill podium and output it as well
                podium = self.persistance.GetKillsPodium()
                self.logger._print("Podium de asesinatos:\n 1º %s con %d \n 2º %s con %d\n 3º %s con %d" % (podium[0].name, podium[0].kills,podium[1].name, podium[1].kills,podium[2].name, podium[2].kills))

    def IsGameFinished(self):
        return (self.persistance.GetActiveUsersCount() == 1)