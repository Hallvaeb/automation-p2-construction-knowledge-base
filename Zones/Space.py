from Zone import Zone
from IDGenerator import IDGenerator
import requests

URL = "http://127.0.0.1:3030/bot"

class Space(Zone):



    def __init__(self, args):
        if (len(args) == 1):
            self.__init__2(args)
        else:
            self.__init__1(args)
    
    def __init__1(self, args):
        # INPUT args: [length, width, height, energyEfficiency, role]
        self.type = "space"
        self.length = args[0]
        self.width = args[1]
        self.height = args[2]
        self.energyEfficiency = args[3]
        self.role = args[4]
        # self.adjacentZones = args[5]

        self.space_id = IDGenerator.create_ID(self.type)
        # self.adjacent_space_id = IDGenerator.create_ID(self.type)

        self.isRoleInKB(self.role)

    def __init__2(self, args):
        # INPUT args: [role]
        self.type = "space"
        role = args[0]
        i = 0
        while(Space.isRoleInKB(role)):
            i += 1
            role = role+"_"+str(i)
        self.role = role
        self.space_id = IDGenerator.create_space_prototype_ID(self)


    def isRoleInKB(role):
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


