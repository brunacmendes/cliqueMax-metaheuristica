from random import choice

class VNS(object):

    def __init__(self, solution):
        self._solution = solution

    def generate_random_solution(self, alpha):
        s = []
        rcl = self._solution.generate_candidate_list(alpha, s)
        while rcl:
            x = choice(rcl)
            s += [x]
            rcl = self._solution.generate_candidate_list(alpha, s)
        
        return s
        
    def local_search(self, s):
        return self._solution.search_neigh(s)
