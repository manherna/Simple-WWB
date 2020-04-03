'''
    Manuel Hernández (@manherna) 03/04/2020 
    Persistenece classes are used by the game to save the status of the game
    There is currently 1 implementation of Persistence:
        DBPersistence: Uses mysql-connector to fetch and update changes in a mysql database
'''
import yaml
import mysql.connector
from models import User, KillReason

class Persistence():
    def GetRandomReason(self):
        pass
    def GetRandomActiveUser(self):
        pass
    def GetTotalUsersCount(self):
        pass
    def GetTwoRandomUsers(self):
        pass
    def GetActiveUserIdList(self):
        pass
    def GetActiveUsersCount(self):
        pass
    def GetKillsPodium(self):
        pass
    def UpdateUserStatus(self, user: User):
        pass
    def UpdateReasonStatus(self, killreason: KillReason):
        pass

   

class DBPersistence(Persistence):
    def __init__(self, config_yaml_url):
        with open(config_yaml_url) as config_yaml:
            cfg = yaml.load(config_yaml, Loader=yaml.Loader)

        self.host=cfg["mysql"]["host"]
        self.user=cfg["mysql"]["user"]
        self.passwd=cfg["mysql"]["passwd"]
        self.db=cfg["mysql"]["db"]

    def GetRandomReason(self):
        query = "SELECT * FROM killreasons ORDER BY killreason_active DESC, RAND() LIMIT 1"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            return KillReason(res[0][0], res[0][1], res[0][2])
    
    def GetRandomActiveUser(self):
        query = "SELECT * FROM participants WHERE (participant_active = 1) ORDER BY RAND() LIMIT 1"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            return User(res[0][0], res[0][1], res[0][2], res[0][3])
  
  
    def GetTotalUsersCount(self):
        query = "SELECT COUNT(id) FROM participants"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            return int(res[0][0])

    def GetTwoRandomUsers(self):
        query = "SELECT * FROM participants WHERE (participant_active = 1) ORDER BY RAND() LIMIT 2"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            return User(res[0][0], res[0][1], res[0][2], res[0][3]), User(res[1][0], res[1][1], res[1][2], res[1][3])
           
            
    def GetActiveUserIdList(self):
        query = "SELECT id FROM participants WHERE participant_active = 1"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            return [t [0] for t in res]

    def GetActiveUsersCount(self):
        query = "SELECT COUNT(id) FROM participants WHERE participant_active = 1"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            return int(res[0][0])
        
    def GetKillsPodium(self):
        query = "SELECT * FROM innodb.participants ORDER BY kills DESC LIMIT 3"
        res = self._executeQuery(query)
        if res is None:
            return -1
        else:
            podium = []
            for x in res:
                podium.append(User(x[0], x[1], x[2], x[3]))
            return podium

    def UpdateUserStatus(self, user: User):
        query = str("UPDATE participants SET participant_name = '%s', participant_active = %d, kills = %d WHERE (id = %d)" % (user.name, int(user.isActive), user.kills, user.id))
        res = self._executeQuery(query)
        if res == []:
            return True
        else:
             return False

    def UpdateReasonStatus(self, killreason: KillReason):
        query = str("UPDATE killreasons SET killreason_text = '%s', killreason_active = %d WHERE (id = %d)" % (killreason.text, int(killreason.isActive), killreason.id))
        res = self._executeQuery(query)
        if res == []:
            return True
        else:
             return False

    def _getDBConnection(self):
        try:
            db_conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.db
            )
            return db_conn
        except mysql.connector.Error as err:
            print(err)
            return 0

    def _executeQuery(self, query):
        db = self._getDBConnection()
        if db is not 0:
            db_cursor = db.cursor()
            try:
                db_cursor.execute(query)
                res = []
                for row in db_cursor:
                    res.append(row) 
                return res         
            except:
                print ("Error ocurred")
            finally:
                db.commit()
                db_cursor.close()
                db.close()
        else:
            return None          