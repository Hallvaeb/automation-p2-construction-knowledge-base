from Zone import Zone
from IDGenerator import IDGenerator
import requests

URL = "http://127.0.0.1:3030/bot"

class Space(Zone):

    #storey_id = NOE

    def __init__(self, args):
        if len(args) == 1:
            self.__init__2(args[1])
    
    def __init__1(self, length, width, height, energyEfficiency, role, adjacentZones):
        # INPUT args: [type, length, width, height, energyEfficiency, role, adjacentZones[]]

        self.type = type
        self.length = length
        self.width = width
        self.height = height
        self.energyEfficiency = energyEfficiency
        self.role = role
        self.adjacentZones = adjacentZones

        self.space_id = IDGenerator.create_ID(self.type)
        self.adjacent_space_id = IDGenerator.create_ID(self.type)

        # self.isRoleInKB(self.role)

    def __init__1(self, type, role):
        # INPUT args: [type, role]
        self.type = type
        self.role = role

        # self.space_id = IDGenerator.createID(self.type)
        # self.adjacent_space_id = IDGenerator.createID(self.type)

        self.isRoleInKB(self.role)

    def isRoleInKB(self, role):
        QUERY = ('''
        PREFIX bot:<https://w3id.org/bot#>
		SELECT ?role 
		WHERE {
			?space bot:hasRole ?role.
		FILTER ( EXISTS { ?space bot:hasRole "''' + str(role) + '''"} )
		}
        ''')

        PARAMS = {"query": QUERY}
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
		
        print(data)
        if (len(data['results']['bindings']) == 0 ):
            return 0
        return 1
        

    def addToKB(self, args):
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
            '''
            )  
            print("Her") 
            for i in range(len(self.adjacentZones)):
                UPDATE += ('''
                bot:''' + str(self.space_id) + ''' bot:adjacentZone bot:''' + str(self.adjacentZones[i]) + '''.
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
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
            ''') 
            for i in range(len(self.adjacentZones)):
                UPDATE += ('''
                bot:''' + str(self.space_id) + ''' bot:adjacentZone bot:''' + str(self.adjacentZones[i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
            bot:''' + str(self.space_id) + ''' a bot:Space.
            bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
            ''') 
            for i in range(len(self.adjacentZones)):
                UPDATE += ('''
                bot:''' + str(self.space_id) + ''' bot:adjacentZone bot:''' + str(self.adjacentZones[i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def addZone(self, adjacent_space_id): #adds zones (here adjacent spaces) to the space as well as the list adjacentZones
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:adjacentZone bot:''' + str(adjacent_space_id) + '''.
                }
            WHERE {
            }
            ''')
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            
            #add the adjacent zone to the list of adjacent zones to this space.
            self.adjacentZones.append(str(adjacent_space_id))
            return 1
        except:
            return 0

    def getStorey(self):
        pass
        #Må her inn i KB

    def getZones(self):
        return self.adjacentZones

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

    def getEnergyEfficiency(self):
        return self.energyEfficiency

##############

space = Space('space', 2100, 4300, 2100, 60, 'Hallway',['space7'])
print("added:",space.addToKB('space','Hallway'))
# print("1 means yes it is in database:", space.isRoleInKB(space.role))

