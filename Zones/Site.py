from Zone import Zone
import requests
# from IDGenerator import IDGenerator

URL = "http://127.0.0.1:3030/bot"


class Site(Zone):
    # site_id = "site_140"
    # hasBuildings = []
    
    def create(self, args):
        self.type = args[0]           
        self.length = args[1]
        self.width = args[2]
        self.height = args[3]
        self.hasBuildings = args[-1]   #List
        self.site_id = "site_20" #IDGenerator.createID(type)         
        
    def addToKB(self, args):
         # INPUT order_list: [type, length, width, height, hasBuildings[]]
        # hasStoryes is a list containing ids for the storeys inside this building. 
 	 	# return 1 (true) when added

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.site_id) + ''' a bot:Site.
                bot:''' + str(self.site_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            '''
            )   
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(args) + ''' bot:hasBuilding bot:''' + str(args[-1][i]) + '''.
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
                bot:''' + str(self.site_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.site_id) + ''' bot:hasBuilding bot:''' + str(args[-1][i]) + '''.
                    ''')
            UPDATE += ('''}
            WHERE {
                bot:''' + str(self.site_id) + ''' a bot:Site.
                bot:''' + str(self.site_id) + ''' bot:hasLength "''' + str(args[1]) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(self.site_id) + ''' bot:hasHeight "''' + str(args[3]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(self.site_id) + ''' bot:hasBuilding bot:''' + str(args[-1][i]) + '''.
                    ''')
            UPDATE += ('''}''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            print(UPDATE)
            return 1
        except:
            return 0

    def addZone(self, building_id): #adds (one at a time) zones (here building) to the site as well as the list hasBuildings
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
    
    def getZones(self):
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

    def getID(self):
        return self.site_id

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

        