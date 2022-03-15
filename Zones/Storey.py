from Zones.Zone import Zone


class Storey(Zone):

    def create(self, height, width, length):
        self.type = "Storey"
        self.height = height
        self.width = width
        self.length = length
        self.containsZone = list

    def addToKB():
        pass

    def remove():
        pass

    def getID():
        pass
