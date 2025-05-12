import re
import logging
from fractions import Fraction
from pprint import pprint
import sympy as sp
from sympy import Matrix, pprint, pretty
import sys

Fraction.__str__
import settings

#logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger("primal_dual.str_padrao_problema")
if not logger.hasHandlers() and __name__ == "__main__":
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(levelname)s %(name)s %(funcName)s: %(message)s'))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
logger.debug("str_padrao_problema.py")

VERBOSE = settings.VERBOSE

VARIAVEL_ADICIONADA = 1

VARIAVEL_ALTERADA = 2
""" 
class LinhaRestricao:
        def __init__(self, restricao:str, detailed:bool = False):
            self.detailed = detailed
            constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(restricao)
            constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
            self.constantes_e_variaveis_lhs = constantes_e_variaveis_lhs
            self.simbolo = simbolo
            self.valor_rhs = valor_rhs
        
        def __str__(self):
            restricao = monta_restricao(self.constantes_e_variaveis_lhs, self.simbolo, 
                                        self.valor_rhs, detailed=self.detailed)
            return restricao[0]
        
        def __repr__(self):
            return self.__str__()
 """
def teste_gpt():
    logger.debug("teste_gpt")

def display_matrix_f_obj1(A:list, b:list, c:list, x:list):
    """
    Exibe a matriz de coeficientes A, b, c e x de forma bonita.
    Args:
        A (list): matriz de coeficientes
        b (list): vetor de constantes
        c (list): vetor de coeficientes da função objetivo
        x (list): lista de variáveis
    """
    A_matrix = Matrix(A)
    B_matrix = Matrix(b)
    C_matrix = Matrix(c)
    X_matrix = Matrix(x)

    trecho1 = f"\nMatriz A\n{pretty(A_matrix)}\n Matriz B\n{pretty(B_matrix)}\n"
    trecho2 = f"\nMatriz C\n{pretty(C_matrix)}\n Matriz X\n{pretty(X_matrix)}"
    return trecho1 + trecho2

    return(f"\nMatriz A \n" + pretty(A_matrix) + "\n Matriz B \n" + pretty(B_matrix) + "\n Matriz C \n" + pretty(C_matrix) 
                 + "\n Matriz X \n" + pretty(X_matrix))

from sympy import Matrix, pretty


from sympy import Matrix, pretty

def _side_by_side_with_labels(left: Matrix, right: Matrix, label_left: str, 
                              label_right: str, sep: str = " │ ") -> str:
    """Returns a nicely aligned multiline string with labeled left and right matrices."""
    left_lines = pretty(left).splitlines()
    right_lines = pretty(right).splitlines()

    # Compute sizes
    height = max(len(left_lines), len(right_lines))
    width_left = max(len(l) for l in left_lines)
    width_right = max(len(r) for r in right_lines)
    
    # Pad shorter matrix with blank lines
    left_lines += [" " * width_left] * (height - len(left_lines))
    right_lines += [" " * width_right] * (height - len(right_lines))

    # Prepare labels centered over their columns
    label_line = f"{label_left.center(width_left)}{sep}{label_right.center(width_right)}"

    # Combine lines
    body_lines = [f"{l.ljust(width_left)}{sep}{r}" for l, r in zip(left_lines, right_lines)]

    return "\n".join([label_line, *body_lines])

def display_matrix_f_obj(A: list, b: list, c: list, x: list) -> None:
    """
    Pretty-print the LP components:
        A │ b   (with labels)
        c │ x   (with labels)
    """
    A_m, b_m = Matrix(A), Matrix(b)
    c_m, x_m = Matrix(c), Matrix(x)

    # Force column vector display
    if c_m.shape[0] == 1:
        c_m = c_m.T
    if x_m.shape[0] == 1:
        x_m = x_m.T

    a_b_row = _side_by_side_with_labels(A_m, b_m, "[ A ]", "[ b ]")
    c_x_row = _side_by_side_with_labels(c_m, x_m, "[ c ]", "[ x ]")
    return "\n" + a_b_row + "\n\n" + c_x_row

def check_ge_zero(constantes_lhs:list, valor_rhs:list, simbolo:str = "≥") -> bool:
    """
    Checa se a restrição é maior ou igual a zero.
    Args:
        constantes_lhs (list[Fraction]): coeficientes do lado esquerdo
        valor_rhs (Fraction): valor do lado direito da restrição
        simbolo (str): símbolo de comparação
    Returns:
        bool: True se a restrição for do tipo x >= 0, False caso contrário
    """
    non_zer_vars = 0
    for constante in constantes_lhs:
        if constante != 0:
            non_zer_vars += 1
    if non_zer_vars == 1: 
        if simbolo == ">=" or simbolo == "≥":
            if valor_rhs == 0:
                return True
    return False

def check_le_zero(constants_lhs:list, value_rhs:list, symbol:str = "≤") -> bool:
    """
    Checa se a restrição é menor ou igual a zero.
    Args:
        constantes_lhs (list[Fraction]): coeficientes do lado esquerdo
        valor_rhs (Fraction): valor do lado direito da restrição
        simbolo (str): símbolo de comparação
    Returns:
        bool: True se a restrição for do tipo x <= 0, False caso contrário
    """
    non_zer_vars = 0
    for constant in constants_lhs:
        if constant != 0:
            non_zer_vars += 1
    if non_zer_vars == 1: 
        if symbol == "<=" or symbol == "≤":
            if value_rhs == 0:
                return True
    return False

def remove_ge_le_constraints(restrictions:list) -> list:
    """
    Remove as restrições do tipo x >= 0 ou x <= 0 da lista de restricoes.
    Args:
        restricoes (list): lista de restrições
    Returns:
        None
    """
    to_remove = []
    for restriction in restrictions:
        constants, variables, symbol, value_rhs = extrai_restricao(restriction)
        if check_ge_zero(constants, value_rhs, symbol) or check_le_zero(constants, value_rhs, symbol):
            to_remove.append(restriction)

    for restriction in to_remove:
        restrictions.remove(restriction)

def change_variable_sign_in_restrictions(variable:str, restrictions:list, detailed = False) -> None:
    """ 
    Troca o sinal da variável nas restrições
    Args:
        variable (str): variável a ter o sinal trocado
        restricoes (list): lista de restrições
        detailed (bool): se True, retorna a função com termos em 0
    Returns:
        None, procedimento
    """
    for i, restriction in enumerate(restrictions):
        constants, variables, symbol, value_rhs = extrai_restricao(restriction)
        constants_and_variables = dict(zip(variables, constants))
        if variable in variables:
            constants_and_variables[variable] = -constants_and_variables[variable]
            restrictions[i], _ = monta_restricao(constants_and_variables, symbol, value_rhs, detailed=detailed)
    
    return restrictions

def change_variable_sign_in_f_obj(variable:str, f_obj:str, detailed:bool=False) -> str:
    """
    Troca o sinal do termo que contém a variável especificada na função objetivo.
    Args:
        variable (str): variável a ter o sinal trocado (ex: 'x1')
        f_obj (str): função objetivo como string (ex: 'min 2x1 + x2')
        detailed (bool): se True, retorna a função com termos em 0
    Returns:
        str: função objetivo com o sinal da variável trocado
    """
    function_type, _, constants, variables = extrai_f_obj(f_obj)
    
    constants_and_variables = dict(zip(variables, constants))
    if variable in variables:
        constants_and_variables[variable] = -constants_and_variables[variable]
    else:
        raise ValueError(f"Variável '{variable}' não encontrada na função objetivo.")
    return monta_f_obj(function_type, constants_and_variables, standard_form=False, detailed=detailed)

