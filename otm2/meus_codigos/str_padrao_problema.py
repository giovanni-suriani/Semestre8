import re
import logging
from fractions import Fraction
from pprint import pprint
import sympy as sp
from sympy import Matrix, pprint, pretty

Fraction.__str__


logger = logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s:%(funcName)s:%(message)s"
)

logger = logging.getLogger(__name__)

VERBOSE = False

def checa_restricao_maior_igual_zero(constantes_lhs, valor_rhs, simbolo:str = "≥"):
    """
    Checa se a restrição é maior ou igual a zero.
    Args:
        constantes_lhs (list[Fraction]): coeficientes do lado esquerdo
        valor_rhs (Fraction): valor do lado direito da restrição
        simbolo (str): símbolo de comparação
    Returns:
        bool: True se a restrição for maior ou igual a zero, False caso contrário
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
        
def str_list_fraction(fractions:list):
    str_frac = ""
    for fraction in fractions:
        str_frac += str(fraction) + " "
    return str_frac.strip()

def extrair_constantes_e_variaveis(expr:str):
    """
    Retorna listas de constantes (como Fraction) e variáveis de uma expressão
    Args:
        expr (str): expressão a ser analisada, ex: "3x1 + 2x2 - 5x3"
    Returns:
        Tuple:
            - constantes (list[Fraction]): lista de coeficientes
            - variaveis (list[str]): lista de variáveis
    """
    padrao = re.compile(
        r"([+-]?\s*(?:\d+(?:\.\d+)?|\d+/\d+)?)(\w\d+)",  # aceita int, decimal, fração
        re.UNICODE
    )

    termos = re.findall(padrao, expr)
    constantes = []
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
        variaveis.append(var)

    return constantes, variaveis

def extrai_f_obj(f_obj:str):
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

def extrai_restricao(restricao:str):
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
        r'([-+]?\s*'                         # sinal opcional
        r'(\d+(\.\d+)?|\d+/\d+)?'          # constante (inteiro, decimal ou fração)
        r'\s*\w\d+\s*)+'                       # variável com número (ex: π1, x2)
    r'))\s*'                                   # ← fecha grupo restricao_lhs e ignora espaços
    r'(?P<restricao_simbolo><=|>=|<|>|=|≥|≤)'      # símbolo de comparação
    r'\s*'                                     # ignora espaços ao redor do símbolo
    r'(?P<restricao_rhs>('                     # ← grupo nomeado para lado direito
        r'[-+]?\s*(?:\d+/\d+|\d+(?:\.\d+)?)'    # constante do lado direito
    r'))',
    re.UNICODE
    )
    match = re.search(padrao, restricao)
    assert match, f"Expressão inválida {restricao}"
    restricao_lhs = match.group("restricao_lhs")
    restricao_simbolo = match.group("restricao_simbolo")
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

def monta_f_obj(tipo_funcao:str, constantes_e_variaveis:dict, standard_form:bool = False, detailed:bool = False, decimal:bool = False) -> str:
    """
    Monta a função objetivo a partir dos componentes extraídos.
    Args:
        tipo_funcao (str): "max" ou "min"
        constantes (dict): coeficientes extraídos
        detailed (bool): se True, retorna a função com termos em 0
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
        standard_form (tuple): se True, retorna a função na forma padrão
        detailed (bool): se True, retorna a função com termos em 0
    Returns:
        str: restrição montada
        int: nada acontece = 0, variavel adicionada = 1, variavel alterada = 2   
    """
    # Checando se é restrição x1 >= 0 ou 
    non_zero_var = 0
    constantes_lhs = list(constantes_e_variaveis_lhs.values())
    
    constant_foo = 0
    for variavel, constante in constantes_e_variaveis_lhs.items():
        if constante != 0:
            non_zero_var += 1
            constant_foo = constante
            variable_foo = variavel
            
    change_var = 0
    
    # Checando se é restrição x1 >= 0 ou 
    if standard_form[0] is True:
        if non_zero_var == 1:
            if (simbolo == ">=" or simbolo == "≥") and valor_rhs == 0 :
                if constant_foo < 0:
                    change_var = 2
                    lhs = standard_display_variable(constant_foo, variable_foo, first_var=True, decimal=decimal)
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
                    lhs = standard_display_variable(constant_foo, variable_foo, first_var=True, decimal=decimal)
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
        primeira = (i == 0)
        if primeira:
            lhs += standard_display_variable(constante, variavel, primeira, show_zero=detailed, decimal=decimal)
        else:
            lhs += " " + standard_display_variable(constante, variavel, primeira, show_zero=detailed, decimal=decimal)
    if VERBOSE:
        logger.debug(f"{lhs.strip()} {simbolo} {valor_rhs} {change_var}")
    return f"{lhs.strip()} {simbolo} {valor_rhs}", change_var
            
    # Segundo, variávies de folga
    
def str_problem_to_standard_form(problem, detailed:bool = False, decimal:bool = False):
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
    constantes_e_variaveis = dict(zip(variaveis, constantes))
    slack_var = 1
    new_restricoes = []
    
    for restricao in restricoes:
        # pegar todas variaveis das restricoes
        pass
    
    for restricao in restricoes:
        constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(restricao)
        constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
        forma_padrao_restricao, change_var = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(True, "s" + str(slack_var)),
                                                             detailed=detailed, decimal=decimal)
        if change_var == 1:
            constantes_e_variaveis["s" + str(slack_var)] = 0
            slack_var += 1
        elif change_var == 2:
            for variavel, constante in constantes_e_variaveis_lhs.items():
                # Trocando o sinal da variavel
                if constante != 0:
                    constantes_e_variaveis[variavel] = -constantes_e_variaveis[variavel]
        new_restricoes.append(forma_padrao_restricao)
        if VERBOSE:
            logger.debug(f"forma_padrao_restricao {restricao.lstrip()} SE TRANSFORMA EIN {forma_padrao_restricao}")
    #monta_f_obj(tipo_funcao, constantes_e_variaveis, standard_form=True, detailed=detailed, decimal=decimal)
    # Adicionando 0's nas variaveis que nao aparecem nas restricoes, mas estao na funcao objetivo
    if detailed:
        restricoes = new_restricoes
        new_restricoes = []
        for restricao in restricoes:
            constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(restricao)
            constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
            constantes_e_variaveis_lhs = adicionando_variaveis_zeradas_na_expr(constantes_e_variaveis, constantes_e_variaveis_lhs)
            forma_padrao_restricao_detailed, _ = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(True, "s" + str(slack_var)),
                                                                 detailed=detailed, decimal=decimal) 
            new_restricoes.append(forma_padrao_restricao_detailed)
            if VERBOSE:
                logger.debug(f"forma_padrao_restricao_detailed {restricao.lstrip()} SE TRANSFORMA EIN {forma_padrao_restricao_detailed}")
    f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis, standard_form=True, detailed=detailed, decimal=decimal)
    std_problem = f_obj + "\n"
    for restricao in new_restricoes:
        std_problem += restricao + "\n"
    std_problem = std_problem.strip()
    logger.debug(f"Função objetivo antiga: \n{problem}")
    logger.debug(f"\nFunção objetivo padrão: \n{std_problem}")
    return std_problem
        
def str_problem_to_std_form_matrix (problem, decimal:bool = False): 
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
        constantes_lhs = list(constantes_lhs)
        for constante in constantes_lhs:
            if constante != 0:
                non_zero_var += 1
        
        if simbolo == ">=" or simbolo == "≥":
            if valor_rhs == 0:
                if non_zero_var == 1:
                    continue
        A.append(constantes_lhs)
        b.append(valor_rhs)
    A_matrix = Matrix(A)
    B_matrix = Matrix(b)
    c_matrix = Matrix(c)
    x_matrix = Matrix(variaveis)

    # Mostra bonitinho no console
    # Mostra bonitinho no log (como string)
    logger.debug("\nMatriz A \n" + pretty(A_matrix) + "\n Matriz B \n" + pretty(Matrix(b)) + "\n Matriz C \n" + pretty(Matrix(c)) 
                 + "\n Matriz X \n" + pretty(Matrix(variaveis)))
    return A, b, c, variaveis
        
def std_matrix_to_str_problem(A, b, c, x, tipo_funcao:str = "max", decimal:bool = False):
    """
    Converte uma matriz de programação linear em sua forma padrão para string.
    Args:
        A (list): matriz de coeficientes
        b (list): vetor de constantes
        c (list): vetor de coeficientes da função objetivo
        x (list): lista de variáveis
        tipo_funcao (str): "max" ou "min"
        decimal (bool): se True, retorna a função com termos em 0
    Returns:
        str: problema transformado para forma padrão
    """
    # Monta a função objetivo
    A = [[-2, -1, 1, 0],
        [-1, -1, 0, 1],
        [0, 1, 0, 0]],
    b = [Fraction(2, 3), Fraction(26, 5), Fraction(0, 1)]
    c = [Fraction(3, 2), Fraction(2), Fraction(0, 1), Fraction(0, 1)]
    x = ["x1", "x2", "s1", "s2"]
    constantes_e_variaveis = dict(zip(x, c))
    f_obj = monta_f_obj(tipo_funcao, constantes_e_variaveis, standard_form=True, detailed=True, decimal=decimal)
    
    # Monta as restrições
    restricoes = []
    for i in range(len(A[0])):
        constantes_lhs = A[0][i]
        variaveis_lhs = x
        simbolo = "="
        valor_rhs = b[i]
        constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
        forma_padrao_restricao, _ = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=(True, "s1"),
                                                     detailed=True, decimal=decimal)
        restricoes.append(forma_padrao_restricao)
    
    # Monta o problema final
    std_problem = f_obj + "\n"
    for restricao in restricoes:
        std_problem += restricao + "\n"
    
    logger.debug(f"Função objetivo de matriz para padrão: \n{std_problem.strip()}")
    return std_problem.strip()
        
def bateria_testes_str_padrao_problema(teste_extrai_f_obj:bool = False, teste_extrai_restricao:bool = False, 
                   teste_monta_f_obj:bool = False, teste_monta_restricao:bool = False, teste_forma_padrao:bool = False, 
                   teste_problema_padrao_matriz:bool = False):
    # Testes para extrair_f_obj
    if teste_extrai_f_obj:
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
    if teste_extrai_restricao:
        logger.info(f"Iniciando testes para extrair_restricao")
        t1 = "2x1 + π2 + 3x4 ≥ 2/3"
        t2 = "π1 + 2x2 ≤ 5.2"
        t3 = "-x1 + p2 + s3 = -2"
        
        assert extrai_restricao(t1) == ([Fraction(2, 1), Fraction(1, 1), Fraction(3, 1)], ["x1", "π2", "x4"], "≥", Fraction(2, 3))
        assert extrai_restricao(t2) == ([Fraction(1, 1), Fraction(2, 1)], ["π1", "x2"], "≤", Fraction(26, 5))
        assert extrai_restricao(t3) == ([Fraction(-1, 1), Fraction(1, 1), Fraction(1, 1)], ["x1", "p2", "s3"], "=", Fraction(-2, 1))
    
    # Testes para monta_f_obj
    if teste_monta_f_obj:
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
                print(f"Erro no teste: {teste[0]}, valor calculado: {str_f_obj}, valor esperado: {teste[3]}")
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
                print(f"Erro no teste: {teste[0]}, valor calculado: {str_f_obj}, valor esperado: {teste[2]}")
                raise e
    
    # Testes para monta_restricao
    if teste_monta_restricao:
        logger.info("Iniciando testes para monta_restricao")
        t1 = ("2x1 + π2 + 3x4 ≥ 2/3", (False, "s1"), {"detailed": True, "decimal": False}, ("2x1 + π2 + 3x4 ≥ 2/3", 0))
        t2 = ("2x1 + π2 + 3x4 ≥ 2/3", (True, "s1"), {"detailed": True, "decimal": False}, ("-2x1 - π2 - 3x4 + s1 = -2/3", 1))
        t3 = ("2x1 + π2 + 3x4 <= 2/3", (True, "s1"), {"detailed": True, "decimal": False}, ("2x1 + π2 + 3x4 + s1 = 2/3", 1))
        t4 = ("x1 >= 0", (False, "s1"), {"detailed": False, "decimal": False}, ("x1 >= 0", 0))    
        t5 = ("x1 <= 0", (False, "s1"), {"detailed": False, "decimal": False}, ("x1 <= 0", 0))
        t6 = ("x1 <= 0", (True, "s1"), {"detailed": False, "decimal": False}, ("x1 >= 0", 2))
        testes = [t1, t2, t3, t4, t5, t6]
        
        for teste in testes:
            #teste = t5
            constantes_lhs, variaveis_lhs, simbolo, valor_rhs = extrai_restricao(teste[0])
            constantes_e_variaveis_lhs = dict(zip(variaveis_lhs, constantes_lhs))
            try:
                valor = monta_restricao(constantes_e_variaveis_lhs, simbolo, valor_rhs, standard_form=teste[1], 
                                                            detailed=teste[2]["detailed"], decimal=teste[2]["decimal"])
                assert valor == teste[3]
            except AssertionError as e:
                print(f"Erro no teste: {teste[0]}, valor calculado: {valor}, valor esperado: {teste[3]}")
                raise e
        
    # Testes para str_problem_to_standard_form
    if teste_forma_padrao:
        logger.info("Iniciando testes para str_problem_to_standard_form")
        # Teste 1
        problem1 = ("""min x1 + 2x2
                2x1 + x2 ≥ 2/3
                x1 + x2 ≥ 1
                x2 = 2
                x1 >= 0
                x2 <= 0""", {"detailed": False, "decimal": False})
                
        problem_ans1 = """min x1 - 2x2 
                -2x1 - x2 + s1 = -2/3
                -x1 - x2 + s2 = -1
                x2 = 2
                x1 >= 0
                x2 >= 0"""
                
        problem2 = ("""max π1 + 2π2
                2π1 + π2 ≥ 4
                7π1 + π2 <= 1
                -π2 = 2
                π1 <= 0
                π2 >= 0""", {"detailed": True, "decimal": False})
                
        problem_ans2 = """MIN π1 - 2π2 + 0s1 + 0s2
                -2π1 - π2 + s1 + 0s2 = -4
                7π1 + π2 + 0s1 + s2 = 1
                0π1 - π2 + 0s1 + 0s2 = 2
                π1 >= 0
                π2 >= 0"""
        
        problems = [problem1, problem2]
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
                    print(f"Erro na linha {i}, valor calculado: {y}, valor esperado: {x}")
                    raise e
         
    if teste_problema_padrao_matriz:
        logger.info("Iniciando testes para str_problem_to_std_form_matrix")
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
                print(f"Erro no teste: {problem[0]}")
                for str_mat, ans_mat in zip([A, b, c, x], [ans["A"], ans["b"], ans["c"], ans["x"]]):
                    print(f"calculado\n{str_mat}\nesperado\n{ans_mat}")
                raise e
    
std_matrix_to_str_problem([], [], [], [], tipo_funcao="max", decimal=False)
         
#str_problem_to_std_form_matrix("min 3/2x1 + 2x2\n2x1 + x2 + 3x4 ≥ 2/3")       


#str_problem_to_standard_form("", detailed=True)

#bateria_testes_str_padrao_problema(True, True, True, True, True, True)



#bateria_testes()

# str_problem_to_matrix("")



# π, Φ