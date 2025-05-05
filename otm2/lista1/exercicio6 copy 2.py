# simplex_step_by_step_frac_with_cost_and_ratios.py
import sympy as sp

def simplex_step_by_step(A, b, c, I0, max_iter=50):
    """
    Simplex primal passo-a-passo, com aritmética exata em frações.
    -----------------------------------------------------------------
      A : matriz (m x n)            – coeficientes das restrições
      b : vetor-coluna (m)          – lados direitos
      c : vetor-linha  (n)          – custos (minimização)
      I0: lista de índices (0-based) – base inicial factível
    -----------------------------------------------------------------
      Retorna x*, z*, I*  (solução, valor ótimo, base ótima)
    """

    # --- Converte tudo para SymPy/Rational --------------------------
    A = sp.Matrix(A)
    b = sp.Matrix(b).reshape(len(b), 1)          # garante coluna
    c = sp.Matrix(c).reshape(1, len(c))           # garante linha

    m, n = A.shape
    I = list(I0)                                # variáveis básicas

    for it in range(1, max_iter + 1):
        J = [j for j in range(n) if j not in I]  # não básicas

        # Passo 1: monta sub-matriz da base e calcula x_I, π
        AI      = A[:, I]
        AI_inv  = AI.inv()
        xI      = AI_inv * b
        cI      = c[:, I]
        π       = cI * AI_inv

        # Passo 2: custos reduzidos ĉ_J
        AJ      = A[:, J]
        cJ      = c[:, J]
        c_hat   = π * AJ - cJ

        # ---------- Impressão em frações ---------------------------
        print(f"\n── Iteração {it} ──")
        print(f"I (básicas)      = {[i+1 for i in I]}")
        print(f"J (não-básicas)  = {[j+1 for j in J]}")
        print("AI =");   sp.pprint(AI)
        print("AI⁻¹ ="); sp.pprint(AI_inv)
        print("xIᵗ =", list(map(sp.nsimplify, xI)))
        print("cI  =", list(cI))
        print("cJ  =", list(cJ))
        print("AJ =");   sp.pprint(AJ)
        print("π   =", list(π))
        print("ĉJ  =", list(c_hat))

        # >>>> Cálculo do valor atual da função objetivo
        x = sp.zeros(n, 1)
        for idx, i in enumerate(I):
            x[i, 0] = xI[idx, 0]
        custo_atual = (c * x)[0]

        print(f"Valor atual da função objetivo (custo) z = {custo_atual}")

        # Passo 3: escolhe k que entra
        positivos = [idx for idx, val in enumerate(c_hat.tolist()[0]) if val > 0]
        if not positivos:
            print("\nNenhum custo reduzido positivo → solução ótima.")
            break
        k_idx = max(positivos, key=lambda i: c_hat[0, i])
        k     = J[k_idx]
        print(f"Variável que entra (k) = {k+1}")

        # Passo 5: coluna que entra y_k
        yk = AI_inv * A[:, k]
        print("y_kᵗ =", list(map(sp.nsimplify, yk)))

        # Passo 6: teste de ilimitado
        if all(val <= 0 for val in yk):
            raise ValueError("Problema ilimitado – y_k ≤ 0")

        # Passo 7: razão mínimo x_i / y_i
        ratios = []
        for xi, yi in zip(xI, yk):
            if yi > 0:
                ratios.append(xi / yi)
            else:
                ratios.append(sp.oo)  # infinito (não permitido)
        
        # Mostrando todas as razões
        print("\nRazões xIᵢ / ykᵢ para cada variável básica:")
        for idx, (i_var, ratio) in enumerate(zip(I, ratios)):
            print(f"Variável {i_var+1}: razão = {sp.nsimplify(ratio)}")

        r_idx  = min(range(len(ratios)), key=ratios.__getitem__)
        r      = I[r_idx]
        print(f"\nVariável que sai (r) = {r+1} com razão mínima = {sp.nsimplify(ratios[r_idx])}")

        # Passo 8: pivoteia
        I[r_idx] = k
    else:
        raise RuntimeError("Nº máximo de iterações atingido")

    # Reconstrói solução completa final
    x = sp.zeros(n, 1)
    AI = A[:, I]
    x[I, 0] = AI.inv() * b
    z = (c * x)[0]

    return x, z, I


# ============================================================
# EXEMPLO (Ex. 5 da apostila – fábrica de sapatos)
# ------------------------------------------------------------
A = [
    [1, 7, 4, 1, 0, 0],
    [2, 1, 7, 0, 1, 0],
    [8, 4, 1, 0, 0, 1]
]
b = [100, 100, 100]
c = [-4, -4, -7, 0, 0, 0]
I0 = [3, 4, 5]  # folgas (0-based)

if __name__ == "__main__":
    x_star, z_star, I_star = simplex_step_by_step(A, b, c, I0)
    print("\n⇒ Solução final")
    sp.pprint(sp.Matrix.hstack(sp.Symbol('x*'), x_star.T))
    print(f"z* = {z_star}")
    print("Base ótima I* =", [i+1 for i in I_star])
