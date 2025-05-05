from fractions import Fraction

# ----------------------------------------------------------------------
#  Utilitários que você já tinha
# ----------------------------------------------------------------------
def to_frac_matrix(mat):
    return [[Fraction(x) for x in row] for row in mat]

def print_tableau(T, base, var, it_):
    #head = ["  "] + var + ["LD"]
    print(f"\n── Tabela – iteração {it_} ──")
    print(f"{'':>2} | " + " | ".join(f"{h:>8}" for h in var + ['LD']))
    print("-" * (12 * (len(var) + 2)))
    for i, row in enumerate(T):
        tag = "z" if i == 0 else base[i - 1]
        print(f"{tag:>2} | " + " | ".join(f"{str(x):>8}" for x in row))

def _simplex_core_verbose(T, base, var, m, n, start_it=1, max_iter=50):
    """
    Núcleo do simplex (mesmo que o seu), com prints detalhados
    """
    it_ = start_it
    print_tableau(T, base, var, 0)

    while it_ < max_iter:
        enter = max((j for j in range(n) if T[0][j] > 0),
                    key=lambda j: T[0][j], default=None)
        if enter is None:
            return T, base, True, it_

        yk = [T[i][enter] for i in range(1, m + 1)]
        print(f"\n♦ Iteração {it_}")
        print(f"  k  (entra) : {var[enter]}")
        print( "  x_B        :", end="")
        for i in range(1, m + 1):
            var_name = base[i - 1]
            value = T[i][-1]
            print(f" {value},",end="")
        print("")
        print(f"  y_k        : {[str(v) for v in yk]}")

        pivot, best, r_conj = None, None, []
        for i in range(1, m + 1):
            a = T[i][enter]
            if a > 0:
                r = T[i][-1] / a
                r_obj = (T[i][-1], a)
                r_conj.append(r_obj)
                if pivot is None or r < best:
                    pivot, best = i, r
        if pivot is None:
            raise ValueError("Problema ilimitado")

        print(f"  r  (sai)   : {base[pivot - 1]}, com o valor {best}",end=" ")
        print("do conjunto r_conj:", end=" ")
        for i, r in enumerate(r_conj):
            print(f" r[{i}] = {r[0]}/{r[1]}", end=" ")
        print(f"  razão min  : {best}\n")

        # pivoteia
        p = T[pivot][enter]
        T[pivot] = [x / p for x in T[pivot]]
        for i in range(m + 1):
            if i == pivot:
                continue
            f = T[i][enter]
            T[i] = [x - f * y for x, y in zip(T[i], T[pivot])]

        base[pivot - 1] = var[enter]
        print_tableau(T, base, var, it_)
        it_ += 1

    raise RuntimeError("max_iter excedido")


# ----------------------------------------------------------------------
#  Funções novas para detectar base “trivial” (colunas‑identidade)
# ----------------------------------------------------------------------
def _identity_basis_cols(A):
    """
    Procura em A colunas cujo padrão seja [0,0,...,1,...,0].
    Retorna lista de índices — um para cada linha — se possível; caso
    contrário devolve lista vazia.
    """
    m, n = len(A), len(A[0])
    chosen = [-1] * m            # coluna escolhida para cada linha
    for j in range(n):
        ones = [i for i in range(m) if A[i][j] == 1]
        if len(ones) == 1 and all(A[i][j] == 0 for i in range(m) if i != ones[0]):
            i = ones[0]
            if chosen[i] == -1:   # ainda não há base para essa linha
                chosen[i] = j
    return [j for j in chosen if j != -1]   # só as que achou


