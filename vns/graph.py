from copy import copy
from random import choice

class Graph():
    
    def __init__(self, **args):
        graph = {}
        for aresta in args['arestas']:
            if aresta[0] not in graph.keys():
                graph[aresta[0]] = [aresta[1]]
            elif aresta[1] not in graph[aresta[0]]:
                graph[aresta[0]].append(aresta[1])  

            if aresta[1] not in graph.keys():
                graph[aresta[1]] = [aresta[0]]
            elif aresta[0] not in graph[aresta[1]]:
                graph[aresta[1]].append(aresta[0])

        self._graf = graph
        self._n_vertices = args['n_vertices']
        self._n_arestas = args['n_arestas']

    def generate_candidate_list(self, alfa, s):
        lista = []
        # se a solucao estiver vazia, todos os nos poderao participar
        if not s:
            lista = list(self._graf.keys())
        else:
            lista = self.possiveis_cliques(s)

        lista.sort(key=lambda x: -self.det_grau(x))

        return lista[:alfa]

    def search_neigh(self, s):
        best_vizinho = s
        aux = copy(s)
        for _ in range(10):
            i = choice(aux)
            aux.remove(i)
            possiveis = self.possiveis_cliques(aux)
            possiveis.remove(i)
            while possiveis:
                aux.append(choice(possiveis))
                possiveis = self.possiveis_cliques(aux)

            if len(aux) > len(best_vizinho):
                best_vizinho = aux

        return best_vizinho
                        
    def representar_solucao(self, s):
        pass

    def is_clique(self, s):        
        for no in s:
            for j in s:
                if j != no and j not in self._graf[no]:
                    return False
        return True
    
    def possiveis_cliques(self, s):
        possiveis = list(self._graf.keys())
        for no in copy(possiveis):
            for i in s:
                if i not in self._graf[no]:
                    possiveis.remove(no)
                    break
            
        return possiveis

    def det_nos(self, s):
        nos = []
        for i, j in s:
            if i not in nos:
                nos.append(i)
            if j not in nos:
                nos.append(j)
        
        return nos

    def det_grau(self, no):
        return len(self._graf[no])