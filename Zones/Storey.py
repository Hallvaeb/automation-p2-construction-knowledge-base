from Zone import Zone
from IDGenerator import IDGenerator
import requests

URL = "http://127.0.0.1:3030/bot"

class Storey(Zone):

    # building_id = NOE
    def __init__(self, args):
    # INPUT args: [type, length, width, height, hasSpaces[]]
        self.type = args[0]
        self.length = args[1]
        self.width = args[2]
        self.height = args[3]
        self.hasSpaces = args[-1]
        self.storey_id = IDGenerator.create_id(self.type) #storey_0

    def addToKB(self, args):
        # hasSpaces is a list containing ids for the spaces in this storey. 
 	 	# return 1 (true) when added

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.storey_id) + ''' a bot:Storey.
                bot:''' + str(self.storey_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                bot:''' + str(self.storey_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.storey_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            '''
            )   
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(args[-1][i]) + '''.
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

    def remove(self, args):
        
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
			DELETE {
                    bot:''' + str(self.storey_id) + ''' a bot:Storey.
                    bot:''' + str(self.storey_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(args[-1][i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
            bot:''' + str(self.storey_id) + ''' a bot:Storey.
                    bot:''' + str(self.storey_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(args[-1][i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def addZone(self, space_id): #adds zones (here space) to the storey as well as the list hasSpaces
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.storey_id) + ''' a bot:Storey.
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(space_id) + '''.
                }
            WHERE {
            }
            ''')
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            
            self.hasSpaces.append(str(space_id))
            return 1
        except:
            return 0

    def getBuilding(self):
        pass

    def getFloorNumber(self):
        pass

    def fillStorey(self):
        pass
    
    def getZones(self):
        return self.hasSpaces

    def getID(self):
        return self.storey_id

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