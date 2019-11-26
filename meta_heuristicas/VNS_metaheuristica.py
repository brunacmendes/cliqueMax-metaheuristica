import os, sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import numpy as np
import pulp as p
from estrutura_dados.Grafo import Grafo
from estrutura_dados.Instancia import Instancia
import random
import time

'''
GRUPO: Bruna Mendes 0021528, Flávia 0022651, Luís Fernando 0022644
Professor: Diego
Disciplina: Meta-Heurística

'''


class VNS: #Variable Neighbourhood Search
    def __init__(self): 
        self.clique = [] #resultado do Max_Clique
        self.instancia = Instancia()