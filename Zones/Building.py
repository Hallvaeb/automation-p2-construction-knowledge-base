from numpy import array
from Zone import Zone
import requests
# from IDGenerator import IDGenerator
from Site import Site



### Comments for Johanne:
#   mappe C:\Users\Johanne\Downloads\apache-jena-fuseki-4.2.0\apache-jena-fuseki-4.2.0
#   kall java -jar fuseki-server.jar
# Gjøre onsdag: lage IDGeneratorklasse

URL = "http://127.0.0.1:3030/bot"

class Building(Zone):

    site_id = None

    def create(self, args):
        self.type = args[0]
        self.length = args[1]
        self.width = args[2]
        self.height = args[3]
        self.hasStoreys = args[-1]

        self.building_id = "building_141" #IDGenerator.create_id(self.type) #building_0

    def addToKB(self, args):
        
        # INPUT args: [type, length, width, height, hasStoreys[]]
        # hasStoryes is a list containing ids for the storeys inside this building. 
 	 	# return 1 (true) when added

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.building_id) + ''' a bot:Building.
                bot:''' + str(self.building_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            '''
            )   
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.building_id) + ''' bot:hasStorey "''' + str(args[-1][i]) + '''".
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
                    bot:''' + str(self.building_id) + ''' a bot:Building.
                    bot:''' + str(self.building_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                    bot:''' + str(self.building_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                    bot:''' + str(self.building_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.building_id) + ''' bot:hasStorey "''' + str(args[-1][i]) + '''".
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

    def addZone(self, storey_id): #adds zones (here storeys) to the builing as well as the list hasStoreys
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.building_id) + ''' a bot:Building.
                bot:''' + str(self.building_id) + ''' bot:hasStorey "''' + str(storey_id) + '''".
                }
            WHERE {
            }
            ''')
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            
            self.hasStoreys.append(str(storey_id))
            return 1
        except:
            return 0

    def getSite(self):
        
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?site
            WHERE {
                ?site a bot:Site.
                ?site bot:hasBuilding ?building.
            FILTER ( 
                EXISTS { ?site bot:hasBuilding "'''+ str(self.building_id) +'''"}
            )}
            ''')

            PARAMS = {"query": QUERY}
            r = requests.get(url = URL, params = PARAMS) 
            data = r.json()
            site = str(data['results']['bindings']).replace("]","").replace("}","").replace("'","").replace('"','').split('#')[-1]
            return site
        except:
            return "This building is not placed at any site"

        # fungerer nå, men det er et problem dersom flere sites har bygg med samme id 
        # på sitt område. Dette må diskuteres!

    def getZones(self):
        return self.hasStoreys

    def getID(self):
        return self.building_id

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





### ----- Tester ----- ###

site_args1 = ['site', 500000, 500000, 0,[]]
site = Site()
# site.create(site_args1)
# print(site.addToKB(site_args1))


args1 = ['building', 7000, 90000, 10000, ['kjøkken', 'bad', 'soverom']]
building = Building()
# building.create(args1)
# print(building.addToKB(args1))
# print(Building.remove(args4))
# print(site.addZone(building.building_id))
# print(site.getID(),"sine bygg: ", site.getZones())
# print(building.building_id,"is places at", building.getSite())
print(site.getZones())

