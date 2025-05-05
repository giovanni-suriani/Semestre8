# simplex_standard_form_auto.py
# rev. 2025‑05‑03 22:10  — funciona p/ Fase I ou p/ pular Fase I

from fractions import Fraction            # só se quiser inserir Fractions
import sympy as sp

# ───────────────── utilitário: base‑identidade ────────────────────────
def _identity_basis_cols(A):
    m, n = A.shape
    chosen = [-1]*m
    for j in range(n):
        col = A.col(j)
        ones = [i for i in range(m) if col[i] == 1]
        if len(ones) == 1 and all(col[k] == 0 for k in range(m) if k != ones[0]):
            i = ones[0]
            if chosen[i] == -1:
                chosen[i] = j
    return [j for j in chosen if j != -1]

def simplex_standard_form(A, b, c, I0, max_iter=50, verbose=True):
    
    flat = lambda M: [M[i] for i in range(M.rows * M.cols)]

    A = sp.Matrix(A)
    b = sp.Matrix(b).reshape(len(b), 1)
    c = sp.Matrix(c).reshape(1, len(c))

    m, n = A.shape
    I = list(I0)

    for it in range(1, max_iter + 1):

        # Passo 1 – calcula x_B
        B      = A[:, I]
        B_inv  = B.inv()
        x_B    = B_inv * b
        if any(xi < 0 for xi in flat(x_B)):
            raise ValueError("Base não factível (x_B < 0).")

        # Passo 2 – calcula λᵀ e custos reduzidos
        λT   = c[:, I] * B_inv                 # já é λᵀ
        N    = [j for j in range(n) if j not in I]
        ĉ_N  = c[:, N] - λT * A[:, N]

        # ─── LOG: estado antes do teste de ótima ─────────────────────
        if verbose:
            print("\n" + "━" * 65)
            print(f"Iteração {it}")
            print(f"Básicas I  : {[idx+1 for idx in I]}")
            print(f"Não-básicas: {[idx+1 for idx in N]}")
            print("B =");  sp.pprint(B)
            print("Bᵀ ="); sp.pprint(B.T)
            print("λᵀ =",  [sp.nsimplify(x) for x in flat(λT)])
            print("x_Bᵗ =", [sp.nsimplify(x) for x in flat(x_B)])
            print("ĉ_N =",  [sp.nsimplify(val) for val in flat(ĉ_N)])

        # Teste de ótima
        if all(val >= 0 for val in ĉ_N):
            if verbose:
                print(f"\n✓ Iteração {it}: todos ĉ ≥ 0  →  solução ótima.\n")
            break

        # Passo 3 – escolhe variável que entra (menor ĉ)
        j_star = min(range(len(N)), key=lambda j: ĉ_N[j])
        k      = N[j_star]

        # Passo 4 – direção simplex
        y = B_inv * A[:, k]

        # Ilimitado?
        if all(yi <= 0 for yi in flat(y)):
            raise ValueError("Problema ilimitado (y ≤ 0).")

        # Passo 5 – razão β e variável que sai
        β       = [x_B[i, 0] / y[i, 0] if y[i, 0] > 0 else sp.oo for i in range(m)]
        l_star  = min(range(m), key=lambda i: β[i])

        # ─── LOG: pivoteamento ───────────────────────────────────────
        if verbose:
            print(f"→ Entra  x_{k+1}")
            print("yᵗ  =", [sp.nsimplify(val) for val in flat(y)])
            print("β   =", [sp.nsimplify(val) for val in β])
            print(f"← Sai   linha {l_star+1}")

        # Passo 6 – troca na base
        I[l_star] = k

    else:
        raise RuntimeError("Limite de iterações atingido.")

    # Solução final
    x = sp.zeros(n, 1)
    B  = A[:, I]
    x_B = B.inv() * b
    for row_idx, var_idx in enumerate(I):
        x[var_idx, 0] = x_B[row_idx, 0]
    z = (c * x)[0]

    # ─── LOG final ───────────────────────────────────────────────────
    if verbose:
        print("═══════ SOLUÇÃO FINAL ═══════")
        sp.pprint(sp.Matrix.hstack(sp.Matrix([[sp.Symbol('x*')]]), x.T))
        print("z* =", sp.nsimplify(z))
        print("Base ótima I* =", [i+1 for i in I])
        print("Variáveis básicas x* =", [sp.nsimplify(x[i,0]) for i in range(n)])

    return x, z, I

