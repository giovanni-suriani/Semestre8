from fractions import Fraction
import logging
#from settings import LOGGING, VERBOSE_VAR
import settings
import re
import str_padrao_problema as spp
from sympy import Matrix, pprint, pretty

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger("primal_dual")  # __main__
logger.debug("primal_dual.py")

VERBOSE = settings.VERBOSE

teste_gpt = spp.teste_gpt()


# Variaveis primais 
RELACAO_PRIMAL_DUAL = {"x1":"π1", "x2":"π2", "x3":"π3", "x4":"π4", "x5":"π5", "x6":"π6", "x7":"π7", "x8":"π8", "x9":"π9", "x10":"π10" }

VARIAVEIS_DUAIS = ["π1", "π2", "π3", "π4", "π5", "π6", "π7", "π8", "π9", "π10"]



def str_matrix(matrix:list):
    matrix = Matrix(matrix)
    return pretty(matrix)

def str_primal_to_dual(problem:list, standard_form:bool = False, decimal: bool = False):
    """
    Converte uma string de um problema primal para o seu dual.
    """
    # Exemplo de problema primal:
    problem = """max 2x1 + 3x2
        x1 + x2 <= 4
        3/2x1 + x2 <= 5
        x1 >= 0 """
        
    res = """min 4π1 + 5π2
            π1 + 3/2π2
    """
    problems = problem.split("\n")[0]
    tipo_funcao, _, _, variaveis = spp.extrai_f_obj(problem.split("\n")[0])
    
    print(f"problema na forma padrao: {spp.str_problem_to_standard_form(problem)}")
    A, b, c, x = spp.str_problem_to_std_form_matrix(problem)
    AT = (Matrix(A).T).tolist()
    new_x = [] 
    # Transformando em variaveis duais
    for _, variavel_dual in zip(variaveis, VARIAVEIS_DUAIS):
        new_x.append(variavel_dual)
        
    # Forcando a funcao objetivo como min
    if tipo_funcao.lower() == "max":
        tipo_funcao = "min"
    else:
        c = [-i for i in c]
    
    # Formando os simbolos de desigualdade das restricoes associadas as variaveis
    # E transformando as restricoes em irrestrito
    restricoes_simbolos = []
    for variavel
    
        
    #logger.debug(f"Matriz AT\n{str_matrix(AT)},\nVetor b\n{str_matrix(b)},\nVetor c\n{str_matrix(c)},\nVariáveis x\n{new_x}")
    print(spp.std_matrix_to_str_problem(AT, c, b, new_x, tipo_funcao))

    
    
    
    #dual_problem = std_matrix_to_str_problem(A.T, c, b.T, tipo_funcao, detailed=True)
    
str_primal_to_dual("", standard_form=True, decimal=False)
    
def primal_to_dual_matrixes(A, b, c, standard_form: bool, constraints):
    pass
    
def bateria_de_testes_primal_dual():
    pass