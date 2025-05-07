from fractions import Fraction
import logging
logger = logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(funcName)s:%(message)s")
logger = logging.getLogger(__name__)
import re

from str_padrao_problema import *


# Variaveis primais 
RELACAO_PRIMAL_DUAL = {"x1":"π1", "x2":"π2", "x3":"π3", "x4":"π4", "x5":"π5", "x6":"π6", "x7":"π7", "x8":"π8", "x9":"π9", "x10":"π10" }


def list_matrix_transpose(matrix:list):
    matrix =  [[-2, -1, 1, 0],
            [-1, -1, 0, 1],
            [0, 1, 0, 0]],
    transposed_matrix = []
    for i in range(len(matrix[0])):
        transposed_row = []
        for row in matrix:
            transposed_row.append(row[i])
        transposed_matrix.append(transposed_row)
    logger.debug(f"Transposed matrix: {transposed_matrix}")

def str_primal_to_dual(problem:list, standard_form:bool = False, decimal: bool = False):
    """
    Converte uma string de um problema primal para o seu dual.
    """
    # Exemplo de problema primal:
    problem = """ max 2x1 + 3x2
        x1 + x2 <= 4
        2x1 + x2 <= 5
        x1, x2 >= 0 """
    A, b, c, x = str_problem_to_std_form_matrix(problem)
    A.T = Matrix(A).T
    b.T = Matrix(b).T
    


    pass
    
list_matrix_transpose([])
    
    
    
    
def primal_to_dual_matrixes(A, b, c, standard_form: bool, constraints):
    pass
    
def bateria_de_testes_primal_dual():
    pass