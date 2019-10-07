from Aresta import *
from Vertice import *


class Grafo:

    def __init__(self):
        self.lista_Vertices = []
        self.lista_Arestas = []
        self.dicionario_adjacencia = dict()

    def novo_Vertice(self, identificador):
        # string = input(str("Identificador do Vertice: "))
        self.lista_Vertices.append(Vertice(identificador))
        self.dicionario_adjacencia[identificador] = []


    def busca_Vertice(self, identificador):  # Método recebe um int
        if self.lista_Vertices[identificador]!= None:
            return self.lista_Vertices[identificador]
        else:
            return None

    def nova_Aresta(self, origem, destino):  # Método recebe dois identificadores
        origem_aux = self.busca_Vertice(origem)
        destino_aux = self.busca_Vertice(destino)
        if (origem_aux is not None) and (destino_aux is not None):
            self.lista_Arestas.append(Aresta(origem_aux, destino_aux))
            self.dicionario_adjacencia[origem].append(destino)
            self.dicionario_adjacencia[destino].append(origem)
            #self.lista_Arestas.append(Aresta(destino_aux, origem_aux))
        else:
            print("Um do Vertice ou ambos são invalidos")

    def eh_adjacente(self, a, b):
        return a in self.dicionario_adjacencia[b]

    def busca_Adjacentes(self,u): #metodo receve Vertice
        return self.dicionario_adjacencia[u]

    

    def liberar_nos(self, lista):
        if len(lista) > 0:
            for i in range(len(lista)):
                self.lista_Vertices[lista[i]].setUsado(False)
        else:
            for i in range(len(self.lista_Vertices)):
                self.lista_Vertices[i].setUsado(False)
                
    def grau(self, u):
        return u.getGrau()

   