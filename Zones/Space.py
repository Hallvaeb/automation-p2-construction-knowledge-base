from Zones.Zone import Zone
from IDGenerator import IDGenerator
import requests


URL = "http://127.0.0.1:3030/bot"

class Space(Zone):

    def __init__(self, args):
        self.type = "space"
        if (len(args) < 3):
            """
                Space is being used and created in construction
            """
            role = args[0]
            if not Space.is_role_in_KB(role):
                self.type = "The given space role was not found in KB!"
            else:
                space_args = Space.get_prototype_args_from_KB(role)
                # GIVE IT A NEW ID BUT COPY ALL OTHER VALUES
                self.space_id = IDGenerator.create_ID(self)
                self.length = space_args[1]
                self.width = space_args[2]
                self.height = space_args[3]
                self.energy_consumption = space_args[4]
                self.role = space_args[5]

                self.add_to_KB()
        else:
            """
                Adds prototype space to KB
            """
            # INPUT args: [length, width, height, energy_consumption, role]
            self.length = args[0]
            self.width = args[1]
            self.height = args[2]
            self.energy_consumption = args[3]

            # WE NEED A UNIQUE ROLE:
            role_core = args[4]+"_"
            i = 1
            role = role_core + str(i)
            while(Space.is_role_in_KB(role)):
                i += 1
                role = role_core + str(i)
            self.role = role
            self.space_id = IDGenerator.create_space_prototype_ID(self)
            
            self.add_to_KB()


    def is_role_in_KB(role):
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
        if r.status_code == 404:
            return 0
        data = r.json()
		
        if (len(data['results']['bindings']) == 0 ):
            return 0
        return 1
        

    def add_to_KB(self):
        print("INSERT {"
                'bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasID "''' + str(self.space_id) + '''"''')
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasID "''' + str(self.space_id) + '''".

                }
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
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasID "''' + str(self.space_id) + '''".
                }
            WHERE {
            bot:''' + str(self.space_id) + ''' a bot:Space.
            bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            bot:''' + str(self.space_id) + ''' bot:energyConsumption "''' + str(self.energy_consumption) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasID "''' + str(self.space_id) + '''".

                }''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def add_zone(self, adjacent_space_id): #adds zones (here adjacent spaces) to the space as well as the list adjacentZones
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
            # self.adjacentZones.append(str(adjacent_space_id))
            return 1
        except:
            return 0

    def get_prototype_args_from_KB(role):
        ''' 
        returns values = [space_id, length, width, height, energy_consumption, role]
        uses the role to filter out wanted space.
        '''
        QUERY = ('''
        PREFIX bot:<https://w3id.org/bot#>
        SELECT ?space_id ?length ?width ?height ?energy_consumption ?role
        WHERE {
	        ?space a bot:Space.
            ?space bot:hasLength ?length.
            ?space bot:hasWidth ?width.
            ?space bot:hasHeight ?height.
            ?space bot:energyConsumption ?energy_consumption.
            ?space bot:hasRole ?role.
            ?space bot:hasID ?space_id.

	        FILTER (EXISTS { ?space bot:hasRole "'''+str(role)+'''"})
            }
        ''')
        PARAMS = {"query": QUERY}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()

        list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').split(",")
        values = []
        for i in range(4,len(list_data),5):
            values.append(str(list_data[i]).strip().strip("'"))

        return values

    def get_args_from_KB(space_id):
        ''' 
        returns values = [space_id, length, width, height, energy_consumption, role]

        '''

        QUERY = ('''
        PREFIX bot:<https://w3id.org/bot#>
        SELECT ?space_id ?length ?width ?height ?energy_consumption ?role
        WHERE {
	        ?space a bot:Space.
            ?space bot:hasLength ?length.
            ?space bot:hasWidth ?width.
            ?space bot:hasHeight ?height.
            ?space bot:energyConsumption ?energy_consumption.
            ?space bot:hasRole ?role.
            ?space bot:hasID ?space_id.
	        FILTER (EXISTS { ?space bot:hasID "'''+str(space_id)+'''"})
            }
        ''')
        PARAMS = {"query": QUERY}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        print("DATA------------------------------\n", data)
        list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').split(",")
        values = []
        for i in range(4,len(list_data),5):
            x = str(list_data[i]).strip().strip("'")
            print(x)
            values.append(x)

        return values

    def get_storey(self):
        pass
        #Må her inn i KB

    def get_zones(self):
        pass

    def get_ID(self):
        print("Space ID is getting gotten", self.space_id)
        return self.space_id

    def get_type(self):
        return self.type
    
    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
    def get_length(self):
        return self.length

    def get_area(self):
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?length ?width
            WHERE {
                ?space a bot:Space.
                ?space bot:hasLength ?length.
                ?building bot:hasWidth ?width.
                FILTER ( EXISTS { ?space bot:hasID "'''+ str(self.space_id) +'''"}
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

    def get_volume(self):
        try:
            QUERY = ('''
            PREFIX bot:<https://w3id.org/bot#>
            SELECT ?length ?width ?height
            WHERE {
                ?space a bot:Space.
                ?space bot:hasLength ?length.
                ?space bot:hasWidth ?width.
                ?space bot:hasHeight ?height.
                FILTER ( EXISTS { ?space bot:hasID "'''+ str(self.space_id) +'''"}
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

    def get_energy_consumption(self):
        energy_efficiency = self.energy_consumption / self.get_area()
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

