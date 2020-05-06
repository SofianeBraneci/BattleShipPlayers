# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:20:08 2020

@author: hp
"""
from grille import np, plt, Grille

"""
**********IMPORTANT*********
Tout les types de joueur prennent 
en paramétre un grille qui a était généré
-------
exemple
grille = Grille()
grille.generer_grille()
player = SmartPlayer(grille) # ou autre joueur
payer.solve() # retourn le nombre de coups tiré

"""
class SmartPlayer(object):
    """
        Impementation de la version probabiliste
    """    
    
    def __init__(self,grid):
        # grille généré 
        self.grid = grid
        # matice des proba
        self.m = np.zeros((10,10))
        #matrix state 0: Unknow, 1:Miss, 2: Hit!
        self.state = np.zeros((10,10))
        # mode de calcul
        self.proba_mode = "hunt"
        # coulé ou non
        self.sunk = False
        self.targets = {1:5, 2:4, 3:3, 4:3, 5:2}
        # longeur des navires
        self.lengths = [5,4,3,3,2]

    
    def count_occurences(self, arr, e=2):
#        print(arr)
        counter = 0
        for i in arr:
            if i == e:
                counter += 1
        return counter
        
    def checkH(self, pos, length):
        """
            verifie s'il un navire de taille length 
            peut etre poisitioné a partir de pos
            
        """
        x, y = pos
        if self.proba_mode == 'hunt':
            if len(self.m[x, y: y+length]) >= length:
                if self.can_fitH(pos, length):
                    # incrementé tout les case
                    self.m[x, y:y+length] +=1
        else:
            if len(self.m[x, y: y+length]) >= length:
                if not self.can_fitH(pos, length):
                    return
                else:
                    k = self.count_occurences(self.state[x, y: y+length])
                    # favorisé les cases qui contiennent les autres parties du navire
                    self.m[x, y: y+length] += k
                    return 
    
    def can_fitH(self, pos, length):
        x, y = pos
        for j in range(y, y+length):
            if self.state[x, j] == 1:
                return False
        return True
    
    def can_fitV(self, pos, length):
        x, y = pos
        for i in range(x, x+length):
            if self.state[i, y] == 1:
                return False
        return True
        
        
                
                
    
    def checkV(self, pos, length):
        """
            verifie s'il un navire de taille length 
            peut etre poisitioné a partir de pos
            
        """
        x, y = pos
        if self.proba_mode=='hunt':
            if len(self.state[x:x+length, y]) >= length:
                if self.can_fitV(pos, length):
                    self.m[x:x+length, y] +=1
            return
        else:
            if len(self.m[x:x+length, y]) >= length:
                if not self.can_fitV(pos, length):
                    return
                else:
                    k = self.count_occurences(self.state[x:x+length, y])
                    self.m[x:x+length, y] += k
                    return
                
    def play(self, pos):
        """ joue un coups sur la position pos"""
        x, y = pos
        
        if self.grid.grille[x, y] == 0 or self.grid.grille[x, y] == -1:
            self.grid.grille[x, y] = -1
            # missed
            self.state[x, y] = 1
            return False
        
        
        which = int(self.grid.grille[x, y])
        self.grid.grille[x, y] = -1
        self.grid.ships[which] -= 1
        self.grid.remaining -= 1
        # hit !
        self.state[x, y] = 2
        if self.grid.ships[which] == 0:
            del self.grid.ships[which]
            self.lengths.remove(self.targets[which])
            del self.targets[which]
            self.sunk = True
        # after this target mode is activated !
        return True
    
    
    def compute(self, length):
        """calcul la matrice des probabilités"""
        self.m = np.zeros((10,10))
        for i in range(10):
            for j in range(10):
                self.checkH((i, j), length)
                self.checkV((i, j), length)
    
    def display(self):
        # affiche 
        plt.imshow(self.m)
        
    
    def config(self):
        print(self.grid.grille)
        print(self.grid.ships)
        
    def max_probv2(self):
        """retourn la position de la proba max"""
        m = -999
        x, y = 0, 0
        for i in range(10):
            for j in range(10):
                temp = int(self.m[i, j])
#                print(temp)
#                print(type(self.m[i, j]))
                if temp > m:
                    m = self.m[i, j]
                    x, y = i, j
        return x, y

    def drop_probs(self, positions=[] ):
        """élimine les proba des cases déja joué"""
        for pos in positions:
            self.m[pos] = 0
                    

            
    def solve(self):
        """
            retourn le nombre de coups tiré pour finir le jeux
        """
        played = []
        count = 0
        while self.grid.remaining > 0:
            
            for length in self.lengths:
                
                if self.sunk and self.proba_mode == 'target':
                    self.sunk = False
                    self.proba_mode = 'hunt'
                
                self.compute(length)
                self.drop_probs(played)
                pos = self.max_probv2()
                
                if pos not in played:
                    count += 1
                    hit = self.play(pos)
                    played.append(pos)
                    if hit:
                        self.proba_mode = 'target'
        return count
    




class RandomPlayer(object):
    """
        Impelentation de la version aléatoire du jeux
    """
    
    def __init__(self,grid):
        self.grid = grid
        
    def take_random_guess(self,):
        """retourn un x et y entre [0,10)"""
        return np.random.randint(0,10), np.random.randint(0,10)
    
    
    def play(self, pos):
        """
            tire sur la position pos
            -------
            return bool
        """
        x, y = pos
        # miss
        if self.grid.grille[x, y] == -1 or self.grid.grille[x, y] == 0:
            self.grid.grille[x, y] = -1
            return False
        # hit
        
        self.grid.grille[x, y] = -1
        self.grid.remaining -= 1
        return True
     
    
    def solve(self):
        """
            retourn le nombre coups tiré
            
        """
        played = []
        count = 0
        
        while self.grid.remaining > 0:
            pos = self.take_random_guess()
            if pos not in played:
                self.play(pos)
                played.append(pos)
                count += 1
        return count
    
    
    
    
class PlayerWithStrategy(object):
    """
        Implementation de la version heristique de l'énoncé
        
    """
    
    def __init__(self, grid):
        self.grid = grid
        self.adj = []
        self.hunt = True
        
    
    def find_adj(self, pos):
        """trouve les positions adjacentes a pos"""
        x, y = pos
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
#        adj = []
        
        for i in range(len(dx)):
            xx = dx[i] + x
            yy = dy[i] + y
            
            if xx < 0 or yy < 0: continue
            if xx > 9 or yy > 9: continue
        
            self.adj.append((xx, yy))

    def play(self, pos):
        """
            tire sur la position pos
            ---------
            return bool
        """
        x, y = pos
        if self.grid.grille[x, y] == 0 or self.grid.grille[x, y] == -1:
            self.grid.grille[x, y] == -1
            return False
        self.hunt = False
        self.grid.grille[x, y] = -1
        self.grid.remaining -= 1
        return True
    
    def take_random_guess(self,):
        """retourn un x et y entre [0,10)"""
        return np.random.randint(0,10), np.random.randint(0,10)
    
    
    def solve(self):
        """retourn le nombre de coups tiré pour terminé la partie"""
        played = []
        counter = 0
        while self.grid.remaining > 0:
            # hunt mode 
            if self.hunt:
                pos = self.take_random_guess()
            else:
                # target mode on explore 
                pos = self.adj.pop()
                if len(self.adj) == 0:
                    self.hunt = True
            
            if pos not in played:
                counter += 1
                played.append(pos)
                feedback = self.play(pos)
                # si touché on cherche les position adjacentes
                if feedback == True:
                    
                    self.find_adj(pos)
                    
        return counter


        
    

            
            
                
        
        
        
        
        
        
        
                
#X = np.zeros(100)
#
#for i in range(10000):
#    grid = Grille()
#    grid.generer_grille()
#    player = PlayerWithStrategy(grid)
#    c  =player.solve()
#    X[c-1] += 1
#plt.plot(X)

