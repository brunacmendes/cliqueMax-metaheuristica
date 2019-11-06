from Grafo import Grafo
import numpy as np
import sys
 
class Instancia:

    def __init__(self): 
        self.matriz = [] #matriz correspondente ao grafo
        self.tamanho = 0 #dimensao da matriz
        self.grafo = Grafo()
        self.vetor_de_graus = []
 
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