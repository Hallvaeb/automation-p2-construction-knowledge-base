from IDGenerator import IDGenerator

#Prototype of the class works. Currently every dfa made will be named "order_17", but a methid to automize this is easily implemented. 
class DFABuilder():

    
    def make_DFA(type, height, width, length):
        id = IDGenerator.create_ID()
        #Read current temp file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/" + type +".dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<LENGTH>", str(length))
        txt_replaced = txt_replaced.replace("block1", str(id)) 
        f.close()

        #Make new DFA file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/tempo_" + type + ".dfa", "w")
        f.write(txt_replaced)
        f.close

        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/Products/" + "order_17" + ".dfa", "a")
        #TODO switch "building_12" with IDGenerator
        f.write(txt_replaced)
        f.close


    def make_design_template(): #Should take some form of ID for the order, def makeDesignTemplate(key):
        #Design
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/design.dfa", "r")
        txt = f.read()
        txt = txt.replace("<ID>", "order_17") #TODO replace order 13 with automated id.
        f.close()
        #Design
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/tempo_design.dfa", "w")
        f.write(txt)
        f.close
        #Design
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/Products/" + "order_17" + ".dfa", "a")
        #TODO switch "building_12" with IDGenerator
        f.write(txt)
        f.close

    def generate_DFA(type, height, width, length):

        if type == "building":
            DFABuilder.make_DFA("building", height, width, length)

        elif type == "site":
            DFABuilder.make_DFA("site", height, width, length)
            
        elif type == "space":
            DFABuilder.make_DFA("space", height, width, length)
            
        elif type == "storey":
            DFABuilder.make_DFA("storey", height, width, length)
            

    def extract_DFA_file(path):
        pass


#Prototype currently works if these methods are called. make_design_template() has to be called before generate_DFA, and this method must be called
#for each zone you want to add to the .dfa-file. 

DFABuilder.make_design_template()
DFABuilder.generate_DFA("site", 0.2, 300, 500)
DFABuilder.generate_DFA("building", 200, 150, 300)
DFABuilder.generate_DFA("space", 2, 11, 14)

# Current issues:
# - Colour only appears on the last added zone
# - Still not implemented a way to select placement of the zones, which probably will mean a big change in the current module. 

