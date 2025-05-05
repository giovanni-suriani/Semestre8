import sympy as sp

# Função para isolar x2
def isolar_x2(expressao_str):
    x1, x2 = sp.symbols('x1 x2')
    eq = sp.sympify(expressao_str)
    solucao = sp.solve(eq, x2)
    return solucao[0]

# Função de uma variável
def f_x(func, x1_valor):
    return func(x1_valor)

# Função de duas variáveis
def g_x(func, x1_valor, x2_valor):
    return func(x1_valor, x2_valor)

# ---- USO ----
x1, x2 = sp.symbols('x1 x2')

# Expressão original (forma igualdade)
expr = '-4*x1 + 2*x2 + 8'

# Isolar x2
x2_expr = isolar_x2(expr)

# f_x: cria função x2 = f(x1)
x2_func = sp.lambdify(x1, x2_expr)

# g_x: reusar a expressão original, transformada em função de 2 variáveis
expr_func_duas_vars = sp.lambdify((x1, x2), sp.sympify(expr))

# Testar
x1_valor = 0
x2_valor_calculado = f_x(x2_func, x1_valor)  # Calcula x2 para x1 = 0
print(f"Para x1 = {x1_valor}, x2 = {x2_valor_calculado}")

x2_valor = -4.1
g_x_valor_calculado = g_x(expr_func_duas_vars, x1_valor, x2_valor_calculado)  # Verifica se a expressão original é verdadeira
g_x_valor = g_x(expr_func_duas_vars, x1_valor, x2_valor)  # Verifica se a expressão original é verdadeira
print(f"Para x1 = {x1_valor} e x2 = {x2_valor_calculado}, a expressão original é: {g_x_valor_calculado}\nPara x1 = {x1_valor} e x2 = {x2_valor}, a expressão original é: {g_x_valor}")
# Testar com outro valor
x1_valor = 1