def adicionando_variaveis_zeradas_na_expr(constantes_e_variaveis_dono:dict, constantes_e_variaveis_expr:dict) -> dict:
    """
    Adiciona variáveis zeradas no dicionário de constantes e variáveis.
    Args:
        constantes_e_variaveis (dict): dicionário de constantes e variáveis
        expressao (str): expressão a ser analisada
    Returns:
        dict: dicionário atualizado com variáveis zeradas
    """
    new_dict = {}
    for variavel, constante in constantes_e_variaveis_dono.items():
        if variavel not in constantes_e_variaveis_expr:
            new_dict[variavel] = 0
        else:
            new_dict[variavel] = constantes_e_variaveis_expr[variavel]
    return new_dict
        
def str_list_fraction(fractions:list) -> str:
    """ Transforma uma lista de frações em uma string formatada.
    Args:
        fractions (list[Fraction]): lista de frações
    Returns:
        str: string formatada com as frações
    """
    str_frac = ""
    for fraction in fractions:
        str_frac += str(fraction) + " "
    return str_frac.strip()

def extrair_constantes_e_variaveis(expr:str, extract_pure_constants:bool = False) -> tuple:
    """
    Retorna listas de constantes (como Fraction) e variáveis de uma expressão
    Args:
        expr (str): expressão a ser analisada, ex: "3x1 + 2x2 - 5x3"
        extract_pure_constants (bool): se True, extrai constantes puras ex: "3", "-5", "2/3"
    Returns:
        Tuple:
            - constantes (list[Fraction]): lista de coeficientes, constantes puras no fim
            - variaveis (list[str]): lista de variáveis
    """
    padrao = re.compile(
        r'(?P<constante_associada>[+-]?\s*(?:\d+(?:\.\d+)?|\d+/\d+)?)(?P<variavel>\w\d+)'  # aceita int, decimal, fração
        r'|' # ou
        r'(?P<constante_pura>\b[+-]?\s*(?:\d+(?:\.\d+)?|\d+/\d+)?\b)',  
        re.UNICODE
    )

    termos = re.finditer(padrao, expr)
    constantes = []
    variaveis = []
    constantes_puras = []
    for termo in termos:
        variavel = termo.group("variavel")
        coef = termo.group("constante_associada")
        constante_pura = termo.group("constante_pura")
        if variavel:
            variaveis.append(variavel)
            if coef:
                coef = coef.replace(" ", "")
                if coef in ("", "+"):
                    coef = Fraction(1)
                elif coef == "-":
                    coef = Fraction(-1)
                else:
                    # converte decimal para Fraction também
                    coef = Fraction(coef)
            else:
                coef = 1
            constantes.append(coef)
            
        else:
            if constante_pura:
                constantes_puras.append(constante_pura)
           
    if extract_pure_constants:
        constantes = constantes + constantes_puras
    """ constantes = []
    variaveis = []
    for coef_raw, var in termos:
        coef = coef_raw.replace(" ", "")
        if coef in ("", "+"):
            coef = Fraction(1)
        elif coef == "-":
            coef = Fraction(-1)
        else:
            # converte decimal para Fraction também
            coef = Fraction(coef)
        constantes.append(coef)
        variaveis.append(var) """

    return constantes, variaveis

def extrai_f_obj(f_obj:str) -> tuple:
    """
    Extrai a função objetivo no formato padrão.

    Args:
        f_obj (Any): String da função objetivo, ex: "min 3x1 + 2x2"

    Returns:
        Tuple:
            - tipo_funcao (str): "min" ou "max"
            - funcao_objetivo (str): parte da função com variáveis
            - constantes (list[Fraction]): coeficientes extraídos
            - variaveis (list[str]): nomes das variáveis
    """
    padrao = re.compile(
    r'(?i)'  # ignore maiúsculas/minúsculas
    r'(?P<tipo_funcao>max|min)\s+'  # grupo nomeado: tipo_funcao
    r'(?P<funcao>('
        r'(?:[-+]?\s*'                  # sinal opcional
        r'(?:\d+(?:\.\d+)?|\d+/\d+)?'   # constante: inteiro, decimal ou fração
        r'\s*\w\d+\s*)+'                # variável com número (ex: π1, x2)
    r'))',
    re.UNICODE
    )
    match = re.search(padrao, f_obj)
    assert match, f"Expressão inválida '{f_obj}'"
    tipo_funcao = match.group("tipo_funcao")
    funcao_objetivo = match.group("funcao")
    constantes, variaveis = extrair_constantes_e_variaveis(funcao_objetivo)

    assert tipo_funcao, f"Tipo de função inválido '{tipo_funcao}'"
    assert funcao_objetivo, f"Função objetivo inválida '{funcao_objetivo}'"
    assert constantes, f"Constantes inválidas '{constantes}'"
    assert variaveis, f"Variáveis inválidas '{variaveis}'"

    if VERBOSE:
        logger.debug(
            f"Tipo da função: {tipo_funcao}, Função objetivo: {funcao_objetivo}, Constantes: {str_list_fraction(constantes)}, Variaveis: {variaveis}"
        )
    
    return tipo_funcao, funcao_objetivo, constantes, variaveis

def extrai_restricao(restricao:str) -> tuple:
    """
    Extrai os componentes de uma restrição.
    Args:
        restricao (str): string da restrição, ex: "2x1 + π2 + 3x4 ≥ 2/3"
    Returns:
        Tuple:
            - constantes (list[Fraction]): coeficientes extraídos
            - variaveis (list[str]): nomes das variáveis
            - simbolo (str): símbolo de comparação
            - valor (Fraction): valor do lado direito da restrição
    """
    padrao = re.compile(
    r'(?P<restricao_lhs>('                     # ← início do grupo nomeado para lado esquerdo
        r'([-+]?\s*'
        r'(\d+(\.\d+)?|\d+/\d+)?'
        #r'\s*[^\W\d_]\d+\s*)+'                 # variável com número (ex: π1, x2)
        r'\s*[^\W\d_]\d+\s*)+'                 # variável com número (ex: π1, x2)
    r'))\s*'
    r'(?:'                                      # ← início da escolha entre dois caminhos (opcionalidade)
        r'(?P<simbolo_com_rhs><=|>=|<|>|=|≥|≤)'  # símbolo de comparação
        r'\s*'
        r'(?P<restricao_rhs>('
            r'[-+]?\s*(?:\d+/\d+|\d+(?:\.\d+)?)'
        r'))'
    r'|'
        r'(?P<simbolo_irrestrito>irrestrito)'   # literal "irrestrito", sem RHS
    r')\s*$',
    re.UNICODE
)
    match = re.search(padrao, restricao)
    assert match, f"Expressão inválida {restricao}"
    restricao_lhs = match.group("restricao_lhs")
    restricao_simbolo = match.group("simbolo_com_rhs") or match.group("simbolo_irrestrito")
    if restricao_simbolo == "irrestrito":
        restricao_rhs = 0
    else:
        restricao_rhs = Fraction(match.group("restricao_rhs"))
    constantes_lhs, variaveis_lhs = extrair_constantes_e_variaveis(restricao_lhs)
    #logger.debug(f"Restrição LHS: {restricao_lhs}, Simbolo: {restricao_simbolo}, Valor: {restricao_rhs}")
    if VERBOSE:
        logger.debug(f"Constantes LHS: {str_list_fraction(constantes_lhs)}, Variáveis LHS: {variaveis_lhs} \n simbolo: {restricao_simbolo}, Valor: {restricao_rhs}")
    return constantes_lhs, variaveis_lhs, restricao_simbolo, restricao_rhs

