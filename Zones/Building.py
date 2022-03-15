from Zones.Zone import Zone


class Building(Zone):

    def create(self, height, width, length):
        self.type = "Building"
        #self.building_ID = "Building_" + building_ID_int #Not sure if this will be enough
        self.height = height
        self.width = width
        self.length = length
        

    def addToKB():
        pass

    def remove():
        pass

    def getID():
        pass
