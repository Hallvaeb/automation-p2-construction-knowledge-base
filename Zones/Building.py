from IDGenerator import IDGenerator
from Zones.Zone import Zone
import requests
from Zones.Site import Site

### Comments for Johanne:
#   mappe C:\Users\Johanne\Downloads\apache-jena-fuseki-4.2.0\apache-jena-fuseki-4.2.0
#   kall java -jar fuseki-server.jar
# Gjøre onsdag: lage IDGeneratorklasse

URL = "http://127.0.0.1:3030/bot"

class Building(Zone):

    def __init__(self, args):
        # INPUT args: [length, width, height, hasStoreys[]]
        self.type = "building"
        self.length = args[0]
        self.width = args[1]
        self.height = args[2]
        self.hasStoreys = args[-1]

        self.building_id = IDGenerator.create_ID(self) 

    def addToKB(self):
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
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(args[-1][i]) + '''.
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
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(args[-1][i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
                bot:''' + str(self.building_id) + ''' a bot:Building.
                bot:''' + str(self.building_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(args[-1][i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
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
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(storey_id) + '''.
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

    # def removeZone(self, storey_id): #adds zones (here storeys) to the builing as well as the list hasStoreys
    #     try:
    #         UPDATE = ('''
    #         PREFIX bot:<https://w3id.org/bot#>
    #         DELETE {
    #             bot:''' + str(self.building_id) + ''' a bot:Building.
    #             bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(storey_id) + '''.
    #             }
    #         WHERE {
    #             bot:''' + str(self.building_id) + ''' a bot:Building.
    #             bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(storey_id) + '''.
    #         }
    #         ''')
    #         PARAMS = {"update": UPDATE}
    #         r = requests.post(url = URL+"/update", data = PARAMS) 
            
    #         self.hasStoreys.remove(str(storey_id))
    #         return 1
    #     except:
    #         return 0

    def getSite(self):
        
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?site
            WHERE {
                ?site a bot:Site.
                ?site bot:hasBuilding ?building.
            FILTER ( 
                EXISTS { ?site bot:hasBuilding bot:'''+ str(self.building_id) +'''}
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





# ### ----- Tester ----- ###

# site_args1 = ['site', 500000, 500000, 0,[]]
# site = Site(site_args1)
# # site.create(site_args1)
# print(site.addToKB(site_args1))


# args1 = ['building', 7000, 90000, 10000, ['Storey_21', 'Storey_22', 'Storey_23']]
# args2 = ['building', 7000, 90000, 10000, ['Storey_1']]

# building = Building(args1)
# print(building.addToKB(args1))

# building2 = Building(args2)
# print(building2.addToKB(args2))

# # print(Building.remove(args4))
# print("added zone:",site.addZone(building.building_id),site.addZone(building2.building_id))
# print(site.getID(),"sine bygg: ", site.getZones())
# print(building.building_id,"is places at", building.getSite())
# # print("Er den fjernet:",site.remove(site_args1))
# print(building2.building_id,"is placed at", building2.getSite())
# print(site.getID(),"sine bygg: ", site.getZones())


