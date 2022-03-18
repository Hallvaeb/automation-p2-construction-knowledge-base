import datetime
datetime.datetime.now().strftime('%Y%m%d%H%M%S')

class IDGenerator:
    
    def create_ID(self, type):
        self.type = type
        integer = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        id = self.type + str(integer)