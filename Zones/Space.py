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
                raise ValueError("The given space role was not found in KB!")
            
            # HERE WE ASK KB WHAT A SPACE OF THIS ROLE HAS
            space_args = Space.get_prototype_args_from_KB(role)
            
            self.space_id = IDGenerator.create_ID(self)
            self.length = space_args[0]
            self.width = space_args[1]
            self.height = space_args[2]
            self.energyEfficiency = space_args[3]
            self.role = space_args[4]

            self.add_to_KB()

        else:
            """
                Adds prototype space to KB
            """
            # INPUT args: [length, width, height, energyEfficiency, role]
            self.length = args[0]
            self.width = args[1]
            self.height = args[2]
            self.energyEfficiency = args[3]

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
        data = r.json()
		
        if (len(data['results']['bindings']) == 0 ):
            return 0
        return 1
        

    def add_to_KB(self):
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
                bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                }
            WHERE {
            bot:''' + str(self.space_id) + ''' a bot:Space.
            bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
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
        returns values = [space_id, length, width, height, energyEfficiency, role]

        '''
        print("role", role)

        QUERY = ('''
        PREFIX bot:<https://w3id.org/bot#>
        SELECT ?length ?width ?height ?energyEfficiency ?role
        WHERE {
	        ?space a bot:Space.
            ?space bot:hasLength ?length.
            ?space bot:hasWidth ?width.
            ?space bot:hasHeight ?height.
            ?space bot:energyEfficiency ?energyEfficiency.
            ?space bot:hasRole ?role.
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
        returns values = [space_id, length, width, height, energyConsumption, role]

        '''

        # QUERY = ('''
        # PREFIX bot:<https://w3id.org/bot#>
        # SELECT ?length ?width ?height ?energyEfficiency ?role
        # WHERE {
	    #     ?space a bot:Space.
        #     ?space bot:hasLength ?length.
        #     ?space bot:hasWidth ?width.
        #     ?space bot:hasHeight ?height.
        #     ?space bot:energyEfficiency ?energyEfficiency.
        #     ?space bot:hasRole ?role.
	    #     FILTER (EXISTS { ?space bot:hasID "'''+str(space_id)+'''"})
        #     }
        # ''')
        # PARAMS = {"query": QUERY}
        # r = requests.get(url = URL, params = PARAMS)
        # data = r.json()
        
        # list_data = str(data['results']['bindings']).replace('{','').replace('[','').replace('}','').replace(']','').replace(':',',').split(",")
        # for i in range(4,len(list_data),5):
        #     values.append(str(list_data[i]).strip().strip("'"))

        values = [space_id, "20", "30", "30", "60000", "Hallway"]
        return values

    def get_storey(self):
        pass
        #Må her inn i KB

    def get_zones(self):
        pass

    def get_ID(self):
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
        return self.length*self.width

    def get_volume(self):
        return self.length*self.width*self.height

    def get_energyEfficiency(self):
        return self.energyEfficiency


