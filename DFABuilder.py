from IDGenerator import IDGenerator
from Zones.Site import Site
from Zones.Building import Building
from Zones.Storey import Storey
from Zones.Space import Space

# SIGVE
# path_to_dfa_folder = "C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/"

# HALLVARD
path_to_dfa_folder = "C:/Users/Eier/Github/kbe-a2/DFAs/"


#First draft of the class works. Currently every dfa made will be named "order_17", but a methid to automize this is easily implemented. 
class DFABuilder():

    
    def make_DFA(type, length, width, height, design_id):
        id = IDGenerator.create_dfa_zone_ID()
        #Read current temp file
        f = open(path_to_dfa_folder + type +".dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<LENGTH>", str(length))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("block1", str(id)) 
        f.close()

        #Make new DFA file
        f = open(path_to_dfa_folder + "tempo_" + type + ".dfa", "w")
        f.write(txt_replaced)
        f.close

        f = open(path_to_dfa_folder + "Products/" + design_id + ".dfa", "a")
        #TODO switch "building_12" with IDGenerator
        f.write(txt_replaced)
        f.close


    def make_design_template(): 
        #Design
        design_id = IDGenerator.create_design_ID()
        f = open(path_to_dfa_folder + "design.dfa", "r")
        txt = f.read()
        txt = txt.replace("<ID>", design_id) #TODO replace order 13 with automated id.
        f.close()
        #Design
        f = open(path_to_dfa_folder + "Products/" + design_id + ".dfa", "w")
        #TODO switch "building_12" with IDGenerator
        f.write(txt)
        f.close
        return design_id

    def generate_DFA(IDs_list):
        """
            DFABuilder.generate_DFA([site_id, building_id, storey_id, space_ids])
        """
        design_id = DFABuilder.make_design_template()

        site_id = IDs_list[0]
        site_args = Site.get_args_from_KB(site_id)
        DFABuilder.make_DFA("site", site_args[0], site_args[1], site_args[2], design_id)
        building_id = IDs_list[1]
        building_args = Building.get_args_from_KB(building_id)
        DFABuilder.make_DFA("building", building_args[0], building_args[1], building_args[2], design_id)
        storey_id = IDs_list[2]
        storey_args = Site.get_args_from_KB(storey_id)
        DFABuilder.make_DFA("storey", storey_args[0], storey_args[1], storey_args[2], design_id)
        space_ids_list = IDs_list[3]
        
        for space_id in space_ids_list:
            space_args = Space.get_args_from_KB(space_id)
            DFABuilder.make_DFA("Space", space_args[0], space_args[1], space_args[2], design_id)
            
        



    # def generate_DFA(type, height, width, length, design_id):

    #     if type == "building":
    #         DFABuilder.make_DFA("building", height, width, length, design_id)

    #     elif type == "site":
    #         DFABuilder.make_DFA("site", height, width, length, design_id)
            
    #     elif type == "space":
    #         DFABuilder.make_DFA("space", height, width, length, design_id)
            
    #     elif type == "storey":
    #         DFABuilder.make_DFA("storey", height, width, length, design_id)
            
DFABuilder.generate_DFA(["building_5655", "site_323232", "storey_24232323", "building_44444"])

#Currently works if these methods are called. 
# make_design_template() has to be called before generate_DFA, and this method must be called
#for each zone you want to add to the .dfa-file. 

# design_id = DFABuilder.make_design_template()
# DFABuilder.generate_DFA("site", 0.2, 300, 500, design_id)
# DFABuilder.generate_DFA("building", 200, 150, 300, design_id)
# DFABuilder.generate_DFA("space", 2, 11, 14, design_id)

# Current issues:
# - Colour only appears on the last added zone
# - Still not implemented a way to select placement of the zones, which probably will mean a big change in the current module. 

