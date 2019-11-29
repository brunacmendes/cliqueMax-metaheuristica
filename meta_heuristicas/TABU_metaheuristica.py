import os, sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import numpy as np
import pulp as p
from estrutura_dados.Grafo import Grafo
from estrutura_dados.Instancia import Instancia
import random
import time

'''
GRUPO: Bruna Mendes 0021528, Flávia 0022651, Luís Fernando 0022644
Professor: Diego
Disciplina: Meta-Heurística

'''
class TABU: #Variable Neighbourhood Search
    def __init__(self): 
        self.clique = [] #resultado do Max_Clique
        self.instancia = Instancia()
        self.tabu_list = []

    def multistart(self, k, L, maxIter):
        #clique inicial
        S = random.choice(self.instancia.grafo)
        Iter = 0
        while Iter < maxIter:
            S_best = self.TS(S,k, L, Iter)
            #se S_best é um clique legal, retorna S e para

            #else
            #S_best = construcao de uma nova solucao


        return -1 #failure

    def TS(self, S, k, L, Iter):
        I = 0
        S_best = S
        while I < L:

            Iter = Iter + 1
            if len(S) > len(S_best):
                S_best = S
                I = 0
            else:
                I = I + 1

        

        return S_best
        

    def executa(self, caminho, iteracoes):
        self.result = []
        self.instancia = Instancia()
        self.instancia.le_benchmarks(caminho)
        self.instancia.cria_o_grafo()
        resposta = self.multistart(20, 100, iteracoes)
        #print('MAX. CLIQUE: ' + str(len(self.clique)))

        return resposta