#  simplex_standard_form.py  –  rev. 2025-05-01 15:05
import sympy as sp

def simplex_standard_form(A, b, c, I0, max_iter=50, verbose=True):
    flat = lambda M: [M[i] for i in range(M.rows * M.cols)]

    A = sp.Matrix(A)
    b = sp.Matrix(b).reshape(len(b), 1)
    c = sp.Matrix(c).reshape(1, len(c))

    m, n = A.shape
    I = list(I0)

    for it in range(1, max_iter + 1):
        # Passo 1
        B      = A[:, I]
        B_inv  = B.inv()
        x_B    = B_inv * b
        if any(xi < 0 for xi in flat(x_B)):
            raise ValueError("Base não factível (x_B < 0).")

        # Passo 2
        λT   = c[:, I] * B_inv           # já é λᵀ
        N    = [j for j in range(n) if j not in I]
        ĉ_N  = c[:, N] - λT * A[:, N]

        # Teste de ótima
        if all(val >= 0 for val in ĉ_N.tolist()[0]):
            if verbose:
                print(f"\n✓ Iteração {it}: solução ótima.")
                print(f"Básicas I  : {[i+1 for i in I]}")
                print(f"Não-básicas: {[j+1 for j in N]}")
                print("B =");      sp.pprint(B)                # ① B
                print("Bᵀ =");      sp.pprint(B.T)              # ① B transposto
                print("λᵀ =", list(map(sp.nsimplify, λT)))      # ② λ transposto
                print("x_Bᵗ =", list(map(sp.nsimplify, x_B)))
                print("ĉ_N =", list(map(sp.nsimplify, ĉ_N)))
               
               # print("Valor atual da função objetivo (custo) z = ", (c * x_B)[0])
               # print("Base ótima I* =", [i+1 for i in I])
               # print("Variáveis básicas x* = ", [x_B[i, 0] for i in range(m)])

            break

        # Escolha de k
        j_star = min(range(len(N)), key=lambda j: ĉ_N[0, j])
        k      = N[j_star]

        # Direção
        y = B_inv * A[:, k]

        # Ilimitado?
        if all(yi <= 0 for yi in flat(y)):
            raise ValueError("Problema ilimitado (y ≤ 0).")

        β       = [x_B[i, 0] / y[i, 0] if y[i, 0] > 0 else sp.oo for i in range(m)]
        l_star  = min(range(m), key=lambda i: β[i])
        I[l_star] = k                      # troca na base

        # ─────── LOG detalhado ──────────────────────────────
        if verbose:
            print("\n" + "━"*55)
            print(f"Iteração {it}")
            print(f"Básicas I  : {[i+1 for i in I]}")
            print(f"Não-básicas: {[j+1 for j in N]}")
            print("B =");      sp.pprint(B)                # ① B
            print("Bᵀ =");      sp.pprint(B.T)              # ① B transposto
            print("λᵀ =", list(map(sp.nsimplify, λT)))      # ② λ transposto
            print("x_Bᵗ =", list(map(sp.nsimplify, x_B)))
            print("ĉ_N =", list(map(sp.nsimplify, ĉ_N)))
            print(f"→ Entra  x_{k+1}")
            print("yᵗ  =", list(map(sp.nsimplify, y)))
            print("β   =", [sp.nsimplify(r) for r in β])
            print(f"← Sai   linha {l_star+1}")

    else:
        raise RuntimeError("Limite de iterações atingido.")

    # Solução final
    x = sp.zeros(n, 1)
    B  = A[:, I]
    x_B = B.inv() * b
    for row_idx, var_idx in enumerate(I):
        x[var_idx, 0] = x_B[row_idx, 0]
    z = (c * x)[0]
    print("\n═══════ SOLUÇÃO FINAL ═══════")
    sp.pprint(sp.Matrix.hstack(sp.Matrix([[sp.Symbol('x*')]]), x.T))
    print("z* =", z)
    print("Base ótima I* =", [i+1 for i in I])
    print("Variáveis básicas x* =", [x[i, 0] for i in range(n)])
    return x, z, I


# ─── teste rápido ──────────────────────────────────────────
if __name__ == "__main__":
    A = [[1,7,4,1,0,0],
         [2,1,7,0,1,0],
         [8,4,1,0,0,1]]
    b = [100,100,100]
    c = [-4,-4,-7,0,0,0]
    I0 = [3,4,5]

    x_star, z_star, I_star = simplex_standard_form(A,b,c,I0)
