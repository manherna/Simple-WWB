'''
    Manuel Hernández (@manherna) 03/04/2020 
    Models used by the persistence and logic.
'''



class User ():
    def __init__ (self, id, name, isActive, kills):
        self.id = id
        self.name = name
        self.isActive = isActive
        self.kills = kills

class KillReason():
    def __init__ (self, id, killreason_text, isActive):
        self.id = id
        self.text = killreason_text
        self.isActive = isActive