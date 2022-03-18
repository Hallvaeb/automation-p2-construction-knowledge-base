#import requests



class DFABuilder():


    
    
    def makeDFA(type, height, width, length):

        #Read current temp file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/" + str(type) ".dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<LENGTH>", str(length))
        txt_replaced = txt_replaced.replace("<ID>", str(type) +"_12") #TODO automize the ID part
        f.close()

        #Make new DFA file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/tempo_" + str(type) + ".dfa", "w")
        f.write(txt_replaced)
        f.close

        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/Products/" + str(type) +"_12" + ".dfa", "a")
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
        match type:
            case 1:
                type = "building"
                return DFABuilder.makeDFA("building", height, width, length)

            case 2:
                type = "site"
                return DFABuilder.makeDFA("site", height, width, length)
            
            case 3:
                type = "site"
                return DFABuilder.makeDFA("site", height, width, length)
            
            case 4:
                type = "site"
                return DFABuilder.makeDFA("site", height, width, length)
            
    


    def extractDFAfile(path):
        pass