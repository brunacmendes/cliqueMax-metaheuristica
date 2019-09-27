import numpy as np
import sys
import pulp as p
from Grafo import Grafo
import random
import time


class Principal:

    def __init__(self):
        # tentativas = alpha * total_de_vertices
        self.alpha_tentativas = 0.1
        self.matriz = []
        self.tamanho = 0
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

    def printa_matriz(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                print(str(self.matriz[i][j]) + " | ", end="")
            print("")

################################## CLIQUE MAXIMA DETERMINISTICA ################################

    def resolve_puLP(self):
        # Cria o problema
        prob = p.LpProblem("Benchmark 01", p.LpMaximize)
 
        # Cria as variaveis
        x = np.zeros(self.tamanho, dtype=p.LpVariable)
        for i in range(self.tamanho):
            x[i] = p.LpVariable("x" + str(i+1), 0, 1, 'Binary')

        # Cria a funcao objetivo
        lista = []
        for i in range(self.tamanho):
            lista += x[i]

        prob += lista

        # Restricoes
        for i in range(1, self.tamanho):
            for j in range(i):
                if self.matriz[i][j] == 1:
                    prob += x[i] + x[j] <= 1, "Arco" + \
                        str(i+1) + "." + str(j+1)

                # Escreve o modelo no arquivo
        prob.writeLP("CLIQUEModelo.lp")

        # Resolve o problema
        prob.solve()

        # Imprime o status da resolucao
        print("Status:", p.LpStatus[prob.status])

        # Solucoes otimas das variaveis
        for variable in prob.variables():
            print("%s = %f" % (variable.name, variable.varValue))

        # Objetivo otimizado
        print("Clique Maxima: %0.2f" % p.value(prob.objective))

    def gera_saida_GLPK(self):
        open("CLIQUEModelo.mod", "w").close()
        f = open("CLIQUEModelo.mod", "a")

        for i in range(self.tamanho):
            f.write("var x" + str(i+1) + " binary;\n")

        f.write("\n")
        f.write("maximize NumNos: ")
        for i in range(self.tamanho-1):
            f.write("x" + str(i+1) + " + ")

        f.write("x" + str(self.tamanho)+";\n\n")
        f.write("subject to \n\n")

        for i in range(1, self.tamanho):
            for j in range(i):
                if self.matriz[i][j] == 1:
                    f.write("arco" + str(j+1) + "_" + str(i+1) + ": " +
                            "x" + str(j+1) + " + " + "x" + str(i+1) + " <= 1; \n")
        f.write("\n")
        f.write("solve;\n")
        f.write("display NumNos, ")
        for i in range(self.tamanho-1):
            f.write("x" + str(i+1) + ", ")
        f.write("x" + str(self.tamanho) + ";")
        f.close()

#################################### CLIQUE MAXIMA HEURISTICA ##################################

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
       
    def cria_lista_vertices(self):
        # cria lista com 10% dos vertices de maior grau do grafo
        ten_percent = int(self.tamanho * 0.1)
        if ten_percent < 1:
            ten_percent = 1
        lista10 = []
        i = 0
        while i < ten_percent:
            ind = np.unravel_index(np.argmax(self.vetor_de_graus, axis=None), self.vetor_de_graus.shape)
            lista10.append(ind[0])
            self.vetor_de_graus[ind[0]] = 0
            i+=1
        return lista10

    def ordena_vertices_adjacentes_pelo_grau(self, v):
        vertice = self.grafo.busca_Vertice(v)
        qtd_vertices = self.grafo.grau(vertice)
        ordenado = []
        lista_tupla = []

        i = 0
        while i <= qtd_vertices:
            adjacente = self.grafo.busca_Adjacente(vertice)
            if adjacente != None:
                grau = self.grafo.grau(adjacente)
                adjacente = adjacente.getId()
                lista_tupla.append((adjacente,grau))
            i+=1
        
        lista_tupla.sort(key=lambda x: x[1])
        ordenado, inutil = zip(*lista_tupla)
        inutil=inutil
        ordenado = list(ordenado)
        #desvisitar nos depois de criar a lista
        self.grafo.desvisitar_nos(ordenado)
        return ordenado[::-1]

    def heuristica_baseada_GRASP(self, iteracoes):
        solucao = []
        # Funcao cria_o_grafo foi movido para fora desta funcao
        # self.cria_o_grafo()

        # lista de vertices de maior grau (amostragem = 10% dos vertices)
        lista_vertices = self.cria_lista_vertices()

        for m in range(iteracoes):
            m=m
            solucao_aux = []

            # seleciona um vertice aleatorio da lista_vertices
            v = random.choice(list(lista_vertices))

            #remover vertice para nao sortear o mesmo na proxima iteracao
            lista_vertices.remove(v)
        
            # insere vertice na solucao_aux
            solucao_aux.append(v)

            # cria lista (ordenada pelo grau) de vertices adjacentes do vertice escolhido
            ini = time.time()
            lista_vertices_adjacentes = self.ordena_vertices_adjacentes_pelo_grau(v)
            fim = time.time()
            print ("cria lista de vertices adj. ordenados pelo grau", fim-ini)

            for a in range(len(lista_vertices_adjacentes)):
                vertice = lista_vertices_adjacentes[a]
                for h in range(len(solucao_aux)): # se a forma um clique com os vertices dentro de solucao_aux, coloca ele junto na solucao_aux
                    vertice_solucao = solucao_aux[h]
                    if self.grafo.eh_adjacente(vertice,vertice_solucao):
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
           
        return solucao, len(solucao)

    def printa_solucao_heuristica(self, solucao, tamanho_clique):
        print('\n\n SOLUÇÃO: ')
        for i in range(len(solucao)):
            print(str(solucao[i]))    
        print("\nTAMANHO DO CLIQUE: " + str(tamanho_clique))
        


##################################################################################################

    def executa(self):
        self.le_benchmarks('benchmarks/DIMACS_benchmark_set_C125.9.txt')
        #self.le_benchmarks('benchmarks/CliqueOITO.txt')
        #self.le_benchmarks('benchmarks/Benchmark_small_test_set.txt')
        self.cria_o_grafo()
        tentativas = int(self.alpha_tentativas*len(self.vetor_de_graus))
        print("Tentativas = ", tentativas)
        ini2 = time.time()
        vetor_solucao, tamanho_clique = self.heuristica_baseada_GRASP(tentativas)
        fim2 = time.time()
        print ("tempo total", fim2-ini2)
        self.printa_solucao_heuristica(vetor_solucao, tamanho_clique)
        #self.le_benchmarks('benchmarks/DIMACS_benchmark_set_C125.9.txt' )
        # self.le_benchmarks('benchmar
        # ks/Benchmark_small_test_set.txt')
        # self.printa_matriz()
        #self.resolve_puLP()
        # self.gera_saida_GLPK()


principal = Principal()
principal.executa()
