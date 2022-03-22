import requests
from Zones.Zone import Zone
from IDGenerator import IDGenerator

URL = "http://127.0.0.1:3030/bot"


class Site(Zone):
    
    def __init__(self, args):
        # INPUT args: [length, width, height, hasBuildings[]]
        self.type = "site"          
        self.length = args[0]
        self.width = args[1]
        self.height = args[2]
        self.hasBuildings = args[-1]   #List
        
        self.site_id = IDGenerator.create_ID()         
        
    def add_to_KB(self):
        # hasStoryes is a list containing ids for the storeys inside this building. 
 	 	# return 1 (true) when added

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.site_id) + ''' a bot:Site.
                bot:''' + str(self.site_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            '''
            )   
            for i in range(len(self.hasBuildings)):
                UPDATE += ('''
                bot:''' + str(self.site_id) + ''' bot:hasBuilding bot:''' + str(self.hasBuildings[i]) + '''.
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
                bot:''' + str(self.site_id) + ''' a bot:Site.
                bot:''' + str(self.site_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            ''') 
            for i in range(len(self.hasBuildings)):
                UPDATE += ('''
                bot:''' + str(self.site_id) + ''' bot:hasBuilding bot:''' + str(self.hasBuildings[i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
                bot:''' + str(self.site_id) + ''' a bot:Site.
                bot:''' + str(self.site_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            ''') 
            for i in range(len(self.hasBuildings)):
                UPDATE += ('''
                bot:''' + str(self.site_id) + ''' bot:hasBuilding bot:''' + str(self.hasBuildings[i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def add_zone(self, building_id): #adds (one at a time) zones (here building) to the site as well as the list hasBuildings
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.site_id) + ''' a bot:Site.
                bot:''' + str(self.site_id) + ''' bot:hasBuilding bot:''' + str(building_id) + '''.

                }
            WHERE {
            }
            ''')
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            
            #add the adjacent zone to the list of adjacent zones to this zone(here site).
            self.hasBuildings.append(str(building_id))
            return 1
        except:
            return 0
    
    def get_zones(self):
        # Usikker på om denne fungerer slik, eller om vi må inn i databasen
        # og hente ut fra relasjonene! Se på på fredag, innspill.
        # Problemet er: laget tre site_100 etter hverandre, men da blir de så klart
        # enkeltstående og ikke samme entitet. det vil si alle har sin egen liste med
        # med kun det ene huset som er lagt til via addZone()
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?building
            WHERE {
                ?site a bot:Site.
  				?site bot:hasBuilding ?building.
            FILTER ( ?site = bot:'''+str(self.site_id)+''')
            }
            ''')

            PARAMS = {"query": QUERY}
            r = requests.get(url = URL, params = PARAMS) 
            data = r.json()
            data_splitted = str(data['results']['bindings']).split('}, {')
            zones = []
            for i in range(len(data_splitted)):
                data_splitted2 = data_splitted[i].split(',')
                data_splitted3=data_splitted2[-1].split(':')
                zone = str(data_splitted3[-1].split('#')[-1]).replace("}",'').replace("]",'').replace("'",'').replace(" ",'')
                zones.append(zone)
            return zones
        except:
            return 0 #"This site does not have any buildings"
        
        # return self.hasBuildings

    def get_ID(self):
        return self.site_id

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