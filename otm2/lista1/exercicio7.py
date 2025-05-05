# simplex_tableau_frac_noslack.py
from fractions import Fraction

def to_frac_matrix(mat):
    return [[Fraction(x) for x in row] for row in mat]

def simplex_tableau_min_frac(A, b, c, max_iter=50):
    """
    Simplex-tabela (minimização) JÁ na forma-padrão.
    NÃO adiciona novas folgas: considera que as últimas m colunas de A
    são a base inicial.
    """
    # ─── preparação ───
    m, n = len(A), len(A[0])          # m eq., n variáveis (incluindo folgas)
    A = to_frac_matrix(A)
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]

    # ★ tableau (m+1) × (n+1) – NÃO há colunas extras de s1,s2,s3
    T = [[Fraction(0) for _ in range(n + 1)] for _ in range(m+1)]

    # linha-custo
    for j in range(n):
        T[0][j] = -c[j]

    # restrições
    for i in range(m):
        T[i+1][:n] = A[i]
        T[i+1][-1] = b[i]

    var  = [f"x{j+1}" for j in range(n)]      # ★ só x1…xn
    base = var[-m:]                           # ★ últimas m = folgas prontas

    # ---- impressão opcional ----
    def print_tableau(it_):
        head = ["  "] + var + ["LD"]
        print(f"\n── Tabela – iteração {it_} ──")
        print(" | ".join(f"{h:>8}" for h in head))
        print("-" * (12*(len(var)+2)))
        for i, row in enumerate(T):
            tag = "z" if i == 0 else base[i-1]
            print(f"{tag:>2} | " + " | ".join(f"{str(x):>8}" for x in row))

    print_tableau(0)

    # ---- loop simplex ----
    # ───────── Loop Simplex ─────────
    for it in range(1, max_iter+1):

        # 1. escolhe coluna que entra  (PASSO b)
        enter_col, best = None, Fraction(0)
        for j in range(n):                       # percorre APENAS colunas x1…xn
            if T[0][j] > 0 and T[0][j] > best:
                best, enter_col = T[0][j], j

        if enter_col is None:                    # condição de ótimalidade
            print("\n*** ÓTIMO ALCANÇADO ***")
            print("\n⇒ Solução ótima (frações):")
            for j, val in enumerate(T[0][:-1], 1):
                print(f"x{j} = {val}")
            print("z* =", T[0][-1])
            break

        # ─── (IMPRESSÃO 1)  k e y_k ───────────────────────────────
        yk = [T[i][enter_col] for i in range(1, m+1)]      # coluna k nas linhas 1..m
        print(f"\n♦ Iteração {it}")
        print(f"  k  (entra) : {var[enter_col]}")          # nome da variável que entra
        print(f"  y_k        : {[str(v) for v in yk]}")


        # 2. escolhe linha que sai  (PASSO c)
        pivot_row, min_ratio = None, None
        for i in range(1, m+1):
            col_val = T[i][enter_col]
            if col_val > 0:
                ratio = T[i][-1] / col_val
                if pivot_row is None or ratio < min_ratio:
                    pivot_row, min_ratio = i, ratio
        if pivot_row is None:
            raise ValueError("Problema ilimitado")

        # ─── (IMPRESSÃO 2)  r e razão ─────────────────────────────
        print(f"  r  (sai)   : {base[pivot_row-1]}")
        print(f"  razão min  : {min_ratio}\n")

        # 3. pivoteamento (PASSO d)
        piv = T[pivot_row][enter_col]
        T[pivot_row] = [x / piv for x in T[pivot_row]]
        for i in range(m+1):
            if i == pivot_row:
                continue
            factor = T[i][enter_col]
            T[i] = [x - factor*y for x, y in zip(T[i], T[pivot_row])]

        # 4. atualiza base e imprime tableau
        base[pivot_row-1] = var[enter_col]
        print_tableau(it)

    else:
        raise RuntimeError("Limite de iterações atingido")

    # solução
    x = [Fraction(0) for _ in range(n)]
    for i, bv in enumerate(base):
        x[var.index(bv)] = T[i+1][-1]
    z = T[0][-1]
    return x, z


# ===================== EXEMPLO: problema da imagem =====================
if __name__ == "__main__":
    A = [
        [2, 1, 1, 0, 0],   # 2x1 +  x2 + x3 = 8
        [1, 2, 0, 1, 0],   #  x1 + 2x2 + x4 = 7
        [0, 1, 0, 0, 1]    #       x2 + x5 = 3
    ]
    b = [8, 7, 3]
    c = [-1, -1, 0, 0, 0]   # min -x1 - x2

    x_opt, z_opt = simplex_tableau_min_frac(A, b, c)

