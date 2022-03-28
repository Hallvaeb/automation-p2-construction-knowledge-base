from IDGenerator import IDGenerator
from Zones.Zone import Zone
from Zones.Site import Site
import requests

### Comments for Johanne:
#   mappe C:\Users\Johanne\Downloads\apache-jena-fuseki-4.2.0\apache-jena-fuseki-4.2.0
#   kall java -jar fuseki-server.jar


URL = "http://127.0.0.1:3030/bot"

class Building(Zone):

    def __init__(self, args):
        # INPUT args: [length, width, height, energy_consumption, hasStoreys[]]
        self.type = "building"
        self.length = args[0]
        self.width = args[1]
        self.height = args[2]
        self.energy_consumption = args[3]
        self.hasStoreys = args[-1] # consists of storey_ids!

        self.building_id = IDGenerator.create_ID(self) 
        self.add_to_KB()

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
                bot:''' + str(self.building_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasID "''' + str(self.building_id) + '''".

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
                    bot:''' + str(self.building_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
                    bot:''' + str(self.building_id) + ''' bot:hasID "''' + str(self.building_id) + '''".

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
                bot:''' + str(self.building_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
                bot:''' + str(self.building_id) + ''' bot:hasID "''' + str(self.building_id) + '''".

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

    def get_args_from_KB(building_id):
        ''' 
        returns [building_id, length, width, height, energy_consumption, number_of_storeys, all_storeys_identical] 
        '''

        QUERY = ('''
        PREFIX bot:<https://w3id.org/bot#>
        SELECT ?building_id ?length ?width ?height ?energy_consumption 
        WHERE {
	        ?building a bot:Building.
            ?building bot:hasLength ?length.
            ?building bot:hasWidth ?width.
            ?building bot:hasHeight ?height.
            ?building bot:energyConsumption ?energy_consumption.
            ?building bot:hasID ?building_id.

	        FILTER (EXISTS { ?building bot:hasID "'''+str(building_id)+'''"})
            }
        ''')
        PARAMS = {"query": QUERY}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        
        list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').split(",")
        values = []
        for i in range(4,len(list_data),5):
            values.append(str(list_data[i]).strip().strip("'"))
        values.append(Building.get_number_of_storeys(building_id))
        return values

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

    def get_number_of_storeys(building_id):
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT (count(?storey) as ?number_of_storeys)
            WHERE {
                ?building a bot:Building.
                ?building bot:hasID ?building_id.
                ?building bot:hasStorey ?storey
	        FILTER (EXISTS { ?building bot:hasID "'''+ building_id +'''"})
            }
			Group by ?building_id
            ''')

            PARAMS = {"query": QUERY}
            r = requests.get(url = URL, params = PARAMS) 
            data = r.json()
            list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').replace("'","").replace(" ","").split(",")
            return list_data[-1]
        except:
            return 0
            
    def get_area(self):
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?length ?width
            WHERE {
                ?building a bot:Building.
                ?building bot:hasLength ?length.
                ?building bot:hasWidth ?width.
                FILTER ( EXISTS { ?building bot:hasID "'''+ str(self.building_id) +'''"}
            )
            }
            ''')

            PARAMS = {"query": QUERY}
            r = requests.get(url = URL, params = PARAMS) 
            data = r.json()
            list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').split(",")
            values = []
            for i in range(4,len(list_data),5):
                values.append(str(list_data[i]).strip().strip("'"))
            return float(values[0])*float(values[1])
        except:
            return 0

    def calculate_energy_efficiency(self):
        energy_efficiency = self.energy_consumption / self.get_area() * Building.get_number_of_storeys(self.building_id)
        if energy_efficiency <= 85:
            return "A"
        elif energy_efficiency <= 95:
            return "B"
        elif energy_efficiency <= 110:
            return "C"
        elif energy_efficiency <= 135:
            return "D"
        elif energy_efficiency <= 160:
            return "E"
        elif energy_efficiency <= 200:
            return "F"
        else:
            return "G"

    def get_volume(self):
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?length ?width ?height
            WHERE {
                ?building a bot:Building.
                ?building bot:hasLength ?length.
                ?building bot:hasWidth ?width.
                ?building bot:hasHeight ?height.
                FILTER ( EXISTS { ?building bot:hasID "'''+ str(self.building_id) +'''"}
            )
            }
            ''')

            PARAMS = {"query": QUERY}
            r = requests.get(url = URL, params = PARAMS) 
            data = r.json()
            list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').split(",")
            values = []
            for i in range(4,len(list_data),5):
                values.append(str(list_data[i]).strip().strip("'"))
            return float(values[0])*float(values[1])*float(values[2])
        except:
            return 0
