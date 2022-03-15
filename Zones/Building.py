# from Zones.Zone import Zone
import requests


### Comments for Johanne:
#   mappe C:\Users\Johanne\Downloads\apache-jena-fuseki-4.2.0\apache-jena-fuseki-4.2.0
#   kall java -jar fuseki-server.jar
# Gjøre onsdag: lage IDGeneratorklasse

URL = "http://127.0.0.1:3030/bot"

class Building(): #class Building(Zone):

    def create(self, height, width, length):
        self.type = "Building"
        #self.building_ID = "Building_" + building_ID_int #Not sure if this will be enough
        self.height = height
        self.width = width
        self.length = length
        self.containsZone = list
        
        

    def addToKB(order_list):
        
        # INPUT order_list: [type, length, width, height, hasStoreys[]]
        # hasStoryes is a list containing ids for the storeys inside this building. 
 	 	# return 1 (true) when added
        building_id = Building.getID(order_list)

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(building_id) + ''' a bot:Building.
                bot:''' + str(building_id) + ''' bot:hasLength "''' + str(order_list[1]) + '''".
                bot:''' + str(building_id) + ''' bot:hasWidth "''' + str(order_list[2]) + '''".
                bot:''' + str(building_id) + ''' bot:hasHeight "''' + str(order_list[3]) + '''".
            '''
            )   
            for i in range(len(order_list[-1])):
                UPDATE += ('''
                bot:''' + str(building_id) + ''' bot:hasStorey "''' + str(order_list[-1][i]) + '''".
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

    def remove(order_list):
        building_id = Building.getID(order_list)
        
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
			DELETE {
                    bot:''' + str(building_id) + ''' a bot:Building.
                    bot:''' + str(building_id) + ''' bot:hasLength "''' + str(order_list[1]) + '''".
                    bot:''' + str(building_id) + ''' bot:hasWidth "''' + str(order_list[2]) + '''".
                    bot:''' + str(building_id) + ''' bot:hasHeight "''' + str(order_list[3]) + '''".
            ''') 
            for i in range(len(order_list[-1])):
                UPDATE += ('''
                bot:''' + str(building_id) + ''' bot:hasStorey "''' + str(order_list[-1][i]) + '''".
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

    def getID(order_list):
        return IDGenerator.create_building_id(order_list)

# order_list1 = ['byggning', 80000, 500000, 10000, ['kjøkken', 'bad', 'soverom']]
# order_list4 = ['bygg', 80000, 500000, 10000, ['kjøkken', 'bad', 'soverom']]
# print(Building.addToKB(order_list1))
# print(Building.remove(order_list4))