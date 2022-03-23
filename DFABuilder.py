from IDGenerator import IDGenerator
from Zones.Site import Site
from Zones.Building import Building
from Zones.Storey import Storey
from Zones.Space import Space

path_to_dfa_folder = "C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/"

#First draft of the class works. Currently every dfa made will be named "order_17", but a methid to automize this is easily implemented. 
class DFABuilder():

    
    def make_DFA(type, height, width, length, order_id):
        id = IDGenerator.create_dfa_zone_ID()
        #Read current temp file
        f = open(path_to_dfa_folder + type +".dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<LENGTH>", str(length))
        txt_replaced = txt_replaced.replace("block1", str(id)) 
        f.close()

        #Make new DFA file
        f = open(path_to_dfa_folder + "tempo_" + type + ".dfa", "w")
        f.write(txt_replaced)
        f.close

        f = open(path_to_dfa_folder + "Products/" + order_id + ".dfa", "a")
        #TODO switch "building_12" with IDGenerator
        f.write(txt_replaced)
        f.close


    def make_design_template(): 
        #Design
        order_id = IDGenerator.create_order_ID()
        f = open(path_to_dfa_folder + "design.dfa", "r")
        txt = f.read()
        txt = txt.replace("<ID>", order_id) #TODO replace order 13 with automated id.
        f.close()
        #Design
        f = open(path_to_dfa_folder + "Products/" + order_id + ".dfa", "w")
        #TODO switch "building_12" with IDGenerator
        f.write(txt)
        f.close
        return order_id

    def generate_DFA(IDs):
        order_id = DFABuilder.make_design_template()   
        list = IDs.split("_")
        list = IDs[::2]
        print(list)
        for type in list:
            if type == "building":
                arguments = Building.get_args_from_KB()
                DFABuilder.make_DFA(type, arguments[2], arguments[1], arguments[0], order_id)
            
            elif type == "site":
                arguments = Site.get_args_from_KB()
                DFABuilder.make_DFA(type, arguments[2], arguments[1], arguments[0], order_id)

            elif type == "space":
                arguments = Space.get_args_from_KB()
                DFABuilder.make_DFA(type, arguments[2], arguments[1], arguments[0], order_id)
            
            elif type == "storey":
                arguments = Storey.get_args_from_KB()
                DFABuilder.make_DFA(type, arguments[2], arguments[1], arguments[0], order_id)
        



    # def generate_DFA(type, height, width, length, order_id):

    #     if type == "building":
    #         DFABuilder.make_DFA("building", height, width, length, order_id)

    #     elif type == "site":
    #         DFABuilder.make_DFA("site", height, width, length, order_id)
            
    #     elif type == "space":
    #         DFABuilder.make_DFA("space", height, width, length, order_id)
            
    #     elif type == "storey":
    #         DFABuilder.make_DFA("storey", height, width, length, order_id)
            
DFABuilder.generate_DFA(["building_5655", "site_323232", "storey_24232323", "building_44444"])

#Currently works if these methods are called. 
# make_design_template() has to be called before generate_DFA, and this method must be called
#for each zone you want to add to the .dfa-file. 

# order_ID = DFABuilder.make_design_template()
# DFABuilder.generate_DFA("site", 0.2, 300, 500, order_ID)
# DFABuilder.generate_DFA("building", 200, 150, 300, order_ID)
# DFABuilder.generate_DFA("space", 2, 11, 14, order_ID)

# Current issues:
# - Colour only appears on the last added zone
# - Still not implemented a way to select placement of the zones, which probably will mean a big change in the current module. 

