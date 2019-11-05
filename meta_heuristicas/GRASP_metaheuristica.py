import numpy as np
import sys
import pulp as p
from Grafo import Grafo
from heuristica.heuristica import Heuristica
import random
import time

class GRASP:

    def __init__(self): 
        self.matriz = [] #matriz correspondente ao grafo
        self.tamanho = 0 #dimensao da matriz
        self.grafo = Grafo()
        self.heuristica = Heuristica()
        self.vetor_de_graus = []
        self.clique = [] #resultado do Max_Clique

    def construct(self, V, E, alpha, Q):
        #V = lista de vertices do grafo
        clique = 0
        C = V
        while len(C) > 0:
            #pega o menor grau (d1) dos vertices no subgrafo C
            #pega o maior grau (d0) dos vertices no sobgrafo C
            pass
        pass


    def local(self, V, E, Q):
        pass
    
    def grasp(self, V, E, maxitr, Q):
        cliqueSize = -1

        pass
    
    def cliquee(self, V, E, maxitr, Tg, Q):
        pass

    def executa(self):
        pass