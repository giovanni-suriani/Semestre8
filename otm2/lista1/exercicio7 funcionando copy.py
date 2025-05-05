from fractions import Fraction

# ---------- utilidades já existentes ----------
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
    """ núcleo (Fase I ou Fase II) com prints """
    it_ = start_it
    print_tableau(T, base, var, 0)

    while it_ < max_iter:
        enter = max((j for j in range(n) if T[0][j] > 0),
                    key=lambda j: T[0][j], default=None)
        if enter is None:
            return T, base, True, it_

        # … resto do seu código inalterado …
        yk = [T[i][enter] for i in range(1, m+1)]
        print(f"\n♦ Iteração {it_}")
        print(f"  k  (entra) : {var[enter]}")
        print(f"  y_k        : {[str(v) for v in yk]}")

        piv_r, best = None, None
        for i in range(1, m+1):
            a = T[i][enter]
            if a > 0:
                r = T[i][-1] / a
                if piv_r is None or r < best:
                    piv_r, best = i, r
        if piv_r is None:
            raise ValueError("Problema ilimitado")

        print(f"  r  (sai)   : {base[piv_r-1]}")
        print(f"  razão min  : {best}\n")

        p = T[piv_r][enter]
        T[piv_r] = [x / p for x in T[piv_r]]
        for i in range(m+1):
            if i == piv_r: continue
            f = T[i][enter]
            T[i] = [x - f*y for x, y in zip(T[i], T[piv_r])]

        base[piv_r-1] = var[enter]
        print_tableau(T, base, var, it_)
        it_ += 1

    raise RuntimeError("Max_iter excedido")
# ------------------------------------------------

# --------- NOVA FUNÇÃO: 1 ou 2 fases ----------
def simplex_min_frac_auto(A, b, c, max_iter=50):
    """
    Resolve PL de minimização:
      - Usa 1 fase se base trivial for viável.
      - Usa 2 fases (artificiais) só quando necessário.
    """
    # --- preparação -------
    A = to_frac_matrix(A)
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]
    m, n0 = len(A), len(A[0])

    # ---- 1. procura base trivial I = {coluna identidade em cada linha} ----
    I0 = []
    for i in range(m):
        piv = None
        for j in range(n0):
            if A[i][j] == 1 and all(A[k][j] == 0 for k in range(m) if k != i):
                piv = j
                break
        if piv is None:
            I0 = None
            break
        I0.append(piv)

    base_viavel = I0 is not None and all(bi >= 0 for bi in b)

    # -------------------- CASO 1: base viável encontrada -------------------
    if base_viavel:
        print("▶ Base trivial viável encontrada – pulando Fase I\n")
        # monta tableau para Fase II
        n = n0
        var = [f"x{j+1}" for j in range(n0)]
        base = [var[j] for j in I0]

        T = [[Fraction(0) for _ in range(n + 1)] for _ in range(m + 1)]
        # linha de custo
        for j in range(n0):
            T[0][j] = -c[j]
        # restrições
        for i in range(m):
            T[i+1][:n0] = A[i]
            T[i+1][-1]  = b[i]

        # corrige custo para base escolhida
        cB = [c[j] for j in I0]
        for j in range(n0):
            T[0][j] += sum(cB[i] * T[i+1][j] for i in range(m))
        T[0][-1] = sum(cB[i] * T[i+1][-1] for i in range(m))

        # roda simplex direto
        T, base, ok, _ = _simplex_core_verbose(T, base, var, m, n, 1, max_iter)
        if not ok:
            raise ValueError("Problema ilimitado")

        # lê solução
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

    # -------------------- CASO 2: precisa Fase I ---------------------------
    print("▶ Base trivial NÃO viável – ativando Fase I (variáveis artificiais)\n")
    n = n0 + m
    var  = [f"x{j+1}" for j in range(n0)] + [f"a{i+1}" for i in range(m)]
    base = [f"a{i+1}" for i in range(m)]

    # tableau Fase I
    T = [[Fraction(0) for _ in range(n + 1)] for _ in range(m + 1)]
    for j in range(n0, n):        # custo das artificiais = +1  (minimização)
        T[0][j] = Fraction(-1)
    for i in range(m):
        # se b negativo já foi tornado positivo
        T[i+1][:n0]    = A[i]
        T[i+1][n0+i]   = 1
        T[i+1][-1]     = b[i]
    # soma linhas B na linha‑custo
    for i in range(1, m+1):
        T[0] = [t + T[i][j] for j, t in enumerate(T[0])]

    # ----- Fase I -----
    T, base, ok, it = _simplex_core_verbose(T, base, var, m, n, 1, max_iter)
    if not ok or T[0][-1] != 0:
        raise ValueError("Problema inviável")

    # remove artificiais
    keep = list(range(n0))
    T  = [[row[j] for j in keep] + [row[-1]] for row in T]
    var = var[:n0]

    # troca básicas artificiais por verdadeiras
    for i in range(m):
        if base[i].startswith('a'):
            row = T[i+1]
            col = next((j for j in range(n0) if row[j] != 0), None)
            if col is None:        # toda linha zero ⇒ redundante
                continue
            piv = row[col]
            T[i+1] = [x / piv for x in T[i+1]]
            for k in range(m+1):
                if k == i+1: continue
                f = T[k][col]
                T[k] = [x - f*y for x, y in zip(T[k], T[i+1])]
            base[i] = var[col]

    # ---- prepara linha‑custo Fase II ----
    T[0][:n0] = [-cj for cj in c]
    T[0][-1]  = 0
    cB = [c[var.index(bv)] for bv in base]
    for j in range(n0):
        T[0][j] += sum(cB[i] * T[i+1][j] for i in range(m))
    T[0][-1] = sum(cB[i] * T[i+1][-1] for i in range(m))

    # ----- Fase II -----
    T, base, ok, _ = _simplex_core_verbose(T, base, var, m, n0, it, max_iter)
    if not ok:
        raise ValueError("Problema ilimitado")

    # solução final
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
# --------------------------------------------------------------------------

# ================== TESTE com problema do usuário ==================
A = [
    [2, 1, 1, 0, 0],   # 2x1 +  x2 + x3 = 8
    [1, 2, 0, 1, 0],   #  x1 + 2x2 + x4 = 7
    [0, 1, 0, 0, 1]    #        x2 + x5 = 3
]
b = [8, 7, 3]
c = [-1, -1, 0, 0, 0]   # min -x1 - x2   (≡ max x1 + x2)

x_opt, z_opt = simplex_min_frac_auto(A, b, c)

A = [[-2, -2, -4,  1, 1, 0],
     [-1, -3, -1,  5, 0, 1]]
b = [-2, -1]
c = [4, 3, 5, -1, 0, 0]

x_opt, z_opt = simplex_min_frac_auto(A, b, c)