def standard_display_variable(constante, variavel, first_var:bool, show_zero:bool = False, decimal:bool = False) -> str:
    if show_zero and first_var and constante == 0:
        return f"0{variavel}"
    
    if show_zero and first_var is False and show_zero and constante == 0:
        return f"+ 0{variavel}"

    if show_zero is False and constante == 0:
        return ""
            

    if not decimal:
        if first_var:
            if constante == 1:
                return f"{variavel}"
            elif constante == -1:
                return f"-{variavel}"
            else:
                return f"{constante}{variavel}"
        else:
            if constante == 1:
                return f"+ {variavel}"
            elif constante == -1:
                return f"- {variavel}"
            if constante > 0:
                return f"+ {constante}{variavel}"
            if constante < 0:
                return f"- {abs(constante)}{variavel}"
        
    else:
        if first_var:
            if constante == 1:
                return f"{variavel}"
            elif constante == -1:
                return f"-{variavel}"
            else:
                return f"{str(float(constante))}{variavel}"
        else:
            if constante > 0:
                return f"+ {str(float(constante))}{variavel}"
            elif constante == -1:
                return f"- {variavel}"
            if constante < 0:
                return f"- {abs(str(float(constante)))}{variavel}"
        
    raise ValueError(f"Erro inesperado")

def monta_f_obj(tipo_funcao:str, constantes_e_variaveis:dict, standard_form:bool = False, 
                detailed:bool = False, decimal:bool = False) -> str:
    """
    Monta a função objetivo a partir dos componentes extraídos.
    Args:
        tipo_funcao (str): "max" ou "min"
        constantes (dict): coeficientes extraídos
        standard_form (bool): se True, retorna a função na forma padrão (MIN)
        detailed (bool): se True, retorna a função com termos em 0
        decimal (bool): se True transforma os números em decimal
    Returns:
        str: função objetivo montada
    """
    if standard_form:
        if tipo_funcao.lower() == "max":
            for variavel, constante in constantes_e_variaveis.items():
                constantes_e_variaveis[variavel] = -constante
            tipo_funcao = "MIN"
                
    funcao_objetivo = f"{tipo_funcao} "
    for i, (variavel, constante) in enumerate(constantes_e_variaveis.items()):
        primeira = (i == 0)
        if primeira:
            funcao_objetivo += standard_display_variable(constante, variavel, primeira, detailed, decimal)
        else:
            funcao_objetivo += " " + standard_display_variable(constante, variavel, primeira, detailed, decimal)
                    
        
    logger.debug(f"Função objetivo montada: {funcao_objetivo}")
    return funcao_objetivo.strip()

def monta_restricao(constantes_e_variaveis_lhs:dict, simbolo:str, valor_rhs:Fraction, standard_form:tuple = (False, "s1"),
                    detailed:bool = False, decimal:bool = False) -> tuple:
    """
    Monta a restrição a partir dos componentes extraídos.
    Args:
        constantes_e_variaveis_lhs (dict): coeficientes extraídos do lado esquerdo
        simbolo (str): símbolo de comparação
        valor_rhs (Fraction): valor do lado direito da restrição
        standard_form (tuple): se True, retorna a restricoes de variavel 
                                e outras na forma padrão (x1>=0, x2 + s1 = 2)
        detailed (bool): se True, retorna a função com termos em 0
        decimal (bool): se True transforma os números em decimal
    Returns:
        tuple:
            str: restrição montada,
            int: nada acontece = 0, 
                variavel adicionada = 1, 
                variavel alterada = 2, 
                duas variaveis adicionadas = 3 (variaveis irrestritas)  
    """
    # Checando se é restrição x1 >= 0 ou irrestrita
    non_zero_var = 0
    constantes_lhs = list(constantes_e_variaveis_lhs.values())
    
    constant_foo = 0
    for variavel, constante in constantes_e_variaveis_lhs.items():
        if constante != 0:
            non_zero_var += 1
            constant_foo = constante
            variable_foo = variavel
            
    change_var = 0
    
    if simbolo == "irrestrito":
        if standard_form[0] is False:
            if VERBOSE:
                logger.debug(f"{standard_display_variable(abs(constant_foo), variable_foo, True)} irrestrito")
            return f"{standard_display_variable(abs(constant_foo), variable_foo, True)} irrestrito", 0
        if standard_form[0] is True:
            logger.warning(f"CUIDADO, condição de variavel puramente irrestrita NAO implementada")
            return f"{standard_display_variable(abs(constant_foo), variable_foo, True)} irrestrito", 0
            
    # Checando se é restrição x1 >= 0 ou <= 0
    if standard_form[0] is True:
        if non_zero_var == 1:
            if (simbolo == ">=" or simbolo == "≥") and valor_rhs == 0 :
                if constant_foo < 0:
                    change_var = 2
                    lhs = standard_display_variable(abs(constant_foo), variable_foo, first_var=True, decimal=decimal)
                    if VERBOSE:
                        logger.debug(f"{lhs} {simbolo} {valor_rhs} {change_var}")
                    return f"{lhs} {simbolo} {valor_rhs}", change_var
                else:
                    lhs = standard_display_variable(constant_foo, variable_foo, first_var=True, decimal=decimal)
                    if VERBOSE:
                        logger.debug(f"{lhs} {simbolo} {valor_rhs} {change_var}")
                    return f"{lhs} {simbolo} {valor_rhs}", change_var
            elif (simbolo == "<=" or simbolo == "≤") and valor_rhs == 0:
                if constant_foo > 0:
                    change_var = 2
                    lhs = standard_display_variable(constant_foo, variable_foo, first_var=True, decimal=decimal)
                    if VERBOSE:
                        logger.debug(f"{lhs} >= {valor_rhs} {change_var}")
                    return f"{lhs} >= {valor_rhs}", change_var
                else:
                    lhs = standard_display_variable(abs(constant_foo), variable_foo, first_var=True, decimal=decimal)
                    logger.debug(f"{lhs} >= {valor_rhs} {change_var}")
                    return f"{lhs} >= {valor_rhs}", change_var
    
    if standard_form[0] is True:
        # Deixando na forma de menor igual
        if simbolo == ">=" or simbolo == "≥":
            simbolo = "<="
            valor_rhs = -valor_rhs
            for variavel, constante in constantes_e_variaveis_lhs.items():
                constantes_e_variaveis_lhs[variavel] = -constante
        if simbolo != "=":
            constantes_e_variaveis_lhs[standard_form[1]] = 1
            simbolo = "="
            change_var = 1
            
        # adicionando variáveis de folga
        
    lhs = ""
    # Primeiro, apenas desigualdades de <=
    for i, (variavel, constante) in enumerate(constantes_e_variaveis_lhs.items()):
        if lhs == "":
            primeira = True
        else:
            primeira = False
        
        if primeira:
            lhs += standard_display_variable(constante, variavel, primeira, show_zero=detailed, decimal=decimal)
        else:
            variavel = standard_display_variable(constante, variavel, primeira, show_zero=detailed, decimal=decimal)
            if variavel != "":
                lhs += " " + variavel
    if VERBOSE:
        logger.debug(f"{lhs.strip()} {simbolo} {valor_rhs} {change_var}")
    return f"{lhs.strip()} {simbolo} {valor_rhs}", change_var
            
    # Segundo, variávies de folga
    
def extrai_variaveis_problema(problema:str) -> list:
    all_variables = []
    tipo_funcao, funcao_objetivo, constantes, variaveis = extrai_f_obj(problema.split("\n")[0])
    for restricao in problema.split("\n")[1:]:
        constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(restricao)
        for variavel in variaveis_lhs:
            if variavel not in all_variables:
                all_variables.append(variavel)
    return all_variables
  