# ----------------------------------------------------------------------
#  Algoritmo principal “auto‑duas‑fases”
# ----------------------------------------------------------------------
def simplex_min_frac_auto_verbose(A, b, c, I0=None, max_iter=50):
    """
    Simplex (minimização) com fallback automático para duas fases.

    - Se `I0` for uma base factível, usa‑se direto.
    - Caso contrário, se A já contém m colunas‑identidade (b >= 0),
      elas viram a base inicial.
    - Caso contrário, adiciona‑se variáveis artificiais apenas nas
      linhas sem coluna‑identidade e executa‑se a Fase I.
    """
    # --- Preparação e sinal de dimensões --------------------------------
    m, n0 = len(A), len(A[0])
    A = to_frac_matrix(A)
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]

    # Garante b >= 0 (multiplica linhas negativas)
    for i in range(m):
        if b[i] < 0:
            A[i] = [-a for a in A[i]]
            b[i] = -b[i]

    # 1) Usuário passou base explícita?
    if I0 is not None:
        if len(I0) != m:
            raise ValueError("I0 deve ter m índices")
        base_cols = I0[:]
    else:
        # 2) Tenta achar base identidade na própria A
        base_cols = _identity_basis_cols(A)

    needs_phase_I = (len(base_cols) != m)   # falta base para alguma linha

    # ------------------------------------------------------------------
    #  *** CASO 1 – não precisa Fase I ***
    # ------------------------------------------------------------------
    if not needs_phase_I:
        var = [f"x{j + 1}" for j in range(n0)]
        base = [var[j] for j in base_cols]

        # monta o tableau (Fase II directa)
        T = [[Fraction(0) for _ in range(n0 + 1)] for _ in range(m + 1)]
        for j in range(n0):
            T[0][j] = -c[j]                # custos com minimização
        for i in range(m):
            T[i + 1][:n0] = A[i]
            T[i + 1][-1] = b[i]

        # corrige a linha z porque já temos base
        cB = [c[j] for j in base_cols]
        for j in range(n0):
            T[0][j] += sum(cB[i] * T[i + 1][j] for i in range(m))
        T[0][-1] = sum(cB[i] * b[i] for i in range(m))

        # roda simplex “uma fase” já óptimo
        T, base, ok, _ = _simplex_core_verbose(T, base, var, m, n0, 1, max_iter)
        if not ok:
            raise ValueError("Problema ilimitado")

    # ------------------------------------------------------------------
    #  *** CASO 2 – precisa Fase I (algumas linhas sem base) ***
    # ------------------------------------------------------------------
    else:
        print("▶ Base trivial inviável – usando Fase I\n")
        # Flags de quais linhas já têm base “natural”
        has_base = [False] * m
        for col in base_cols:
            row = next(i for i in range(m) if A[i][col] == 1)
            has_base[row] = True

        # Cria variáveis artificiais só nas linhas sem base
        art_map = {}       # row -> índice de variável artificial
        for i, ok in enumerate(has_base):
            if not ok:
                art_map[i] = len(art_map)      # ordem das artificiais

        n = n0 + len(art_map)                  # total de variáveis
        var = [f"x{j + 1}" for j in range(n0)] + \
              [f"a{k + 1}" for k in range(len(art_map))]
        base = []

        # Tableau inicial
        T = [[Fraction(0) for _ in range(n + 1)] for _ in range(m + 1)]

        # Linha‑custo da Fase I: -1 para cada artificial
        for k in range(len(art_map)):
            T[0][n0 + k] = -1

        for i in range(m):
            # Parte das variáveis originais
            T[i + 1][:n0] = A[i]
            # Se esta linha tem artificial:
            if i in art_map:
                idx = n0 + art_map[i]
                T[i + 1][idx] = 1
                base.append(var[idx])
            else:
                # pega a coluna‑identidade indicada em base_cols
                j = base_cols.pop(0)
                base.append(var[j])
            T[i + 1][-1] = b[i]

        # Corrige a linha‑custo para reflectir base inicial (somatório das linhas básicas)
        for i in range(1, m + 1):
            if base[i - 1].startswith("a"):
                T[0] = [t + T[i][j] for j, t in enumerate(T[0])]

        # ---------- Fase I ----------
        T, base, ok, it = _simplex_core_verbose(T, base, var, m, n, 1, max_iter)
        if not ok or T[0][-1] != 0:
            raise ValueError("Problema inviável")

        # Remove colunas artificiais
        keep = list(range(n0))                 # só as originais
        T = [[row[j] for j in keep] + [row[-1]] for row in T]
        var = var[:n0]

        # Se ainda restar artificial na base, pivoteia para retirar
        for i in range(m):
            if base[i].startswith('a'):
                row = T[i + 1]
                col = next((j for j in range(n0) if row[j] != 0), None)
                if col is None:        # linha zero ⇒ restrição redundante
                    continue
                p = row[col]
                T[i + 1] = [x / p for x in T[i + 1]]
                for k in range(m + 1):
                    if k == i + 1:
                        continue
                    f = T[k][col]
                    T[k] = [x - f * y for x, y in zip(T[k], T[i + 1])]
                base[i] = var[col]

        # ---------- Fase II ----------
        # custos reais
        T[0][:n0] = [-cj for cj in c]
        T[0][-1] = 0
        cB = [c[var.index(bv)] for bv in base]
        for j in range(n0):
            T[0][j] += sum(cB[i] * T[i + 1][j] for i in range(m))
        T[0][-1] = sum(cB[i] * T[i + 1][-1] for i in range(m))

        T, base, ok, _ = _simplex_core_verbose(T, base, var, m, n0, it, max_iter)
        if not ok:
            raise ValueError("Problema ilimitado")

    # ------------------------------------------------------------------
    #  *** Recupera solução óptima ***
    # ------------------------------------------------------------------
    x = [Fraction(0) for _ in range(n0)]
    for i, bv in enumerate(base):
        idx = var.index(bv)
        x[idx] = T[i + 1][-1]
    z = T[0][-1]

    print("\n*** ÓTIMO ALCANÇADO ***")
    for j, val in enumerate(x, 1):
        print(f"x{j} = {val}")
    print(f"z*  = {z}")
    return x, z


