import random


class IDGenerator():
    
    def create_ID(self):
        """
        Returns "type_rrrrrrrrr" where r = random(0,9) 
        """
        r1 = str(random.randint(0, 9))
        r2 = str(random.randint(0, 9))
        r3 = str(random.randint(0, 9))
        r4 = str(random.randint(0, 9))
        r5 = str(random.randint(0, 9))
        r6 = str(random.randint(0, 9))
        r7 = str(random.randint(0, 9))
        r8 = str(random.randint(0, 9))
        r9 = str(random.randint(0, 9))
        r_all = r1+r2+r3+r4+r5+r6+r7+r8+r9
        id = self.type + "_" + r_all
        print("ID generated for " +self.type+", id = " + id)
        return id

    def create_space_prototype_ID(self):
        '''
        Returns "type_role", role is unique
        '''
        return self.type+"_"+self.role 

