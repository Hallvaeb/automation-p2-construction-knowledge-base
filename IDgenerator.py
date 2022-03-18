import datetime


class IDGenerator:
    
    def create_ID(self, type):
        self.type = type
        integer = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        id = self.type + str(integer)
        return id