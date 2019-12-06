class Solution(object):

    @abstractmethod
    def generate_candidate_list(self, alpha, s) -> list:
        pass
    
    @abstractmethod
    def search_neigh(self, s) -> list:
        pass

    @abstractmethod
    def representate_solution(self, s):
        pass