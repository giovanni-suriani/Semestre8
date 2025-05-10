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
logger.getChild("str_padrao_problema").setLevel(logging.INFO)

VERBOSE = settings.VERBOSE

teste_gpt = spp.teste_gpt()


# Variaveis primais 
RELACAO_PRIMAL_DUAL = {"x1":"π1", "x2":"π2", "x3":"π3", "x4":"π4", "x5":"π5", "x6":"π6", "x7":"π7", "x8":"π8", "x9":"π9", "x10":"π10" }

VARIAVEIS_DUAIS = ["π1", "π2", "π3", "π4", "π5", "π6", "π7", "π8", "π9", "π10"]


def check_non_neg_variables(restricoes:list):
    """ 
    Verifica se todas as variaveis são não-negativas.
    Args:
        restricoes (list): Lista de restrições.
    Returns:
        bool: True se todas as variaveis forem não-negativas, False caso contrário.
    """
    for restricao in restricoes:
        if not spp.check_ge_zero(restricao):
            return False
    return True
        
        

def str_primal_to_dual(problema, relacao_atual:str="primal"):
    """ 
    Converte um problema primal, transformando todas as variaveis em NÃO-NEGATIVAS, exceto irrestritas, para o seu dual.
    A função retorna o tipo da função objetivo do dual, as restrições do dual e as variáveis do dual.
    """
    funcao_objetivo = "min 2x1 + 3x2"
    restricoes = ["x1 + x2 <= 4", "3/2x1 + x2 <= 5", "x1 >= 0"]
    
    # Verifica se as variaveis são não-negativas
    if check_non_neg_variables(restricoes) == False:
        logger.debug("variaveis nao sao nao-negativas, realizando transformacao das restricoes")
        spp.change_variable_sign_in_restrictions(restricoes, True)
    
    tipo_funcao, _, _, _ = spp.extrai_f_obj(funcao_objetivo)
    todas_variaveis = spp.extrai_variaveis_problema(funcao_objetivo + "\n".join(restricoes))
    
    new_variables = []
    new_constraints = []
    if tipo_funcao.lower() == "min":
        for variable in todas_variaveis:
            logger.debug(f"variavel: {variable} vira constraint <=")
            new_constraints.append()
            
    
    
    


def str_matrix(matrix:list):
    matrix = Matrix(matrix)
    return pretty(matrix)

def str_primal_to_dual2(problem:list, standard_form:bool = False, decimal: bool = False):
    """
    Converte uma string de um problema primal para o seu dual.
    """
    # Exemplo de problema primal:
    problem = """max 2x1 + 3x2
        x1 + x2 <= 4
        3/2x1 + x2 <= 5
        x1 >= 0 """
        
    # problem = """min -2x1 - 3x2
    #     x1 + x2 <= 4
    #     3/2x1 + x2 <= 5
    #     x1 >= 0 """
        
    tipo_funcao, _, _, variaveis = spp.extrai_f_obj(problem.split("\n")[0])
    
    print(f"problema na forma padrao: {spp.str_problem_to_standard_form(problem)}")
    A, b, c, x = spp.str_problem_to_std_form_matrix(problem)
    AT = (Matrix(A).T).tolist()
    
    # Transformando em variaveis duais
    # Forcando a funcao objetivo DO DUAL como min
    if tipo_funcao.lower() == "max":
        tipo_funcao = "min"
    else:
        c = [-i for i in c]
    
    new_x = []
    for i in range(len(b)):
        new_x.append(VARIAVEIS_DUAIS[i])
    
    # Formando os simbolos de desigualdade das restricoes associadas as variaveis
    # E transformando as restricoes em irrestrito TODO
    restricoes_simbolos = []
    for restricao in AT:
        restricoes_simbolos.append("<=")
        
    str_f_obj = spp.std_matrix_to_str_problem(AT, c, b, new_x, tipo_funcao, restricoes_simbolos=restricoes_simbolos, detailed=True)
    #str_f_obj = spp.str_problem_to_standard_form(str_f_obj, detailed=True)
    
    A_dual, b_dual, c_dual, x_dual = spp.str_problem_to_std_form_matrix(str_f_obj)
    print(f"f_obj do dual = {str_f_obj}")
    print(f"matriz do dual = {spp.display_matrix_f_obj(A_dual, b_dual, c_dual, x_dual)}")

str_primal_to_dual("", standard_form=True, decimal=False)
    
def primal_to_dual_matrixes(A, b, c, standard_form: bool, constraints):
    pass
    
def bateria_de_testes_primal_dual():
    pass