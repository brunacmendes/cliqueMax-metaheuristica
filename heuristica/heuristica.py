import numpy as np
import sys
import pulp as p
from Grafo import Grafo
import random
import time

class Heuristica:

    def __init__(self): 
        self.matriz = []
        self.tamanho = 0
        self.grafo = Grafo()
        self.vetor_de_graus = []
        self.result = []

    def le_benchmarks(self, nome):
        # pega o nome do arquivo
        # nome = str(input('Nome do arquivo: '))
        try:
            arq = open(nome, 'r')  # abre arquivo
            texto = arq.readlines()  # le arquivo inteiro
            for linha in texto:  # cada linha é uma string
                # divide as strings da linha e coloca os valores no formato de lista.
                linha = linha.split(' ')
                if linha[0] == 'p':
                    # cria matriz
                    self.cria_matriz(int(linha[2]))  # numero vertices
                if linha[0] == 'e':
                    # quando achar o arco, a posiçao fica sendo 0
                    # dessa forma, uma matriz complementar de E já é gerada
                    self.matriz[int(linha[1])-1][int(linha[2])-1] = 0
                    self.matriz[int(linha[2])-1][int(linha[1])-1] = 0

            arq.close()  # fecha arquivo

        except IOError:  # exceção para tratar quando o nome do arquivo estiver incorreto
            print('Arquivo não existe!')

    def cria_matriz(self, dimensao):
        # criar e preencher a matriz com valores 1
        self.matriz = np.ones((dimensao, dimensao), dtype=np.float64)
        self.tamanho = dimensao

    def cria_o_grafo (self):
        self.vetor_de_graus = np.zeros(self.tamanho, dtype=np.float64)

        for i in range (self.tamanho):
             self.grafo.novo_Vertice(i)

        for i in range(1,self.tamanho):
            for j in range(i):
                if self.matriz[i][j] == 0:
                    self.grafo.nova_Aresta(i,j)
                    self.vetor_de_graus[i] += 1
                    self.vetor_de_graus[j] += 1
                    self.grafo.busca_Vertice(i).setGrau(self.grafo.busca_Vertice(i).getGrau() + 1)
                    self.grafo.busca_Vertice(j).setGrau(self.grafo.busca_Vertice(j).getGrau() + 1)
        self.tupla_de_graus = tuple(self.vetor_de_graus)
       
    def cria_lista_vertices(self):
        # cria lista com 10% dos vertices de maior grau do grafo
        vetor_aux = []
        vetor_aux.append(self.tupla_de_graus)
        vetor_aux = np.array(vetor_aux)
        vetor_aux = vetor_aux[0]
        ten_percent = int(self.tamanho * 0.3)
        if ten_percent < 1:
            ten_percent = 1
        lista10 = []
        
        while len(lista10) < int(ten_percent):
            #pega o index do maior valor
            ind = np.unravel_index(np.argmax(vetor_aux, axis=None), vetor_aux.shape)
            if self.grafo.busca_Vertice(ind[0]).getUsado() == False:
                lista10.append(ind[0])
                vetor_aux[ind[0]] = 0
            elif vetor_aux[ind[0]] == 0:
                #signfica que o grafo é muito pequeno para tantas iteracoes
                self.grafo.liberar_nos([])
            else:
                vetor_aux[ind[0]] = 0
        return lista10

    def ordena_vertices_adjacentes_pelo_grau(self, v):

        adjacentes = self.grafo.busca_Adjacentes(v)
        qtd_vertices = len(adjacentes)
        ordenado = []
        lista_tupla = []

        for i in range(qtd_vertices):
            vertice = self.grafo.busca_Vertice(adjacentes[i])
            grau = self.grafo.grau(vertice)
            lista_tupla.append((adjacentes[i],grau))

        lista_tupla.sort(key=lambda x: x[1])
        ordenado, _ = zip(*lista_tupla)
        ordenado = list(ordenado)    
        return ordenado[::-1]

    def heuristica_baseada_GRASP(self, iteracoes):
        solucao = []

        for m in range(iteracoes):
            ini = time.time()
            solucao_aux = []

            # lista de vertices de maior grau (amostragem = 10% dos vertices)
            lista_vertices = self.cria_lista_vertices()
        
            # seleciona um vertice aleatorio da lista_vertices
            v = random.choice(lista_vertices)
            print('vertice escolhido: ' + str(v))
            self.grafo.busca_Vertice(v).setUsado(True)

            # insere vertice na solucao_aux
            solucao_aux.append(v)

            # cria lista (ordenada pelo grau) de vertices adjacentes do vertice escolhido
            ini2 = time.time()
            lista_vertices_adjacentes = self.ordena_vertices_adjacentes_pelo_grau(v)
            fim2 = time.time()
            print('tempo ordenacao: ' + str(fim2-ini2)) 

            for a in range(len(lista_vertices_adjacentes)):
                vertice = lista_vertices_adjacentes[a]
                for h in range(len(solucao_aux)): # se a forma um clique com os vertices dentro de solucao_aux, coloca ele junto na solucao_aux
                    vertice_solucao = solucao_aux[h]
                    if self.grafo.eh_adjacente(vertice,vertice_solucao) or self.grafo.eh_adjacente(vertice_solucao,vertice) :
                        coloca = True
                    else:
                        coloca = False
                        break
                if coloca:
                    solucao_aux.append(lista_vertices_adjacentes[a])

                if len(solucao_aux) > len(solucao):  # verificar se eh a melhor solução encontrada
                    solucao = solucao_aux

                # coloca o primeiro elemento da lista_vertices_adjacentes na ultima posicao
                #primeiro = lista_vertices_adjacentes.pop(0)
                #lista_vertices_adjacentes.insert(len(lista_vertices_adjacentes)+1, primeiro)
            fim = time.time()
            self.result.append([len(solucao_aux),fim-ini])
            print('Iteracao ' + str(m) + ' - tempo ' + str(fim-ini))

        return self.result

    def printa_solucao_heuristica(self, solucao, tamanho_clique):
        print('\n\n SOLUÇÃO: ')
        for i in range(len(solucao)):
            print(str(solucao[i]))    
        print("\nTAMANHO DO CLIQUE: " + str(tamanho_clique))


    def executa(self, caminho, iteracoes):
        self.result = []
        self.le_benchmarks(caminho)
        self.cria_o_grafo()
        resposta = self.heuristica_baseada_GRASP(iteracoes)
        
        return resposta