# ----------------------------------------------------------------------
#  EXEMPLOS RÁPIDOS
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # (a) Problema que já possui base identidade (pula Fase I)
    A1 = [[1, 2, 1, 0],
          [2, 1, 0, 1]]
    b1 = [8, 7]
    c1 = [5, 4, 0, 0]
    #print("\n=== Exemplo sem Fase I ===")
    simplex_min_frac_auto_verbose(A1, b1, c1)

    # (b) Mesmo exemplo que você mandou (precisa Fase I)
    A2 = [[-2, -2, -4,  1, 1, 0],
          [-1, -3, -1,  5, 0, 1]]
    b2 = [-2, -1]
    c2 = [4, 3, 5, -1, 0, 0]
    I0 = [4,5]
    print("\n=== Exemplo com Fase I ===")
    simplex_min_frac_auto_verbose(A2, b2, c2)
    
    A = [
        [2, 1, 1, 0, 0],
        [1, 2, 0, 1, 0],
        [0, 1, 0, 0, 1]
    ]
    b = [8, 7, 3]
    c = [-1, -1, 0, 0, 0]
    
    
    #simplex_min_frac_auto_verbose(A, b, c)
    
    A = [
    [ 1,  1, -1, 0 ,0 ],   # x1 + x2 -x3 = 2
    [-1,  1, 0, -1, 0 ],   # -x1 + x2  - x4= 1
    [ 0,  1, 0, 0, 1]    #  x2 +x5     = 3
]

    # Vetor b (termos constantes)
    b = [2, 1, 3]

    # Vetor c (função-objetivo: max z = -x1 + 2x2)
    c = [-1, 2, 0, 0, 0]
    #simplex_min_frac_auto_verbose(A, b, c)
    
    """  A = [
        [2, 1, 1, 0, 0],
        [1, 2, 0, 1, 0],
        [0, 1, 0, 0, 1]
    ]
    b = [8, 7, 3]
    c = [-1, -1, 0, 0, 0]

    I0 = [2, 3, 4]  # base explícita: x3, x4, x5
    x_opt, z_opt = simplex_min_frac_auto_verbose(A, b, c, I0) """



