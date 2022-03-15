
class DFABuilder():


    
    
    def makeDFA(height, width, length):
        
        #Read current temp file
        f = open("URL", "r")
        txt = f.read()
        txt_replaced = txt.replace("<HEIGTH>", str(height))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<LENGTH>", str(length))

        #Make new DFA file
        f = open("URL", "w")
        f.write(txt_replaced)
        f.close
