from Zones.Zone import Zone
from IDGenerator import IDGenerator
import requests
from Zones.Storey import Storey

URL = "http://127.0.0.1:3030/bot"

class Space(Zone):

    def create(self, args):
        self.type = args[0]
        self.height = args[1]
        self.width = args[2]
        self.length = args[3]
        self.role = args[4]
        self.hasSpaces = args[5]
        self.space_id = IDGenerator.createID(self.type)
        self.storey_id = IDGenerator.createID(self.type)

    def addToKB(self, args):

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.space_id) + ''' a bot:Building.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(args[3]) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(args[1]) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(args[4]) + '''".
            '''
            )   
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.space_id) + ''' bot:hasSpace "''' + str(args[-1][i]) + '''".
                    ''')
            UPDATE += ('''}
            WHERE {
            }
            ''')
            print(UPDATE)
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
    
            return 1
        except:
            return 0
    
    def remove(self, args):
        
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
			DELETE {
                bot:''' + str(self.space_id) + ''' a bot:Building.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(args[3]) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(args[1]) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(args[4]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.space_id) + ''' bot:hasStorey "''' + str(args[-1][i]) + '''".
                    ''')
            UPDATE += ('''}
            WHERE {
            }
            ''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    



    def getStorey(self):
        return self.storey_id

    def getZones(self):
        return self.hasSpaces

    def getID(self):
        return self.space_id

    def getType(self):
        return self.type
    
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width
    
    def getLength(self):
        return self.length

    def getVolume(self):
        return self.length*self.width*self.height