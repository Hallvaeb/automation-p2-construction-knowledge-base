#import requests



class DFABuilder():


    
    
    def makeDFA(height, width, length):
        
        #Read current temp file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/building.dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<LENGTH>", str(length))
        f.close()

        #Make new DFA file
        f = open("C:/Users/sigve/OneDrive/Dokumenter/NTNU/V2022/Automatisering prosjekt/kbe-a2/DFAs/building.dfa", "w")
        f.write(txt_replaced)
        f.close

        #f = open("FILE" + ".dfa", "a")
        #f.write(txt_replaced)
        #f.close


        #Upload DFA file to URL
        #f = open("FILE", "r")
        #uploaded = requests.post("URL", files = {"form_field_name": f})
        #if uploaded.ok:
        #   print("File uploaded successfully !")
        #    print(uploaded.text)
        #else:
        #    print("Please Upload again !")
    


    def extractDFAfile(path):
        pass