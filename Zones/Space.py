from Zones.Zone import Zone
import requests

URL = "http://127.0.0.1:3030/bot"

class Space(Zone):

    def create(self, args):
        self.type = args[0]
        self.height = args[1]
        self.width = args[2]
        self.length = args[3]
        self.hasSpaces = args[4]

    def addToKB(args):
        space_id = Space.getID()

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(space_id) + ''' a bot:Building.
                bot:''' + str(space_id) + ''' bot:hasLength "''' + str(args[3]) + '''".
                bot:''' + str(space_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(space_id) + ''' bot:hasHeight "''' + str(args[1]) + '''".
            '''
            )   
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(space_id) + ''' bot:hasSpace "''' + str(args[-1][i]) + '''".
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
    
    def remove():
        pass

    def getID(self):
        pass