def extract_ge_le_constraints(constraints:list, positive_lhs:bool = False) -> list:
    """
    Extrai as restrições do tipo x >= 0 ou x <= 0 de uma lista de restricoes.
    Args:
        constraints (list): lista de restrições
        positive_lhs (bool): se True, formas -x1 >= 0 se tornam x1 <= 0
    Returns:
        list: lista de restrições do tipo x >= 0 ou x <= 0
    """
    ge_le_constraints = []
    for constraint in constraints:
        constants_lhs, variables_lhs, symbol, value_rhs = extrai_restricao(constraint)
        if check_ge_zero(constants_lhs, value_rhs, symbol) or check_le_zero(constants_lhs, value_rhs, symbol):
            if positive_lhs:
                # Flipping the sign of the constant and symbol
                for constant in constants_lhs:
                    if constant < 0:
                        if symbol == ">=" or symbol == "≥":
                            symbol = "<="
                        elif symbol == "<=" or symbol == "≤":
                            symbol = ">="
                        break
                constraint = assemble_variables_constraints(variables_lhs, symbols=[symbol])[0]
            ge_le_constraints.append(constraint)
    return ge_le_constraints
  
def extract_constraints_signs(restricoes:list) -> list:
    """
    Extrai os sinais das restrições de uma lista de restricoes.
    Args:
        restricoes (list): lista de restrições
    Returns:
        list: lista de sinais das restrições
    """
    restrictions_signs = []
    for restricao in restricoes:
        _, _, symbol, _ = extrai_restricao(restricao)
        restrictions_signs.append(symbol)
    return restrictions_signs
    
def assemble_variables_constraints(variables:list, symbols:list = [], 
                                   is_vars_on_standard_form:bool=False) -> list:
    """
    Monta restricoes do tipo "x1 >= 0", "x2 <= 0", "x3 irrestrito" "x4 = 0" a partir de variáveis e sinais.
    Args:
        variables (list): lista de variáveis
        restrictions_symbols (list): lista de sinais das restrições
        is_vars_on_standard_form (bool): se True, as variáveis estão na forma padrão( >=0 )
    Returns:
        list: lista de restricoes do tipo "x1 >= 0", "x2 <= 0", "x3 irrestrito" "x4 = 0"
    """
    variables_constraints = []
    if not is_vars_on_standard_form:
        for variable, symbol in zip(variables, symbols):
            if symbol == "irrestrito":
                variables_constraints.append(f"{standard_display_variable(1, variable, first_var=True)} {symbol}")
            else:
                variables_constraints.append(f"{standard_display_variable(1, variable, first_var=True)} {symbol} 0")
    else:
        for variable in variables:
            variables_constraints.append(f"{standard_display_variable(1, variable, first_var=True)} >= 0")
    return variables_constraints
    
def str_problem_to_standard_form(problem, detailed:bool = False, decimal:bool = False) -> str:
    """ 
    Transforma um problema de programação linear em sua forma padrão.
    Args:
        problem (str): problema a ser transformado
        detailed (bool): se True, retorna a função com termos em 0
        decimal (bool): se True, retorna a função com termos em 0
    Returns:
        str: problema transformado para forma padrão
    """
    problem = problem.split("\n")
    f_obj = problem[0]
    restricoes = problem[1:]
    
    # Transforma as restricoes primeiro
    # tipo_funcao, funcao_objetivo, constantes, variaveis = extrai_f_obj(problem[0])
    # constantes_e_variaveis = dict(zip(variaveis, constantes))
    tipo_funcao, funcao_objetivo, constantes, variaveis = extrai_f_obj(f_obj)
    constantes_e_variaveis_fobj = dict(zip(variaveis, constantes))
    slack_var = 1
    new_restricoes = []
    
    for restricao in restricoes:
        constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(restricao)
        constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
        forma_padrao_restricao, change_var = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(True, "s" + str(slack_var)),
                                                             detailed=detailed, decimal=decimal)
        if change_var == VARIAVEL_ADICIONADA:
            # Adicionando variaveis de folga na f_obj
            constantes_e_variaveis_fobj["s" + str(slack_var)] = 0
            slack_var += 1
        
        elif change_var == VARIAVEL_ALTERADA:
            for variavel, constante in constantes_e_variaveis_lhs.items():
                if constante != 0:
                # Trocando o sinal da variavel na funcao objetivo
                    constantes_e_variaveis_fobj[variavel] = -constantes_e_variaveis_fobj[variavel]
                # Trocando sinal da variavel nas equacoes
                    change_variable_sign_in_restrictions(variavel, new_restricoes)
                    
        new_restricoes.append(forma_padrao_restricao)
        
        if VERBOSE:
            logger.debug(f"forma_padrao_restricao {restricao.lstrip()} SE TRANSFORMA EIN {forma_padrao_restricao}")
    #monta_f_obj(tipo_funcao, constantes_e_variaveis, standard_form=True, detailed=detailed, decimal=decimal)
    # Adicionando 0's nas variaveis que nao aparecem nas restricoes, mas estao na funcao objetivo
    if detailed:
        restricoes = new_restricoes
        new_restricoes = []
        for restricao in restricoes:
            constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(str(restricao))
            constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
            constantes_e_variaveis_lhs = adicionando_variaveis_zeradas_na_expr(constantes_e_variaveis_fobj, constantes_e_variaveis_lhs)
            forma_padrao_restricao_detailed, _ = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(True, "s" + str(slack_var)),
                                                                 detailed=detailed, decimal=decimal) 
            new_restricoes.append(forma_padrao_restricao_detailed)
            if VERBOSE:
                logger.debug(f"forma_padrao_restricao_detailed {restricao.lstrip()} SE TRANSFORMA EIN {forma_padrao_restricao_detailed}")
    f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis_fobj, standard_form=True, detailed=detailed, decimal=decimal)
    std_problem = f_obj + "\n"
    for restricao in new_restricoes:
        std_problem += str(restricao) + "\n"
    std_problem = std_problem.strip()
    logger.debug(f"Função objetivo antiga: \n{problem}")
    logger.debug(f"\nFunção objetivo padrão: \n{std_problem}")
    return std_problem
        
def str_problem_to_std_form_matrix (problem, decimal:bool = False) -> tuple: 
    """ 
        Função para transformar um problema de programação linear em sua forma padrão, retornado em matriz.
        Args:
            problem (str): problema a ser transformado
            decimal (bool): se True, retorna a função com termos em 0
        Returns:
            Tuple:
                - A (list): matriz de coeficientes
                - b (list): vetor de constantes
                - c (list): vetor de coeficientes da função objetivo
                - x (list): lista de variáveis
    """
    std_problem = str_problem_to_standard_form(problem, detailed=True, decimal=decimal)
    std_problem = std_problem.split("\n")
    tipo_funcao, funcao_objetivo, constantes, variaveis = extrai_f_obj(std_problem[0])
    # Matriz de coeficientes c
    c = constantes
    restricoes = std_problem[1:]
    # Matriz de coeficientes A
    A = []
    b = []
    for restricao in restricoes:
        constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(restricao)
        non_zero_var = 0
        if check_ge_zero(constantes_lhs, valor_rhs, simbolo):
            continue
        A.append(constantes_lhs)
        b.append(valor_rhs)
    # Mostra bonitinho no console
    # Mostra bonitinho no log (como string)
    logger.debug(f"Problema em matriz {display_matrix_f_obj(A, b, c, variaveis)}")
    return A, b, c, variaveis
        
