from Zones.Zone import Zone
from IDGenerator import IDGenerator
import requests

URL = "http://127.0.0.1:3030/bot"


class Storey(Zone):

    def __init__(self, args):
        # INPUT args: [length, width, height, hasSpaces[]]
        self.type = "storey"
        self.length = args[0]
        self.width = args[1]
        self.height = args[2]
        self.hasSpaces = args[-1]
        
        self.storey_id = IDGenerator.create_ID() 
        self.add_to_KB()

    def add_to_KB(self):
        # hasSpaces is a list containing ids for the spaces in this storey. 
 	 	# return 1 (true) when added

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.storey_id) + ''' a bot:Storey.
                bot:''' + str(self.storey_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.storey_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.storey_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            '''
            )   
            for i in range(len(self.hasSpaces)):
                UPDATE += ('''
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(self.hasSpaces[i]) + '''.
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

    def remove(self):
        
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
			DELETE {
                    bot:''' + str(self.storey_id) + ''' a bot:Storey.
                    bot:''' + str(self.storey_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            ''') 
            for i in range(len(self.hasSpaces)):
                UPDATE += ('''
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(self.hasSpaces[i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
            bot:''' + str(self.storey_id) + ''' a bot:Storey.
                    bot:''' + str(self.storey_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                    bot:''' + str(self.storey_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            ''') 
            for i in range(len(self.hasSpaces)):
                UPDATE += ('''
                bot:''' + str(self.storey_id) + ''' bot:hasSpace bot:''' + str(self.hasSpaces[i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def add_zone(self, space_id): #adds zones (here space) to the storey as well as the list hasSpaces
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

    def get_building(self):
        pass

    def get_floorNumber(self):
        pass

    def fill_storey(self):
        pass
    
    def get_zones(self):
        return self.hasSpaces

    def get_ID(self):
        return self.storey_id

    def get_type(self):
        return self.type
    
    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
    def get_length(self):
        return self.length

    def get_area(self):
        return self.length*self.width

    def get_volume(self):
        return self.length*self.width*self.height