from Zones.Zone import Zone
import requests


URL = "http://127.0.0.1:3030/bot"


class Site(Zone):

    def create(self, args):
        self.type = args[0]           
        self.height = args[1]         
        self.width = args[2]          
        self.length = args[3]
        self.site_id = Site.getID()         
        self.hasBuildings = args[4]   #List

    def addToKB(args):
         # INPUT order_list: [type, length, width, height, hasStoreys[]]
        # hasStoryes is a list containing ids for the storeys inside this building. 
 	 	# return 1 (true) when added
        site_id = Site.getID(args)

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(site_id) + ''' a bot:Building.
                bot:''' + str(site_id) + ''' bot:hasLength "''' + str(args[3]) + '''".
                bot:''' + str(site_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(site_id) + ''' bot:hasHeight "''' + str(args[1]) + '''".
            '''
            )   
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(args) + ''' bot:hasBuildings "''' + str(args[-1][i]) + '''".
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

    def remove(args):
        
        site_id = Site.getID(args)
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
			DELETE {
                bot:''' + str(site_id) + ''' a bot:Building.
                bot:''' + str(site_id) + ''' bot:hasLength "''' + str(args[3]) + '''".
                bot:''' + str(site_id) + ''' bot:hasWidth "''' + str(args[2]) + '''".
                bot:''' + str(site_id) + ''' bot:hasHeight "''' + str(args[1]) + '''".
            ''') 
            for i in range(len(args[-1])):
                UPDATE += ('''
                bot:''' + str(site_id) + ''' bot:hasStorey "''' + str(args[-1][i]) + '''".
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

    
    
    def getID(self):
        pass