def std_matrix_to_str_problem(A:list, b:list, c:list, x:list, tipo_funcao:str = "min", 
                              standard_form = False, restricoes_simbolos:list = None, 
                              decimal:bool = False, detailed:bool = False) -> str:
    """
    Converte uma matriz de programação linear de A,b,c e x para string.
    Espera-se todas as variáveis no vetor x, exceto se for exigido forma padrao
    Args:
        A (list): matriz de coeficientes
        b (list): vetor de constantes
        c (list): vetor de coeficientes da função objetivo
        x (list): lista de variáveis
        tipo_funcao (str): "max" ou "min"
        tipo_variaveis (list): lista o tipo 
        decimal (bool): se True, retorna a função com termos em 0
    Returns:
        str: problema transformado para forma padrão
    """
    #assert tipo_funcao.lower() == "min", "Tipo de função inválido, deve ser 'min'"
    assert A, "Matriz A está vazia"
    assert b, "Vetor b está vazio"
    assert c, "Vetor c está vazio"
    
    forma_padrao = standard_form
    if forma_padrao:
        if tipo_funcao.lower() == "max":
            tipo_funcao = "min"
            c = [-i for i in c]
    
    constantes_e_variaveis_f_obj = dict(zip(x, c))
    f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis_f_obj, standard_form=forma_padrao, detailed=detailed, decimal=decimal)
    
    # Monta as restrições
    restricoes = []
    slack_var = 1
    for i in range(len(A)):
        constantes_lhs = A[i]
        variaveis_lhs = x
        
        if restricoes_simbolos:
            simbolo = restricoes_simbolos[i]
        
        else:
            simbolo = "="
        
        valor_rhs = b[i]
        constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
        forma_padrao_restricao, change_var = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(forma_padrao, "s"+str(slack_var)),
                                                     detailed=detailed, decimal=decimal)
        
        if change_var == VARIAVEL_ADICIONADA:
            constantes_e_variaveis_f_obj["s" + str(slack_var)] = 0
            slack_var += 1
            # Adicionando variaveis de folga
        
        if change_var == VARIAVEL_ALTERADA:
            for variavel, constante in constantes_e_variaveis_lhs.items():
                if constante != 0:
                    # Trocando o sinal da variavel na funcao objetivo
                    constantes_e_variaveis_f_obj[variavel] = -constantes_e_variaveis_f_obj[variavel]
                    # Trocando sinal de todas variaveis lhs
                    change_variable_sign_in_restrictions(variavel, restricoes)
        
        restricoes.append(forma_padrao_restricao)
    
    # Monta o problema final
    if detailed:
        f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis_f_obj, standard_form=True, detailed=detailed, decimal=decimal)
        std_problem = f_obj + "\n"
        for restricao in restricoes:
            constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(str(restricao))
            constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
            constantes_e_variaveis_lhs = adicionando_variaveis_zeradas_na_expr(constantes_e_variaveis_f_obj, constantes_e_variaveis_lhs)
            forma_padrao_restricao_detailed, _ = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(standard_form, "s1"),
                                                                 detailed=detailed, decimal=decimal) 
            
            std_problem += forma_padrao_restricao_detailed + "\n"
    
    else:
        std_problem = f_obj + "\n"
        for restricao in restricoes:
            std_problem += str(restricao) + "\n"
    """ std_problem = f_obj + "\n"
    for restricao in restricoes:
        std_problem += str(restricao) + "\n" """
    
    logger.debug(f"Função objetivo antiga: {display_matrix_f_obj(A, b, c, x)}")
    logger.debug(f"Função objetivo de matriz para padrão: \n{std_problem.strip()}")
    return std_problem.strip()
        
def bateria_testes_utilitarios(test_check_ge_zero:bool=False,
                                test_check_le_zero:bool=False,
                                test_remove_ge_le_constraints:bool=False,
                                test_change_variable_sign_in_f_obj:bool=False,
                                test_change_variable_sign_in_restrictions:bool=False,
                                test_adicionando_variaveis_zeradas_na_expr:bool=False,
                                test_extrai_variaveis_problema:bool=False,
                                test_extract_ge_le_constraints:bool=False,
                               ):
    # Testes para check_ge_zero
    if test_check_ge_zero:
        t1 = {"constraint":"2x1 + π2 + 3x4 ≥ 2/3", "result":False}
        t2 = {"constraint":"π1 + 2x2 ≤ 5.2", "result":False}
        t3 = {"constraint":"-x1 + p2 + s3 = -2", "result":False}
        t4 = {"constraint":"x1 irrestrito", "result":False}
        t5 = {"constraint":"x1 + x2 + x3 >= 0", "result":False}
        t6 = {"constraint":"x1 <= 0", "result":False}
        t7 = {"constraint":"x1 >= 0", "result":True}
        t8 = {"constraint":"0x1 >= 0", "result":False}
        t9 = {"constraint":"0x1 + x2 >= 0", "result":True}
        t10 = {"constraint":"-x1 >= 0", "result":True}
        t11 = {"constraint":"24x1 >= 0", "result":True}
        tests = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]
        if VERBOSE:
            logger.info(f"Iniciando testes para check_ge_zero")
        
        for test in tests:
            constraint = test["constraint"]
            result = test["result"]
            constants, _, symbol, value_rhs = extrai_restricao(constraint)
            logger.debug(f"teste: {test}")
            assert check_ge_zero(constantes_lhs=constants, valor_rhs=value_rhs, simbolo=symbol) == result, f"Erro: {constraint} != {result}, teste: {test}"
    
    # Testes para check_le_zero
    if test_check_le_zero:
        t1 = {"constraint":"2x1 + π2 + 3x4 ≤ 2/3", "result":False}
        t2 = {"constraint":"π1 + 2x2 ≥ 5.2", "result":False}
        t3 = {"constraint":"-x1 + p2 + s3 = -2", "result":False}
        t4 = {"constraint":"x1 irrestrito", "result":False}
        t5 = {"constraint":"x1 + x2 + x3 <= 0", "result":False}
        t6 = {"constraint":"x1 >= 0", "result":False}
        t7 = {"constraint":"x1 <= 0", "result":True}
        t8 = {"constraint":"0x1 <= 0", "result":False}
        t9 = {"constraint":"0x1 + x2 <= 0", "result":True}
        t10 = {"constraint":"-x1 <= 0", "result":True}
        t11 = {"constraint":"24x1 <= 0", "result":True}
        tests = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]
       
        if VERBOSE:
            logger.info(f"Iniciando testes para check_le_zero")
        
        for test in tests:
            constraint = test["constraint"]
            result = test["result"]
            constants, _, symbol, value_rhs = extrai_restricao(constraint)
            assert check_le_zero(constants_lhs=constants, value_rhs=value_rhs, symbol=symbol) == result, f"Erro: {constraint} != {result}"
        
    # Testes para remove_ge_le_constraints
    if test_remove_ge_le_constraints:
        t1 = "2x1 + π2 + 3x4 ≥ 2/3"
        t2 = "π1 + 2x2 ≤ 5.2"
        t3 = "-x1 + p2 + s3 = -2"
        t4 = "x1 irrestrito"
        t5 = "x1 + x2 + x3 >= 0"
        t6 = "x1 <= 0"
        t7 = "x1 >= 0"
        constraints = [t1, t2, t3, t4, t5, t6, t7]
        if VERBOSE:
            logger.info(f"Iniciando testes para remove_ge_le_constraints")
        remove_ge_le_constraints(constraints)
        for constraint in constraints:
            constants, _, symbol, value_rhs = extrai_restricao(constraint)
            if check_ge_zero(constants, value_rhs, symbol) or check_le_zero(constants, value_rhs, symbol):
                raise AssertionError(f"Erro: {constraint} não foi removida")
        
    # Testes para change_variable_sign_in_f_obj
    if test_change_variable_sign_in_f_obj:
        t1 = {"f_obj":"max 2x1 + π2 + 3x4", "variable":"x1", "result":"max -2x1 + π2 + 3x4"}
        t2 = {"f_obj":"max 2x1 + π2 + 3x4", "variable":"π2", "result":"max 2x1 - π2 + 3x4"}
        t3 = {"f_obj":"max 2x1 + π2 + 3x4", "variable":"x4", "result":"max 2x1 + π2 - 3x4"}
        t4 = {"f_obj":"MAX -π1 + 2x2", "variable":"π1", "result":"MAX π1 + 2x2"}
        t5 = {"f_obj":"MIN -π1 + 0x2", "variable":"x2", "result":"MIN -π1 + 0x2"}
        tests = [t1, t2, t3, t4, t5]
        if VERBOSE:
            logger.info(f"Iniciando testes para change_variable_sign_in_f_obj")
        for test in tests:
            f_obj = test["f_obj"]
            variable = test["variable"]
            result = test["result"]
            new_f = change_variable_sign_in_f_obj(variable, f_obj, detailed=True)
            assert new_f == result, f"Erro: {new_f} != {result}, teste: {test}"
            
    # Testes para change_variable_sign_in_restrictions
    if test_change_variable_sign_in_restrictions:
        t1 = {"restrictions":["2x1 + π2 + 3x4 ≥ 2/3", 
                              "x1 >= 24", 
                              "-5x1 + π2 + 23x4 ≥ 2/3"],
                "variable":"x1", 
                "result":["-2x1 + π2 + 3x4 ≥ 2/3", 
                          "-x1 >= 24", 
                          "5x1 + π2 + 23x4 ≥ 2/3"]}
        tests = [t1]
        if VERBOSE:
            logger.info(f"Iniciando testes para change_variable_sign_in_restrictions")
        for test in tests:
            restrictions = test["restrictions"]
            variable = test["variable"]
            result = test["result"]
            change_variable_sign_in_restrictions(variable, restrictions)
            for i in range(len(restrictions)):
                assert restrictions[i] == result[i], f"Erro: {restrictions[i]} != {result[i]} teste: {test}"
    
    # Testes para adicionando_variaveis_zeradas_na_expr
    if test_adicionando_variaveis_zeradas_na_expr:
        # Implementar
        pass
    
    # Testes para extrai_variaveis_problema
    if test_extrai_variaveis_problema:
        # Implementar
        pass
        
    # Testes para extrair_ge_le_constraints
    if test_extract_ge_le_constraints:
        t1 = {"constraints":[
            "2x1 + π2 + 3x4 ≥ 2/3",
            "π1 + 2x2 ≤ 5.2",
            "x3 <= 0",
            "x1 + x2 + x3 >= 0",
            "-x1 <= 0",
            "p2 >= 0"
            ],
            "positive_lhs":False,
            "result":[
                "x3 <= 0",
                "-x1 <= 0",
                "p2 >= 0"
            ]
              }
        t2 = {"constraints":[
            "2x1 + π2 + 3x4 ≥ 2/3",
            "π1 + 2x2 ≤ 5.2",
            "-p2 >= 0",
            "x1 + x2 + x3 >= 0",
            "-x3 >= 0",
            "-x1 <= 0"
            ],
            "positive_lhs":True,
            "result":[
                "p2 <= 0",
                "x3 <= 0",
                "x1 >= 0"
            ]
              }
        tests = [t2]
        
        if VERBOSE:
            logger.info(f"Iniciando testes para extrair_ge_le_constraints")
        for test in tests:
            constraints = test["constraints"]
            positive_lhs = test["positive_lhs"]
            result = test["result"]
            ge_le_constraints = extract_ge_le_constraints(constraints, positive_lhs=positive_lhs)
            for i in range(len(ge_le_constraints)):
                try:
                    assert ge_le_constraints[i] == result[i]
                except AssertionError:
                    logger.error(f"Erro: {ge_le_constraints[i]} != {result[i]}, teste: {test}")
                    logger.error(f"\nvalor calculado:{ge_le_constraints}\nvalor  esperado:{result}")
                    raise
        
        
        
