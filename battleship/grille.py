# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 21:03:10 2020

@author: hp
"""
import numpy as np
import matplotlib.pyplot as plt
from navires import Croiseur, Torpilleur, ContreTorpilleur, SousMarin, PortAvion


class Grille(object):
    """
        Classe qui represente la grille du jeux de naval
        direction 1:horizontal, 2:veticale
        
        *****************IMPORTANT*******************
        tout les navires qui sont passé en paramètre
        doivent être des objet
        même les list de navire doivent 
        contenire des objet des classes navires différentes
    """
    def __init__(self, shape=(10,10)):
        self.grille = np.zeros(shape)
        self.remaining = 0
        self.ships = {}
    
    def affiche(self):
        """
            Crée une image 
        """

        plt.figure(figsize=(10, 10))
        plt.imshow(self.grille, cmap='viridis')
        
    
    def peut_placer(self, navire, pos, direction=1):
       """ navire: un objet de type navire
            pos: tuple
            direction: int {1,2}
            ---------
            return bool
            
            exemple 
            self.peut_placer(SousMarin(), (0,0), 1)
       """
        
        
       if direction == 1:
           # vertical
#           print(self.grille[pos[0]: navire.get_size(),pos[1]].size, self.grille[pos[0]: navire.get_size(),pos[1]])
           if len(self.grille[pos[0]:pos[0] + navire.get_size(),pos[1]]) < navire.get_size(): 
               return False
           return np.all(self.grille[pos[0]: pos[0] + navire.get_size(),pos[1]] == 0)
       else:
           # horizontal
#           print(self.grille[pos[0], pos[1]:pos[1] + navire.get_size()].size, self.grille[pos[0], pos[1]:pos[1] + navire.get_size()] )
           if len(self.grille[pos[0], pos[1]: pos[1] + navire.get_size()]) < navire.get_size():
               return False
           return np.all(self.grille[pos[0], pos[1]:pos[1] + navire.get_size()]==0)
        
        
    def placer(self, navire, pos, direction=1):
        """ navire: un objet de type navire
            pos: tuple
            direction: int {1,2}
            ---------
            exemple 
            self.peut_placer(SousMarin(), (0,0), 1)
        """
        if self.peut_placer(navire, pos, direction):
            if direction == 1:
                self.grille[pos[0]: pos[0] + navire.get_size(),pos[1]] = navire.get_num()
            else:
                self.grille[pos[0], pos[1]:pos[1] + navire.get_size()] = navire.get_num()



            
    def placer_alea(self, navire, direction):
        """
            essaye de placer le navire dans la grille selon la direction spécifié
            
            navire: objet de type navire
            direction: int {1,2}
            --------
            self.placer(SousMarin(), 1)
            
        """
        placed = False
        while not placed:
            row, col = np.random.randint(low=0, high=self.grille.shape[0], size=2)
            if self.peut_placer(navire, (row, col), direction):
                self.placer(navire, (row, col), direction)
                placed = True
                
        
    def generer_grille(self):
        """
            a partire d'une liste de navires on génére une grille complete du jeux
            
        """
        
        navires =[PortAvion, Croiseur, SousMarin, Torpilleur, ContreTorpilleur]#, Croiseur, SousMarin, ContreTorpilleur, Torpilleur]
        dirs = [1, 2]
        
        for i in range(len(navires)):
            d = dirs[np.random.randint(0, len(dirs))]
            navire =  navires[i]()
#            print(navire.get_size)
            self.placer_alea(navire, d)
            self.remaining += navire.get_size()
            self.ships[navire.get_num()] = navire.get_size()
            # selon les ids
#        print(self.ships)
            
    def eq(self, grilleB):
        """
            test l'égalité de deux objet de type Grille
            -----------
            return bool
            -----------
            exemple
            G1 = Grille()
            G2 = Grille()
            G1.generer_grille()
            G2.generer_grille()
            G1.eq(G2)
           
        """
        return np.array_equal(self.grille, grilleB.grille)
    
    def denombrer(self, navire):
        """
            calcule le nombre de cofiguration pour un navire donné
            
            navire: object de Type navire
            ---------
            return int
            ----------
            exeple
            grille = Grille()
            navire = PortAvion()
            grille.denombrer(navire) -> 120
        """
        return (self.grille.shape[0] -  navire.get_size() + 1) * self.grille.shape[0] * 2

                                        
    def copy(self):
        """
            crée une copie de la grille
        """
        
        new = Grille()
        new.grille = np.copy(self.grille)
        return new
    
    def reset(self):
        """
            réinitialise la grille
        """
        self.grille = np.zeros_like(self.grille)
        self.remaining = 0
        self.ships = {}
        
    def num_grille_gen(self):
        """
            Q4 partie 2
            retourn le nombre de grille généré
            -----------
            return int
        
        """
        
        count = 1
        g = self.copy()
        g.reset()
        g.generer_grille()
        
        while not self.eq(g):
            g.reset()
            g.generer_grille()
            count += 1
#        g.affiche()
        return count
    
    def approximer(self, max_iter=100):
        """
            Q5 partie 2
            permet d'approximer le nombre de grille genéré pour une liste de navire
            --------------
            return int
        """
        count = 0
        for _ in range(max_iter):
            count += self.num_grille_gen()
        return count / max_iter
    
    def get_ship(self, ship_id):
        """
            retourn le type de navire
            ------------
            return str
        """
        return ['PA', 'C', 'CT', 'SM','T'][ship_id - 1]
        
            
def count_recu(grille, navire):
        """
            calcul le nombre de configuration pour une liste de navires
            grille: objet de type Grille()
            navires: liste d'objet de type navire
            -----------
            return int
            -----------
            exemple
            from grille import count_recu
            grille = Grille()
            navire = [SousMarin(), Torpilleur()]
            config = count_recu(grille, navire)
        """
        count = 0
        if len(navire) == 1:
            for i in range(grille.grille.shape[0]):
                for j in range(grille.grille.shape[1]):
                    # si il peut etre placé verticalement
                    if grille.peut_placer(navire[0], (i, j), 1):
                        count += 1
                    # si il peut etre placé horizontalement
                    if grille.peut_placer(navire[0], (i, j), 2):
                        count += 1
            return count
        else:
            for i in range(grille.grille.shape[0]):
                for j in range(grille.grille.shape[1]):
                    # si il peut etre placé verticalement
                    if grille.peut_placer(navire[0], (i, j), 1):
                        
                        copy = grille.copy()
                        #placer le navire
                        copy.placer(navire[0], (i, j), 1)
                        # executer la meme procedure sur la nouvelle grille et les navires restant
                        count += count_recu(copy, [n for n in navire[1:]])
                    if grille.peut_placer(navire[0], (i, j), 2):  
                         copy = grille.copy()
                         # placer le navire
                         copy.placer(navire[0], (i, j), 2)
                         # executer la meme procedure sur la nouvelle grille et les navires restant
                         count += count_recu(copy, [n for n in navire[1:]])
            return count
                        
            
    