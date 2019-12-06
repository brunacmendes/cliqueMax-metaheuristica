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

class GRASP:

    def __init__(self): 
       
        self.clique = [] #resultado do Max_Clique
        self.instancia = Instancia()
        self.dic_graus_C = dict()
        self.result = []

    def RLC(self, C, d0, d1, alpha):
        RLC = []
        limiar = d1 + alpha*(d0-d1)
        for i in range(len(C)):
            if C[i].getGrau() > limiar: 
                RLC.append(C[i])
        return RLC

    def construct(self, alpha):

        #copia do dicionario de adjacencia
        copia_adj = self.instancia.grafo.dicionario_V_adjacencia.copy()
        
        #V = lista de vertices do grafo
        V = self.instancia.grafo.lista_Vertices
        Q = [] #zera vetor da solucao
        C = V # Lista de Candidatos recebem todos os vertices inicialmente
        while len(C) > 0:
            #cria dicionario com {chave=id vertice | valor=grau} da lista C
            for i in range(len(C)):
                self.dic_graus_C[C[i].getId()] = len(copia_adj[C[i].getId()])

            #pega o menor grau (d1) dos vertices no subgrafo C
            d1_key = min(self.dic_graus_C, key=self.dic_graus_C.get)
            d1 = self.dic_graus_C[int(d1_key)]

            #pega o maior grau (d0) dos vertices no sobgrafo C
            d0_key = max(self.dic_graus_C, key=self.dic_graus_C.get)
            d0 = self.dic_graus_C[int(d0_key)]

            #RCL = lista de vertices candidatos cujo grau > d1 + alpha(d0-d1)
            RLC = self.RLC(C, d0, d1, alpha)
            #seleciona vertice u aleatorio da RCL e coloca na solução clique sendo construida
            u = random.choice(RLC)
            Q.append(u)
            #eliminar vertice u e todos os vértices não adjacentes a ele do conjunto C
            C = copia_adj[u.getId()] # C recebe os adjacentes de u
            if u in C:
                C.remove(u) #remove u

            #remocao dos nao adjacentes da lista de adjacencia
            for i in range(len(V)):
                if not V[i] in C:
                    for j in range(len(copia_adj)):
                            aux = V[j].getId()
                            if V[i] in copia_adj[aux]:
                                copia_adj[aux].remove(V[i])

        return Q  #solucao da iteracao atual
    
    def CalculaH (self, Q):
        '''
        O obj. da funcao eh achar dois vertices v e u que formem um clique com os
        vertices do conjunto Q ao retirar um vertice w
        '''
        H = []
        V = self.instancia.grafo.lista_Vertices
        for i in range(len(Q)): #comprimento do clique inicial
            achou = False
            achou1 = False
            w = Q[i] # w recebe um vertice de Q
            Q_aux = Q.copy() #cria clique auxiliar
            Q_aux.remove(w) #remove w do clique auxiliar
            for j in range (len(V)): #percorre todos os vertices
                v = V[j] #um vertice v de V é selecionado
                for k in range (len(Q_aux)): #percorre o conjunto sem o w
                    if self.instancia.grafo.eh_adjacente(Q_aux[k].getId(), v.getId()) and not self.instancia.grafo.eh_adjacente(w.getId(), v.getId()) and v.getId() != w.getId():
                        achou = True
                    else:
                        #se v nao for clique com algum dos vertices de Q_aux, procurar outro v
                        achou = False
                        break
                if achou:
                    # u tem que ser adjacente a v, obrigatoriamente
                    Lista_possivel_u = self.instancia.grafo.dicionario_adjacencia[v.getId()]
                    for y in range (len(Lista_possivel_u)):
                        for x in range (len(Q_aux)):
                            if self.instancia.grafo.eh_adjacente(Q_aux[x].getId(), Lista_possivel_u[y]) and not self.instancia.grafo.eh_adjacente(w.getId(), Lista_possivel_u[y]):
                                achou1 = True
                            else:
                                achou1 = False
                                break
                        if achou1:
                            u = self.instancia.grafo.busca_Vertice(Lista_possivel_u[y])
                            H.append((v,u,w))
                            break
                    
        return H

    def local(self, Q):   
        H = self.CalculaH(Q)
        while len(H) > 0:
            #escolhe conjunto random de H
            (v, u, w) = random.choice(H)
            #insere u em Q
            Q.append(u)
            #insere v em Q
            Q.append(v)
            #remove w de Q
            Q.remove(w)
            #calcula H
            H = self.CalculaH(Q)

        return Q
    
    def grasp(self, maxitr):
        cliqueSize = -1
        for i in range(maxitr):
            ini = time.time()
            self.instancia.cria_o_grafo()
            alpha = random.random() #alpha = parametro no valor entre 0 e 1
            Q = self.construct(alpha)
            print("Q: " + str(len(Q)))
            Q1 = self.local(Q)
            print("Q1: " + str(len(Q1)))
            print('ITER ' + str(i) + ': ' + str(len(Q1)))
            if len(Q1) > cliqueSize: #se clique encontrado for maior, atualiza a solucao final
                cliqueSize = len(Q1)
                self.clique = Q1

            fim = time.time()
            self.result.append([len(self.clique),fim-ini])
            print('Iteracao ' + str(i) + ' - tempo ' + str(fim-ini))

            return self.result
        
    def executa(self, caminho, iteracoes):
        self.result = []
        self.instancia = Instancia()
        self.instancia.le_benchmarks(caminho)
        #self.instancia.cria_o_grafo()
        resposta = self.grasp(iteracoes)
        #print('MAX. CLIQUE: ' + str(len(self.clique)))

        return resposta

#grasp = GRASP()
#grasp.executa('benchmarks/C125.9.clq')