def bateria_testes_str_padrao_problema(test_extrai_f_obj:bool = False, 
                   test_extrai_restricao:bool = False,
                   test_monta_f_obj:bool = False, 
                   test_monta_restricao:bool = False, 
                   test_extrai_variaveis_problema:bool = False, 
                   test_forma_padrao:bool = False, 
                   test_problema_padrao_matriz:bool = False, 
                   test_matriz_para_problema_padrao:bool = False,
                   test_extract_constraints_signs:bool = False,
                   test_assemble_variables_constraints:bool = False,
                   ):
    # Testes para extrair_f_obj
    if test_extrai_f_obj:
        logger.info(f"Iniciando testes para extrair_f_obj")
        teste1 = "max 3/2π1 + 2y2"
        teste2 = "MIN 3/2Φ1 + 2Φ2 + 3Φ3"
        teste3 = "MIN 1.5x1"
        teste4 = "MIN -1.5x1 + 0x2 + 0x3"
        teste5 = "MAX - 1.5x1 + 0x2 + 0x3"
        teste6 = "max -3/2x1 - 2x2 + 0x3"
        
        assert extrai_f_obj(teste1) == ("max", "3/2π1 + 2y2", [Fraction(3, 2), Fraction(2)], ["π1", "y2"])
        assert extrai_f_obj(teste2) == ("MIN", "3/2Φ1 + 2Φ2 + 3Φ3", [Fraction(3, 2), Fraction(2), Fraction(3)], ["Φ1", "Φ2", "Φ3"])
        assert extrai_f_obj(teste3) == ("MIN", "1.5x1", [Fraction(3, 2)], ["x1"])
        assert extrai_f_obj(teste4) == ("MIN", "-1.5x1 + 0x2 + 0x3", [Fraction(-3, 2), Fraction(0, 1), Fraction(0, 1)], ["x1", "x2", "x3"])
        assert extrai_f_obj(teste5) == ("MAX", "- 1.5x1 + 0x2 + 0x3", [Fraction(-3, 2), Fraction(0, 1), Fraction(0, 1)], ["x1", "x2", "x3"])
        assert extrai_f_obj(teste6) == ("max", "-3/2x1 - 2x2 + 0x3", [Fraction(-3, 2), Fraction(-2), Fraction(0, 1)], ["x1", "x2", "x3"])
    
    # Testes para extrair_restricao
    if test_extrai_restricao:
        logger.info(f"Iniciando testes para extrair_restricao")
        t1 = "2x1 + π2 + 3x4 ≥ 2/3"
        t2 = "π1 + 2x2 ≤ 5.2"
        t3 = "-x1 + p2 + s3 = -2"
        t4 = "x1 irrestrito"
        
        assert extrai_restricao(t1) == ([Fraction(2, 1), Fraction(1, 1), Fraction(3, 1)], ["x1", "π2", "x4"], "≥", 
                                        Fraction(2, 3))
        assert extrai_restricao(t2) == ([Fraction(1, 1), Fraction(2, 1)], ["π1", "x2"], "≤", Fraction(26, 5))
        assert extrai_restricao(t3) == ([Fraction(-1, 1), Fraction(1, 1), Fraction(1, 1)], ["x1", "p2", "s3"], "=", Fraction(-2, 1))
        assert extrai_restricao(t4) == ([1],["x1"], "irrestrito", 0)
    
    # Testes para monta_f_obj
    if test_monta_f_obj:
        logger.info("Iniciando testes para monta_f_obj")
        t1 = ("max 3/2π1 + 2y2", True, False, "max 3/2π1 + 2y2")
        t2 = ("min -3/2x1 + 2x2 + 0x3", True, False, "min -3/2x1 + 2x2 + 0x3")
        t3 = ("min -3/2x1 + 2x2 + 0x3", False, False, "min -3/2x1 + 2x2")
        t4 = ("max -4.1x1", True, True, "max -4.1x1")
        testes = [t1, t2, t3, t4]
        for teste in testes:
            tipo_funcao, funcao_objetivo, constantes, variaveis = extrai_f_obj(teste[0])
            constantes_e_variaveis = dict(zip(variaveis, constantes))
            try:
                str_f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis, detailed=teste[1], decimal=teste[2])
                assert str_f_obj == teste[3]
            except AssertionError as e:
                logger.error(f"Erro no teste: {teste[0]}, valor calculado: {str_f_obj}, valor esperado: {teste[3]}")
                raise e
        
        t1 = ("max 3/2π1 + 2y2", False, "MIN -3/2π1 - 2y2")
        t2 = ("min -3/2x1 + 2x2 + 0x3", False, "min -3/2x1 + 2x2 + 0x3")
        t3 = ("max -4.1x1", True, "MIN 4.1x1")
        t4 = ("max 0x1 + 0x2", True, "MIN 0x1 + 0x2")
        testes = [t1, t2, t3, t4]
        for teste in testes:
            tipo_funcao, funcao_objetivo, constantes, variaveis = extrai_f_obj(teste[0])
            constantes_e_variaveis = dict(zip(variaveis, constantes))
            try:
                str_f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis, standard_form=True, detailed=True, decimal=teste[1])
                assert str_f_obj == teste[2]
            except AssertionError as e:
                logger.error(f"Erro no teste: {teste[0]}, valor calculado: {str_f_obj}, valor esperado: {teste[2]}")
                raise e
    
    # Testes para extrai_variaveis_problema
    if test_extrai_variaveis_problema:
        logger.info("Iniciando testes para extrai_variaveis_problema")
        problema1 = """min x1 + 2x2
                2x1 + x2 ≥ 2/3
                x1 + x2 ≥ 1
                x2 = 2
                x1 >= 0
                x2 <= 0"""
                
        problema2 = """max π1 + 2π2
                2π1 + π2 ≥ 4
                7π1 + π2 <= 1
                -π2 = 2
                π1 <= 0 
                π2 >= 0"""
                
        problema3 = """max π1 + 2π2
                2π1 + π2 ≥ 4
                7π1 + π2 <= 1
                -π2 = 2
                π1 <= 0
                π2 irrestrito"""
        assert extrai_variaveis_problema(problema1) == ["x1", "x2"]
        assert extrai_variaveis_problema(problema2) == ["π1", "π2"]
        assert extrai_variaveis_problema(problema3) == ["π1", "π2"]
    
    # Testes para monta_restricao
    if test_monta_restricao:
        logger.info("Iniciando testes para monta_restricao")
        t1 = ("2x1 + π2 + 3x4 ≥ 2/3", (False, "s1"), {"detailed": True, "decimal": False}, ("2x1 + π2 + 3x4 ≥ 2/3", 0))
        t2 = ("2x1 + π2 + 3x4 ≥ 2/3", (True, "s1"), {"detailed": True, "decimal": False}, ("-2x1 - π2 - 3x4 + s1 = -2/3", 1))
        t3 = ("2x1 + π2 + 3x4 <= 2/3", (True, "s1"), {"detailed": True, "decimal": False}, ("2x1 + π2 + 3x4 + s1 = 2/3", 1))
        t4 = ("x1 >= 0", (False, "s1"), {"detailed": False, "decimal": False}, ("x1 >= 0", 0))    
        t5 = ("x1 <= 0", (False, "s1"), {"detailed": False, "decimal": False}, ("x1 <= 0", 0))
        t6 = ("x1 <= 0", (True, "s1"), {"detailed": False, "decimal": False}, ("x1 >= 0", 2))
        t7 = ("x1 irrestrito", (False, "s1"), {"detailed": False, "decimal": False}, ("x1 irrestrito", 0))
        t8 = ("π2 irrestrito", (False, "s1"), {"detailed": False, "decimal": False}, ("π2 irrestrito", 0))
        testes = [t1, t2, t3, t4, t5, t6, t7, t8]
        
        for teste in testes:
            #teste = t5
            constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(teste[0])
            constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
            try:
                valor = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=teste[1], 
                                                            detailed=teste[2]["detailed"], decimal=teste[2]["decimal"])
                assert valor == teste[3]
            except AssertionError as e:
                logger.error(f"Erro no teste: {teste[0]}, valor calculado: {valor}, valor esperado: {teste[3]}")
                raise e
        
    # Testes para str_problem_to_standard_form
    if test_forma_padrao:
        logger.info("Iniciando testes para str_problem_to_standard_form")
        # Teste 1
        problem1 = ("""min x1 + 2x2
                2x1 + x2 ≥ 2/3
                x1 + x2 ≥ 1
                x2 = 2
                x1 >= 0
                x2 <= 0""", {"detailed": False, "decimal": False})
                
        problem_ans1 = """min x1 - 2x2 
                -2x1 + x2 + s1 = -2/3
                -x1 + x2 + s2 = -1
                -x2 = 2
                x1 >= 0
                x2 >= 0"""
                
        problem2 = ("""max π1 + 2π2
                2π1 + π2 ≥ 4
                7π1 + π2 <= 1
                -π2 = 2
                π1 <= 0 
                π2 >= 0""", {"detailed": True, "decimal": False})
        
        problem_ans2 = """MIN π1 - 2π2 + 0s1 + 0s2
                2π1 - π2 + s1 + 0s2 = -4
                -7π1 + π2 + 0s1 + s2 = 1
                0π1 - π2 + 0s1 + 0s2 = 2
                π1 >= 0
                π2 >= 0"""
        
        # TODO:
        problem3 = ("""max π1 + 2π2
            2π1 + π2 ≥ 4
            7π1 + π2 <= 1
            -π2 = 2
            π1 <= 0
            π2 irrestrito""", {"detailed": True, "decimal": False}) 
        
        
        
        problems = [problem1, problem2]
        #problems = [problem2]
        problems_ans = [problem_ans1, problem_ans2]
        for problem, problem_ans in zip(problems, problems_ans):
            #print(problem)
            #print(problem_ans)
            problem_ans = problem_ans.split("\n")
            problem_ans = [x.lstrip() for x in problem_ans]
            std_problem = str_problem_to_standard_form(problem[0], detailed=problem[1]["detailed"], 
                                                        decimal=problem[1]["decimal"])
            std_problem = std_problem.split("\n")
            for i, (x, y) in enumerate(zip(problem_ans, std_problem)):
                try: 
                    if VERBOSE:
                        logging.debug(f"Comparando {x} e {y}")
                    assert x.strip() == y
                except AssertionError as e:
                    logger.error(f"Erro na linha {i}, valor calculado: {y}, valor esperado: {x}")
                    raise e
         
    # Testes para str_problem_to_std_form_matrix
    if test_problema_padrao_matriz:
        logger.info("Iniciando testes para std_matrix_to_str_problem")
        # Teste 1
        problem1 = ("""min x1 + 2x2
            2x1 + x2 ≥ 2/3
            x1 + x2 ≥ 1
            x2 = 2
            x1 >= 0
            x2 >= 0""", {"decimal": False})
        
        ans1 = {"c": [1, 2, 0, 0],
                "b": [Fraction(-2, 3), -1, 2],
                "A": [[-2, -1, 1, 0],
                      [-1, -1, 0, 1],
                      [0, 1, 0, 0]],
                "x": ["x1", "x2", "s1", "s2"]}
        problems = [problem1]
        answers = [ans1]
        
        for ans, problem in zip(answers, problems):
            #print(problem)
            #print(problem_ans)
            A, b, c, x = str_problem_to_std_form_matrix(problem[0], decimal=problem[1]["decimal"])
            try:
                assert A == ans["A"]
                assert b == ans["b"]
                assert c == ans["c"]
                assert x == ans["x"]
            except AssertionError as e:
                logger.error(f"Erro no teste: {problem[0]}")
                for str_mat, ans_mat in zip([A, b, c, x], [ans["A"], ans["b"], ans["c"], ans["x"]]):
                    logger.error(f"calculado\n{str_mat}\nesperado\n{ans_mat}")
                raise e
    
    # Testes para std_matrix_to_str_problem
    if test_matriz_para_problema_padrao:
        logger.info("Iniciando testes para std_matrix_to_str_problem")

        """ problem_structure (
            [A],
            [b],
            [c],
            [x],
            tipo_funcao,
            [restricoes_simbolos],
        )
            
             """

        problem1 = {
            "A":[
                [-2, -1, 1, 0],
                [-1, -1, 0, 1],
                [0, 1, 0, 0]
            ],
            "b":[Fraction(-2, 3), -1, 2],
            "c":[1, 2, 0, 0],
            "x":["x1", "x2", "s1", "s2"],
            "standard_form": True,
            "tipo_funcao":"min",
            "restricoes_simbolo": [],
            "detailed": False,
            "decimal": False,
        }
        
        ans1 = ("min x1 + 2x2\n"
        "-2x1 - x2 + s1 = -2/3\n"
        "-x1 - x2 + s2 = -1\n"
        "x2 = 2\n")
        
        problem2 ={ 
            "A":[
                [-2, -1, 1, 0],
                [-1, -1, 0, 1],
                [0, 1, 0, 0]
            ],
            "b":[Fraction(-2, 3), -1, 2],
            "c":[1, 2, 0, 0],
            "x":["x1", "x2", "x3", "x4"],
            "standard_form": True,
            "tipo_funcao":"max",
            "restricoes_simbolo":["<=", "<=", "<="],
            "detailed": False,
            "decimal": False,
        }
        
        ans2 = ("min -x1 - 2x2\n"
        "-2x1 - x2 + x3 + s1 = -2/3\n"
        "-x1 - x2 + x4 + s2 = -1\n"
        "x2 + s3 = 2\n")
        
        problem3 ={ 
            "A":[
                [-2, -1, 1, 0],
                [-1, -1, 0, 1],
                [0, 1, 0, 0]
            ],
            "b":[Fraction(-2, 3), -1, 2],
            "c":[1, 2, 0, 0],
            "x":["x1", "x2", "x3", "x4"],
            "standard_form": False,
            "tipo_funcao":"max",
            "restricoes_simbolo":["<=", "<=", "<="],
            "detailed": False,
            "decimal": False,
        }
        
        ans3 = ("max x1 + 2x2\n"
        "-2x1 - x2 + x3 <= -2/3\n"
        "-x1 - x2 + x4 <= -1\n"
        "x2 <= 2\n")
        
        problems = [problem1, problem2, problem3]
        answers = [ans1, ans2, ans3]
        
        for ans, problem in zip(answers, problems):
            calculado = std_matrix_to_str_problem(problem["A"], problem["b"], problem["c"], 
                                                  problem["x"], tipo_funcao=problem["tipo_funcao"],
                                                  standard_form=problem["standard_form"],
                                                  restricoes_simbolos=problem["restricoes_simbolo"],
                                                  detailed=problem["detailed"], decimal=problem["decimal"],)
            for i, (x, y) in enumerate(zip(ans.split("\n"), calculado.split("\n"))):
                try: 
                    if VERBOSE:
                        logging.debug(f"Comparando {x} e {y}")
                    assert x.strip() == y.strip()
                except AssertionError as e:
                    logger.error(f"Erro no teste: \n{problem['tipo_funcao']}{display_matrix_f_obj(problem['A'], problem['b'], problem['c'], problem['x'])})")
                    logger.error(f"Erro na linha {i}, valor calculado: {y}, valor esperado: {x}")
                    raise e
 
    # Testes para extract_constraints_signs
    if test_extract_constraints_signs:
        logger.info("Iniciando testes para extract_constraints_signs")
        t1 = "2x1 + π2 + 3x4 ≥ 2/3"
        t2 = "π1 + 2x2 <= 5.2"
        t3 = "-x1 + p2 + s3 = -2"
        t4 = "x1 irrestrito"
        tests = [t1, t2, t3, t4]
        
        assert extract_constraints_signs(tests) == ["≥", "<=", "=", "irrestrito"]
 
    # Testes para assemble_variables_constraints
    if test_assemble_variables_constraints:
        logger.info("Iniciando testes para assemble_variables_constraints")
        t1 = {"variables":["x1","x2","x3","x4"] ,"symbols":["≥", "<=", "=", "irrestrito"], "is_vars_on_standard_form":False, 
              "result": ["x1 ≥ 0","x2 <= 0","x3 = 0","x4 irrestrito"]}
        t2 = {"variables":["π1","π2","π3","π4"] ,"symbols":["≤", ">=", "=", "irrestrito"], "is_vars_on_standard_form":False,
              "result": ["π1 ≤ 0","π2 >= 0","π3 = 0","π4 irrestrito"]}
        t3 = {"variables":["x1","x2","x3","x4"] ,"symbols":[], "is_vars_on_standard_form":True, 
              "result": ["x1 >= 0","x2 >= 0","x3 >= 0","x4 >= 0"]}
        tests = [t1, t2, t3]
        
        for test in tests:
            variables = test["variables"]
            symbols = test["symbols"]
            is_vars_on_standard_form = test["is_vars_on_standard_form"]
            result = test["result"]
            try:
                assert assemble_variables_constraints(variables, symbols, is_vars_on_standard_form) == result
            except AssertionError as e:
                logger.error(f"Erro no teste: {test}\nvalor calculado: {assemble_variables_constraints(variables, symbols)}\nvalor  esperado: {result}")
                raise e        
 
