#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual + forma‑padrão completa
maio/2025
"""
from fractions import Fraction
from typing    import List, Tuple
from sympy     import Matrix


# ================================================================
# 1) PRIMAL  →  DUAL
# ================================================================
def primal_to_dual_extended(
    c: List[float], A: List[List[float]], b: List[float],
    constr_senses: List[str], var_signs: List[str], objective: str
) -> Tuple[str, List[Fraction], List[List[Fraction]], List[Fraction],
           List[str], List[str]]:
    A = Matrix([[Fraction(a) for a in row] for row in A])
    c = Matrix([Fraction(ci) for ci in c])
    b = Matrix([Fraction(bi) for bi in b])
    m, n = A.rows, A.cols

    dual_y_signs = [
        {"<=": ">=0", ">=": "<=0", "=": "free"}[s] for s in constr_senses
    ]
    dual_A = [[A[i, j] for i in range(m)] for j in range(n)]   # Aᵀ
    dual_b = list(c)                                           # c

    if objective not in ("max", "min"):
        raise ValueError("objective deve ser 'max' ou 'min'")

    dual_senses = []
    for sign in var_signs:
        dual_senses.append(
            {">=0": ">=", "<=0": "<=", "free": "="}[sign]
            if objective == "max" else
            {">=0": "<=", "<=0": ">=", "free": "="}[sign]
        )

    dual_obj_type = "min" if objective == "max" else "max"
    dual_c        = list(b)                                    # b

    return (dual_obj_type, dual_c, dual_A,
            dual_b, dual_senses, dual_y_signs)


# ================================================================
# 2) DESIGUALDADES → IGUALDADES  (folga / excesso)
# ================================================================
def add_slack_variables(
    A: List[List[Fraction]], b: List[Fraction], c: List[Fraction],
    senses: List[str]
) -> Tuple[List[List[Fraction]], List[Fraction],
           List[Fraction], List[str], List[int]]:
    A = [row[:] for row in A]
    b = list(b); c = list(c); senses = list(senses)
    slack_idx = []

    for i, s in enumerate(senses):
        if s not in ("<=", ">="):          # já é "="
            continue

        # nova coluna nula …
        for row in A:
            row.append(Fraction(0))
        # … com coef. +1 (folga) ou –1 (excesso) na linha i
        A[i][-1] = Fraction(1) if s == "<=" else Fraction(-1)
        c.append(Fraction(0))
        slack_idx.append(len(c) - 1)
        senses[i] = "="                    # virou igualdade

    return A, b, c, senses, slack_idx


# ================================================================
# 3) VARIÁVEIS  →  “≥ 0” (forma‑padrão)
# ================================================================
def to_standard_form(
    A: List[List[Fraction]], c: List[Fraction], var_signs: List[str]
) -> Tuple[List[List[Fraction]], List[Fraction], List[str]]:
    """
    - ‘>=0’  mantém a coluna
    - ‘<=0’  multiplica coluna e custo por (–1)
    - ‘free’ duplica:   x  =  x⁺ – x⁻   (ambas ‘>=0’)
    """
    # adiciona variaveis de folga/excesso
    
    m        = len(A)
    new_A    = [[] for _ in range(m)]
    new_c    = []
    new_sign = []

    for j, sign in enumerate(var_signs):
        col = [A[i][j] for i in range(m)]

        if sign == ">=0":                            # mantém
            for i in range(m):
                new_A[i].append(col[i])
            new_c.append(c[j]);  new_sign.append(">=0")

        elif sign == "<=0":                          # inverte
            for i in range(m):
                new_A[i].append(-col[i])
            new_c.append(-c[j]); new_sign.append(">=0")

        elif sign == "free":                         # duplica
            # x⁺
            for i in range(m):
                new_A[i].append(col[i])
            new_c.append(c[j]);  new_sign.append(">=0")
            # x⁻
            for i in range(m):
                new_A[i].append(-col[i])
            new_c.append(-c[j]); new_sign.append(">=0")
        else:
            raise ValueError(f"sinal desconhecido: {sign}")

    return new_A, new_c, new_sign


# ================================================================
# AUXILIAR – imprime o PL
# ================================================================
def print_lp(title: str, obj_type: str,
             c: List[Fraction], A: List[List[Fraction]],
             b: List[Fraction], senses: List[str], signs: List[str]) -> None:
    print(f"\n=== {title} ===")
    print(f"Objective: {obj_type} z = " +
          " + ".join(f"{coef}x{j+1}" for j, coef in enumerate(c)))
    print("Subject to:")
    for i, row in enumerate(A):
        lhs = " + ".join(f"{coef}x{j+1}" for j, coef in enumerate(row))
        print(f"  {lhs} {senses[i]} {b[i]}")
    print("Variable signs:")
    for j, s in enumerate(signs):
        print(f"  x{j+1}: {s}")
    print("-"*60)


# ================================================================
# 4) DEMONSTRAÇÃO RÁPIDA
# ================================================================
if __name__ == "__main__":
    # PRIMAL DE EXEMPLO  (o mesmo do seu post)
    cP  = [2, 1]
    AP  = [[2, 1],
           [2, 3],
           [4, 1],
           [1, 5]]
    bP  = [4, 3, 5, 1]
    sP  = ["<=", "<=", "<=", ">="]        # sentidos
    vP  = [">=0", ">=0"]                  # sinais x1, x2
    obj = "max"

    # -------- 1) gera dual ------------------------------------------
    (objD, cD, AD, bD, sD, vD) = primal_to_dual_extended(
        cP, AP, bP, sP, vP, obj
    )

    # imprime dual “cru”
    print_lp("DUAL – antes das folgas", objD, cD, AD, bD, sD, vD)

    # -------- 2) folga/excesso --------------------------------------
    # AD, bD, cD, sD, idx_slack = add_slack_variables(AD, bD, cD, sD)
    # vD = vD + [">=0"] * len(idx_slack)    # slack sempre ≥0
    # print_lp("DUAL – após folgas", objD, cD, AD, bD, sD, vD)

    # -------- 3) forma‑padrão (≥0) ----------------------------------
    AD, cD, vD = to_standard_form(AD, cD, vD)
    print_lp("DUAL – forma‑padrão final", objD, cD, AD, bD, sD, vD)
    
    from exercicio7 import simplex_min_frac_auto_verbose
    
    simplex_min_frac_auto_verbose(AD, bD, cD)
