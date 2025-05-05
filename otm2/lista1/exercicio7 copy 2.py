from fractions import Fraction

def to_frac_matrix(mat):
    return [[Fraction(x) for x in row] for row in mat]

def simplex_tableau_min_frac(A, b, c, I0=None, max_iter=50):
    """
    Simplex-tabela (minimização) JÁ na forma-padrão.
    NÃO adiciona novas folgas: considera que as colunas de I0 são a base inicial.
    Se I0 não for fornecido, usa as últimas m colunas de A.
    """
    m, n = len(A), len(A[0])          # m eq., n variáveis (incluindo folgas)
    A = to_frac_matrix(A)
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]

    # Definição da base inicial
    if I0 is None:
        I0 = list(range(n - m, n))  # base padrão: últimas m colunas
    base_indices = I0[:]            # cópia explícita

    # ★ tableau (m+1) × (n+1)
    T = [[Fraction(0) for _ in range(n + 1)] for _ in range(m+1)]

    # linha-custo
    for j in range(n):
        T[0][j] = -c[j]

    # restrições
    for i in range(m):
        T[i+1][:n] = A[i]
        T[i+1][-1] = b[i]

    var  = [f"x{j+1}" for j in range(n)]
    base = [var[j] for j in base_indices]  # nomes das variáveis básicas

    def print_tableau(it_):
        head = ["  "] + var + ["LD"]
        print(f"\n── Tabela – iteração {it_} ──")
        print(" | ".join(f"{h:>8}" for h in head))
        print("-" * (12*(len(var)+2)))
        for i, row in enumerate(T):
            tag = "z" if i == 0 else base[i-1]
            print(f"{tag:>2} | " + " | ".join(f"{str(x):>8}" for x in row))

    print_tableau(0)

    for it in range(1, max_iter+1):
        # 1. escolhe coluna que entra
        enter_col, best = None, Fraction(0)
        for j in range(n):
            if T[0][j] > 0 and T[0][j] > best:
                best, enter_col = T[0][j], j

        if enter_col is None:
            print("\n*** ÓTIMO ALCANÇADO ***")
            # solução
            x = [Fraction(0) for _ in range(n)]
            for i, bv in enumerate(base):
                x[var.index(bv)] = T[i+1][-1]
            z = T[0][-1]

            print("\n⇒ Solução ótima (frações):")
            for j, val in enumerate(x, 1):
                print(f"x{j} = {val}")
            print("z* =", z)
            break

        yk = [T[i][enter_col] for i in range(1, m+1)]
        print(f"\n♦ Iteração {it}")
        print(f"  k  (entra) : {var[enter_col]}")
        print(f"  y_k        : {[str(v) for v in yk]}")

        # 2. escolhe linha que sai
        pivot_row, min_ratio = None, None
        for i in range(1, m+1):
            col_val = T[i][enter_col]
            if col_val > 0:
                ratio = T[i][-1] / col_val
                if pivot_row is None or ratio < min_ratio:
                    pivot_row, min_ratio = i, ratio
        if pivot_row is None:
            raise ValueError("Problema ilimitado")

        print(f"  r  (sai)   : {base[pivot_row-1]}")
        print(f"  razão min  : {min_ratio}\n")

        # 3. pivoteamento
        piv = T[pivot_row][enter_col]
        T[pivot_row] = [x / piv for x in T[pivot_row]]
        for i in range(m+1):
            if i == pivot_row:
                continue
            factor = T[i][enter_col]
            T[i] = [x - factor*y for x, y in zip(T[i], T[pivot_row])]

        # 4. atualiza base
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


# ===================== EXEMPLO =====================
if __name__ == "__main__":
  A = [
    [-2, -2, -4, 1, 1, 0, 1, 0],
    [-1, -3, -1, 5, 0, 1, 0, 1],
]

b = [-2, -1]

c = [4, 3, 5, -1, 0, 0, 1110, 1110]

I0 = [6, 7]  # variáveis de folga como base inicial

x, z = simplex_tableau_min_frac(A, b, c, I0)
