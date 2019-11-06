import sys
import numpy as np
import pulp as p
from estrutura_dados.Grafo import Grafo
from estrutura_dados.Instancia import Instancia
import random
import time

class GRASP:

    def __init__(self): 
       
        self.clique = [] #resultado do Max_Clique
        self.instancia = Instancia()
        self.dic_graus_C = dict()     


    def RLC(self, C, d0, d1, alpha):
        RLC = []
        for i in range(len(C)):
            if C[i].getGrau() > d1 + alpha*(d0-d1):
                RLC.append(C[i])
        return RLC

    def construct(self, alpha):
       
        #V = lista de vertices do grafo
        V = self.instancia.grafo.lista_Vertices
       
        Q = [] #zera vetor da solucao
        C = V # Lista de Candidatos recebem todos os vertices inicialmente
        while len(C) > 0:
            #cria dicionario com {chave=id vertice | valor=grau} da lista C
            for i in range(len(C)):
                self.dic_graus_C[C[i].getId()] = C[i].getGrau()

            #pega o menor grau (d1) dos vertices no subgrafo C
            d1 = min(self.dic_graus_C, value=self.dic_graus_C.get)

            #pega o maior grau (d0) dos vertices no sobgrafo C
            d0 = max(self.dic_graus_C, value=self.dic_graus_C.get)

            #RCL = lista de vertices candidatos cujo grau > d1 + alpha(d0-d1)
            RLC = self.RLC(C, d0, d1, alpha)
            #seleciona vertice u aleatorio da RCL e coloca na solução clique sendo construida
            u = random.choice(RLC)
            Q.append(u)
            #eliminar vertice u e todos os vértices não adjacentes a ele do conjunto C
            C = self.instancia.grafo.busca_V_Adjacentes(u.getId())

        return Q  #solucao da iteracao atual

    def local(self, Q):
        return Q
    
    def grasp(self, maxitr):
        cliqueSize = -1
        for i in range(maxitr):
            alpha = random.random() #alpha = parametro no valor entre 0 e 1
            Q = self.construct(alpha)
            Q1 = self.local(Q)
            print('ITER ' + str(i) + ': ' + str(len(Q1)))
            if len(Q1) > cliqueSize: #se clique encontrado for maior, atualiza a solucao final
                cliqueSize = len(Q1)
                self.clique = Q1

        
    def executa(self, caminho):
        self.instancia.le_benchmarks(caminho)
        self.instancia.cria_o_grafo()
        self.grasp(1)
        print('MAX. CLIQUE: ' + str(len(self.clique)))

grasp = GRASP()
grasp.executa('benchmarks/C125.9.clq')