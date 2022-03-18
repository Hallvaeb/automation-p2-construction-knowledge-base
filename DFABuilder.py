#import requests



class DFABuilder():

    
    def makeDFA(type, height, width, length):

        #Read current temp file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/" + type +".dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<LENGTH>", str(length))
        txt_replaced = txt_replaced.replace("<ID>", "order_13") #TODO automize the ID part
        f.close()

        #Make new DFA file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/tempo_" + type + ".dfa", "w")
        f.write(txt_replaced)
        f.close

        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/Products/" + "order_13" + ".dfa", "a")
        #TODO switch "building_12" with IDGenerator
        f.write(txt_replaced)
        f.close


        #Upload DFA file to URL
        #f = open("FILE", "r")
        #uploaded = requests.post("URL", files = {"form_field_name": f})
        #if uploaded.ok:
        #   print("File uploaded successfully !")
        #    print(uploaded.text)
        #else:
        #    print("Please Upload again !")

    def generateDFA(type, height, width, length):
        

        if type == "building":
            DFABuilder.makeDFA("building", height, width, length)

        elif type == "site":
            DFABuilder.makeDFA("site", height, width, length)
            
        elif type == "space":
            DFABuilder.makeDFA("space", height, width, length)
            
        elif type == "storey":
            DFABuilder.makeDFA("storey", height, width, length)
            
    



    def extractDFAfile(path):
        pass

DFABuilder.generateDFA("site", 0.2, 300, 500)
