from graph import Graph


class ReadDinamcGraph():

    def ler(self, arquivo):

        arquivo = open(arquivo, 'r')
        n_vertices = 0
        n_arestas = 0
        arestas = []
        for linha in arquivo.readlines():
            linha = linha.split()
            if linha[0] == 'c':
                continue # atualizar depois
            elif linha[0] == 'p':
                n_vertices = int(linha[2])
                n_arestas = int(linha[3])
            elif linha[0] == 'e':
                arestas.append((int(linha[1]), int(linha[2])))
        arquivo.close()
        return Graph(n_vertices=n_vertices, n_arestas=n_arestas, arestas=arestas)
        