# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 21:29:12 2020

@author: hp
"""

class Navire(object):
    def __init__(self, num, size):
        
        if num == 0 or size == 0: 
            raise ValueError("num > 0 et size > 0")
        self.num = num
        self.size = size
        self.name = "Navire"
        
    def get_num(self):
        return self.num
    
    def get_size(self):
        return self.size
    def __repr__(self):
        return "\tType: {}, id : {},  longeur : {}".format(self.name,self.num, self.size)
    
    
    

class PortAvion(Navire):
    
    def __init__(self, num=1, size=5):
        Navire.__init__(self, num, size)
        self.name = "Port Avion"


class Croiseur(Navire):
    
    def __init__(self, num=2, size=4):
        Navire.__init__(self, num, size)
        self.name = "Croiseur"

class ContreTorpilleur(Navire):
    
    def __init__(self, num=3, size=3):
        Navire.__init__(self, num, size)
        self.name = "Contre Torpilleur"


class SousMarin(Navire):
    
    def __init__(self, num=4, size=3):
        Navire.__init__(self, num, size)
        self.name = "Sous Marin"

class Torpilleur(Navire):
    
    def __init__(self, num=5, size=2):
        Navire.__init__(self, num, size)
        self.name = "Torpilleur"