def check_health_status():
    logger.level = logging.INFO
    logger.info("Iniciando com os testes utilitarios ...")
    bateria_testes_utilitarios(True, True, True, True, True, True)
    logger.info("Testes utilitarios passaram com sucesso!")
    logger.info("Iniciando com os testes de str_padrao_problema ...")
    bateria_testes_str_padrao_problema(True, 
                                       True, 
                                       True, 
                                       True, 
                                       True, 
                                       True, 
                                       True, 
                                       True,
                                       True,
                                        True,
                                       )
    logger.info("Todos os testes passaram com sucesso!")

bateria_testes_utilitarios(test_extract_ge_le_constraints=True)

#bateria_testes_str_padrao_problema(teste_forma_padrao=True,teste_problema_padrao_matriz=True)

#check_health_status()

#bateria_testes_utilitarios(True, True, True, True, True, True)

#print(extrai_restricao("pi1 irrestrito"))

def str_primal_to_dual(problem:list, standard_form:bool = False, decimal: bool = False):
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
        
    res = """min 4π1 + 5π2
            π1 + 3/2π2
    """
    problems = problem.split("\n")[0]
    tipo_funcao, _, _, variaveis = extrai_f_obj(problem.split("\n")[0])
    
    print(f"problema na forma padrao: {str_problem_to_standard_form(problem)}")
    A, b, c, x = str_problem_to_std_form_matrix(problem)
    AT = (Matrix(A).T).tolist()
    
    # Transformando em variaveis duais
    # Forcando a funcao objetivo DO DUAL como min
    if tipo_funcao.lower() == "max":
        tipo_funcao = "min"
    else:
        c = [-i for i in c]
    
    
    # Formando os simbolos de desigualdade das restricoes associadas as variaveis
    # E transformando as restricoes em irrestrito
    restricoes_simbolos = []
    for restricao in AT:
        restricoes_simbolos.append("<=")
        
    print(f"f_obj do dual {std_matrix_to_str_problem(AT, c, b, x, tipo_funcao, restricoes_simbolos=restricoes_simbolos)}")

#print(extrair_constantes_e_variaveis("-2/3x1 - x2 + 3"))

#print(change_variable_sign_in_f_obj("x2","max 2x1 + 3x2"))
#print(change_variable_sign_in_f_obj("x1","max 2x1 + 3x2"))

#str_primal_to_dual("")

#std_matrix_to_str_problem([], [], [], [], tipo_funcao="max", decimal=False)
         
#str_problem_to_std_form_matrix("min 3/2x1 + 2x2\n2x1 + x2 + 3x4 ≥ 2/3")       


#str_problem_to_standard_form("", detailed=True)

#bateria_testes_str_padrao_problema(True, True, True, True, True, True)



#bateria_testes()

# str_problem_to_matrix("")



# π, Φ