# ───────────────── versão “auto‑duas‑fases” ───────────────────────────
def simplex_standard_form_auto(A, b, c, I0=None, max_iter=50, verbose=True):
    A = sp.Matrix(A)
    b = sp.Matrix(b).reshape(len(b), 1)
    c = sp.Matrix(c).reshape(1, len(c))
    m, n0 = A.shape

    # 1) garante b ≥ 0 (agora sem usar row_op que bagunça a linha)
    for i in range(m):
        if b[i, 0] < 0:
            A[i, :] = -A[i, :]
            b[i, 0] = -b[i, 0]

    # 2) escolhe base inicial
    base_cols = list(I0) if I0 is not None else _identity_basis_cols(A)
    needs_phase_I = (len(base_cols) != m)

    # ─── caso 1: não precisa Fase I ───────────────────────────────────
    if not needs_phase_I:
        if verbose: print("▶ Base identidade encontrada – pulando Fase I\n")
        return simplex_standard_form(A, b, c, base_cols, max_iter, verbose)

    # ─── caso 2: monta Fase I (apenas linhas sem base) ───────────────
    if verbose: print("▶ Base factível não encontrada – executando Fase I\n")

    has_base = [False]*m
    for col in base_cols:
        row = next(i for i in range(m) if A[i, col] == 1)
        has_base[row] = True
    art_rows = [i for i, ok in enumerate(has_base) if not ok]

    n_art  = len(art_rows)
    A_art  = sp.zeros(m, n_art)
    for idx, i in enumerate(art_rows):
        A_art[i, idx] = 1
    A1 = A.row_join(A_art)
    c_phase1 = sp.Matrix([[0]*n0 + [1]*n_art])          # minimizar soma das artificiais

    I_phase1 = [next(j for j in base_cols if A[i, j] == 1) if has_base[i]
                else n0 + art_rows.index(i)
                for i in range(m)]

    # ---------- Fase I ----------
    x_p1, z_p1, I_p1 = simplex_standard_form(A1, b, c_phase1, I_phase1, max_iter, verbose)
    if abs(float(z_p1)) > 1e-12:
        raise ValueError("Problema inviável (ótimo da Fase I ≠ 0).")

    # ---------- remove artificiais da base ----------
    I_base = []
    for idx in I_p1:
        if idx < n0:                      # variável original
            I_base.append(idx)
        else:                             # artificial → tenta pivotar
            row = I_p1.index(idx)
            pivoted = False
            for j in range(n0):
                if j not in I_base and A[row, j] != 0:
                    I_base.append(j)
                    pivoted = True
                    break
            if not pivoted:
                pass  # linha redundante

    if len(I_base) != m:                  # completa com identidade se faltou
        extra = [j for j in _identity_basis_cols(A) if j not in I_base]
        I_base.extend(extra[:m - len(I_base)])

    # ---------- Fase II ----------
    if verbose: print("\n▶ Iniciando Fase II\n")
    return simplex_standard_form(A, b, c, I_base, max_iter, verbose)


# ────────────────────────── TESTE RÁPIDO ──────────────────────────────
if __name__ == "__main__":
    # (1) problema com base identidade – Fase I pulada
    A1 = [[1, 2, 1, 0],
          [2, 1, 0, 1]]
    b1 = [8, 7]
    c1 = [5, 4, 0, 0]
    # print("=== Exemplo sem Fase I ===")
    # x, z, I = simplex_standard_form_auto(A1, b1, c1, verbose=True)
    # print("x* =", [Fraction(xi) for xi in x])
    # print("z* =", Fraction(z))

    # (2) problema que exige Fase I
    A2 = [[-2, -2, -4,  1, 1, 0],
          [-1, -3, -1,  5, 0, 1]]
    b2 = [-2, -1]
    c2 = [4, 3, 5, -1, 0, 0]
    print("\n=== Exemplo com Fase I ===")
    x, z, I = simplex_standard_form_auto(A2, b2, c2, verbose=True)
    print("x* =", [Fraction(xi) for xi in x])
    print("z* =", Fraction(z))


    A2 = [[2, 2, 4,  -1, -1, 0],
      [1, 3, 1,  -5, 0, -1]]
    b2 = [2, 1]
    c2 = [4, 3, 5, -1, 0, 0]
    x, z, I = simplex_standard_form_auto(A2, b2, c2, verbose=True)