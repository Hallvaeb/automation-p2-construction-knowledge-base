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

        self.building_id = IDGenerator.create_ID() 

    def add_to_KB(self):
        # hasStoryes is a list containing ids for the storeys inside this building. 
 	 	# return 1 (true) when added

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.building_id) + ''' a bot:Building.
                bot:''' + str(self.building_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            '''
            )   
            for i in range(len(self.hasStoreys)):
                UPDATE += ('''
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(self.hasStoreys[i]) + '''.
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
                    bot:''' + str(self.building_id) + ''' a bot:Building.
                    bot:''' + str(self.building_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                    bot:''' + str(self.building_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                    bot:''' + str(self.building_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            ''') 
            for i in range(len(self.hasStoreys)):
                UPDATE += ('''
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(self.hasStoreys[i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
                bot:''' + str(self.building_id) + ''' a bot:Building.
                bot:''' + str(self.building_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            ''') 
            for i in range(len(self.hasStoreys)):
                UPDATE += ('''
                bot:''' + str(self.building_id) + ''' bot:hasStorey bot:''' + str(self.hasStoreys[i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def add_zone(self, storey_id): #adds zones (here storeys) to the builing as well as the list hasStoreys
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

    def get_site(self):
        
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
            return 0 #"This building is not placed at any site"

    def get_zones(self):
        return self.hasStoreys

    def get_ID(self):
        return self.building_id

    def get_type(self):
        return self.type
    
    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
    def get_length(self):
        return self.length

    def get_volume(self):
        return self.length*self.width*self.height
