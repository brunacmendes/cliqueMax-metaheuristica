from read_dinamc_graph import ReadDinamcGraph
from vns import VNS
import time

'''
GRUPO: Bruna Mendes 0021528, Flávia 0022651, Luís Fernando 0022644
Professor: Diego
Disciplina: Meta-Heurística

'''

class Main(object):
    def run(self,file_name):
        x = 6
        leit = ReadDinamcGraph()
        solution = leit.ler(file_name)
        max_k = 2
        vns = VNS(solution)
        k = 1
        solution = None
        initial = time.time()
        while k <= max_k:
            random_solution = vns.generate_random_solution(x)
            ls_solution = vns.local_search(random_solution)
            if solution is None or len(ls_solution) > len(solution):
                solution = ls_solution
                k=1
            else:
                k += 1                                      
            print(len(solution)) 
        final = time.time()
        print(solution)
        print(len(solution))
        return (len(solution), '{0:.2f}'.format(final-initial))

