# simplex_step_by_step.py
import numpy as np

def simplex_step_by_step(A, b, c, I0, max_iter=50):
    """
    Método Simplex (primal) com impressões detalhadas.
    -----------------------------------------------------------------
    A : matriz (m x n)
    b : vetor (m)
    c : vetor (n)          (função a minimizar)
    I0: lista/tupla        índices (0-based) da base inicial factível
    -----------------------------------------------------------------
    Retorna x*, z*, I*  (solução, valor ótimo, base ótima)
    """
    np.set_printoptions(precision=4, suppress=True)
    m, n = A.shape
    I = list(I0)                       # básica   (será atualizada)
    for it in range(1, max_iter+1):
        J = [j for j in range(n) if j not in I]   # não-básicas

        # Passo 1 – calcula x_I, π, z₀ :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}
        AI      = A[:, I]
        AI_inv  = np.linalg.inv(AI)
        xI      = AI_inv @ b
        pi      = c[I] @ AI_inv
        AJ      = A[:, J]
        c_hat   = pi @ AJ - c[J]        # Passo 2: custos reduzidos

        # ---------- PRINTS PEDIDOS ----------
        print(f"\n── Iteração {it} ──")
        print(f"I (básicas)      = {[i+1 for i in I]}")
        print(f"J (não-básicas)  = {[j+1 for j in J]}")
        print("AI =\n", AI)
        print("AI⁻¹ =\n", AI_inv)
        print("xI =", xI)
        print("cI =", c[I])
        print("cJ =", c[J])
        print("AJ =\n", AJ)
        print("π  =", pi)
        print("ĉJ =", c_hat)

        # Passo 3 – escolhe k que entra
        k_idx = np.argmax(c_hat)
        k     = J[k_idx]
        if c_hat[k_idx] <= 1e-12:       # Passo 4 – ótimalidade
            print("\nNenhum custo reduzido positivo → solução ótima.")
            break

        # Passo 5 – coluna da variável que entra (y_k)
        yk = AI_inv @ A[:, k]
        print("y_k =", yk)

        # Passo 6 – teste de ilimitado
        if np.all(yk <= 1e-12):
            raise ValueError("Problema ilimitado – y_k ≤ 0")

        # Passo 7 – razão para escolher r que sai :contentReference[oaicite:4]{index=4}&#8203;:contentReference[oaicite:5]{index=5}
        ratios = np.array([xi/yi if yi > 1e-12 else np.inf
                           for xi, yi in zip(xI, yk)])
        r_idx  = np.argmin(ratios)
        r      = I[r_idx]
        print(f"r (sai) = variável {r+1},   razão mínima = {ratios[r_idx]}")

        # Passo 8 – pivoteia: troca r←k
        I[r_idx] = k
    else:
        raise RuntimeError("Nº máx. de iterações atingido")

    # Reconstrói solução completa
    x = np.zeros(n)
    x[I] = AI_inv @ b
    z = c @ x
    return x, z, I

# ============================================================
# EXEMPLO (Ex. 5 da apostila – fábrica de sapatos)  :contentReference[oaicite:6]{index=6}&#8203;:contentReference[oaicite:7]{index=7}
# ------------------------------------------------------------
# Matriz A (coeficientes das variáveis)
A = np.array([
    [1, 7, 4, 1, 0, 0],
    [2, 1, 7, 0, 1, 0],
    [8, 4, 1, 0, 0, 1]
], dtype=float)

# Vetor b (lado direito das equações)
b = np.array([100, 100, 100], dtype=float)

# Vetor c (coeficientes da função objetivo, incluindo folgas com custo 0)
c = np.array([-4, -4, -7, 0, 0, 0], dtype=float)

# Conjunto I inicial (índices das variáveis básicas: as de folga)
I0 = [3, 4, 5]  # indices 0-based: s1, s2, s3

if __name__ == "__main__":
    x_star, z_star, I_star = simplex_step_by_step(A, b, c, I0)
    print("\n⇒ Solução final")
    print("x* =", x_star)
    print("z* =", z_star)
    print("Base ótima I* =", [i+1 for i in I_star])
