import numpy as np
import sys
import pulp as p


class Principal:

    def __init__(self):
        self.matriz = []
        self.tamanho = 0
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

################################## CLIQUE MAXIMA EXATO ################################

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

    def executa(self):
        self.le_benchmarks('benchmarks/DIMACS_benchmark_set_C125.9.txt' )
        self.resolve_puLP()
        self.gera_saida_GLPK()


principal = Principal()
principal.executa()
