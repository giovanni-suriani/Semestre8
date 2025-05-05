from fractions import Fraction

def to_frac_matrix(mat):
    return [[Fraction(x) for x in row] for row in mat]

def print_tableau(T, base, var, it_):
    head = ["  "] + var + ["LD"]
    print(f"\n── Tabela – iteração {it_} ──")
    print(" | ".join(f"{h:>8}" for h in head))
    print("-" * (12*(len(var)+2)))
    for i, row in enumerate(T):
        tag = "z" if i == 0 else base[i-1]
        print(f"{tag:>2} | " + " | ".join(f"{str(x):>8}" for x in row))

def _simplex_core_verbose(T, base, var, m, n, start_it=1, max_iter=50):
    """
    Versão com prints detalhados
    """
    it_ = start_it
    print_tableau(T, base, var, 0)

    while it_ < max_iter:
        enter = max((j for j in range(n) if T[0][j] > 0), 
                    key=lambda j: T[0][j], default=None)
        if enter is None:
            return T, base, True, it_

        yk = [T[i][enter] for i in range(1, m+1)]
        print(f"\n♦ Iteração {it_}")
        print(f"  k  (entra) : {var[enter]}")
        print(f"  y_k        : {[str(v) for v in yk]}")

        pivot, best = None, None
        for i in range(1, m+1):
            a = T[i][enter]
            if a > 0:
                r = T[i][-1] / a
                if pivot is None or r < best:
                    pivot, best = i, r
        if pivot is None:
            raise ValueError("Problema ilimitado")

        print(f"  r  (sai)   : {base[pivot-1]}")
        print(f"  razão min  : {best}\n")

        p = T[pivot][enter]
        T[pivot] = [x / p for x in T[pivot]]
        for i in range(m+1):
            if i == pivot: continue
            f = T[i][enter]
            T[i] = [x - f*y for x, y in zip(T[i], T[pivot])]

        base[pivot-1] = var[enter]
        print_tableau(T, base, var, it_)
        it_ += 1

    raise RuntimeError("Max_iter excedido")

def simplex_two_phase_min_frac_verbose(A, b, c, max_iter=50):
    m, n0 = len(A), len(A[0])
    A = to_frac_matrix(A)
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]

    for i in range(m):
        if b[i] < 0:
            A[i] = [-a for a in A[i]]
            b[i] = -b[i]

    n = n0 + m
    var  = [f"x{j+1}" for j in range(n0)] + [f"a{i+1}" for i in range(m)]
    base = [f"a{i+1}" for i in range(m)]

    T = [[Fraction(0) for _ in range(n+1)] for _ in range(m+1)]
    for j in range(n0, n):
        T[0][j] = -1
    for i in range(m):
        T[i+1][:n0]      = A[i]
        T[i+1][n0 + i]   = 1
        T[i+1][-1]       = b[i]
    for i in range(1, m+1):
        T[0] = [t + T[i][j] for j, t in enumerate(T[0])]

    # Fase I com prints
    T, base, ok, it = _simplex_core_verbose(T, base, var, m, n, 1, max_iter)
    if not ok or T[0][-1] != 0:
        raise ValueError("Problema inviável")

    keep = list(range(n0))
    T  = [[row[j] for j in keep] + [row[-1]] for row in T]
    var = var[:n0]

    for i in range(m):
        if base[i].startswith('a'):
            row = T[i+1]
            col = next((j for j in range(n0) if row[j] != 0), None)
            if col is None:
                continue
            p = row[col]
            T[i+1] = [x / p for x in T[i+1]]
            for k in range(m+1):
                if k == i+1: continue
                f = T[k][col]
                T[k] = [x - f*y for x, y in zip(T[k], T[i+1])]
            base[i] = var[col]

    T[0][:n0] = [-cj for cj in c]
    T[0][-1]  = 0
    cB = [c[var.index(bv)] for bv in base]
    for j in range(n0):
        T[0][j] += sum(cB[i] * T[i+1][j] for i in range(m))
    T[0][-1] = sum(cB[i] * T[i+1][-1] for i in range(m))

    # Fase II com prints
    T, base, ok, _ = _simplex_core_verbose(T, base, var, m, n0, it, max_iter)
    if not ok:
        raise ValueError("Problema ilimitado")

    x = [Fraction(0) for _ in range(n0)]
    for i, bv in enumerate(base):
        idx = var.index(bv)
        x[idx] = T[i+1][-1]
    z = T[0][-1]
    print("\n*** ÓTIMO ALCANÇADO ***")
    print("\n⇒ Solução ótima (frações):")
    for j, val in enumerate(x, 1):
        print(f"x{j} = {val}")
    print("z* =", z)
    return x, z

# Executar com os dados do problema
A = [[-2, -2, -4,  1, 1, 0],
     [-1, -3, -1,  5, 0, 1]]
b = [-2, -1]
c = [4, 3, 5, -1, 0, 0]

x_opt, z_opt = simplex_two_phase_min_frac_verbose(A, b, c)
