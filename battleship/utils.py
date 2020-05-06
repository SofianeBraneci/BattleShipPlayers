# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:57:39 2020

@author: hp
"""

import numpy as np
from math import factorial
import matplotlib.pyplot as plt
from player import Grille, RandomPlayer, SmartPlayer, PlayerWithStrategy


plt.style.use('ggplot')

def comb(n, p):
    return factorial(n) / (factorial(p) * factorial(n-p))




def E():
    """
        Espérence Theorique = 94.6821 ~ 95
        
    """
    omega = 0
    v = []
    for i in range(17, 100):
        temp = comb(i, 17)
        omega += temp
        v.append(temp)
    
    p = [ x / omega for x in v]
    e = 0
    for i in range(17,17+len(v)):
        e += i * p[i-17]
    print(e)
    
    
def emprical_mean(X, max_iter):
    
    e = 0
    for i in range(len(X)):
        e+= i  * X[i]
    print(e / max_iter)
    
D = {}

def plot_dist(playerClass=RandomPlayer, max_iter=100000):
    """
        affiche la distribution de la variable aléatoire celon la stratégie
        player : la classe à partire de laquelle on instancie l'objet
        max_iter: nombre de partie a jouer
    
    """
    with open('num_fig.txt', 'r') as f:
        num = int(f.readline())
    
    X = np.zeros(100)
    Y = []
    for i in range(max_iter):
#        print(i)
        grid = Grille()
        grid.generer_grille()
        player = playerClass(grid)
        c = player.solve()
        X[c-1] += 1
        Y.append(c)
    emprical_mean(X, max_iter)
    print(np.mean(Y))
    print('--------------')
    # plot la distribution 
    plt.figure(figsize=(8,8))
    plt.plot(X)
    plt.xlabel("Nombre de coups pour terminer une partie")
    plt.ylabel("Nombre de partie joué")
    plt.title("Distribution de la VA X pour le joueur {}".format(playerClass.__name__))
    # sauvegard la figure, commenté la si vous envoulez pas
    plt.savefig("fig_{}.svg".format(num), dpi=200)
    D[playerClass.__name__] = X
    num += 1
    with open('num_fig.txt', 'w') as f:
        print(num, file=f)
    

def n_config():
    l = [5,4,3,3,2]
    n = 100 
    c = 1
    for p in l:
        temp = comb(n, p)
        c *= temp
        n -= p
    print(c)
        
        
players = [RandomPlayer, PlayerWithStrategy,SmartPlayer]

for player in players:
    print(player.__name__)
#    print(D)
    plot_dist(playerClass=player)
#    print(D)
    
# plot la distribution de X des differentes stratégies
plt.figure(figsize=(10,10))
for player in D.keys():
    plt.plot(D[player], label=player)

plt.xlabel("Nombre de coups pour terminer une partie")
plt.ylabel("Nombre de partie joué")
plt.title('Distribution de X selon les différentes stratégies')
plt.legend()
plt.savefig('comparaison3.png', dpi=300)

    

    



