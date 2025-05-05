import numpy as np
import matplotlib.pyplot as plt


def plot_feasible_region(constraints,
                         x1_range=(0, 10),
                         x2_range=(0, 10),
                         resolution=400,
                         fill_region=True,
                         show_labels=True):
    """
    Desenha a região viável para um sistema de inequações lineares em x1 e x2.

    Parameters
    ----------
    constraints : list[dict]
        Cada dicionário descreve uma desigualdade do tipo
            a1 * x1 + a2 * x2  op  b
        Campos obrigatórios:
            'a1', 'a2', 'b' : coeficientes numéricos
            'op'            : '<=' ou '>='
        Campos opcionais:
            'color'         : cor da reta
            'label'         : texto exibido no gráfico
    x1_range, x2_range : tuple(float, float)
        Limites dos eixos x1 e x2.
    resolution : int
        Número de pontos da malha.
    fill_region : bool
        Se True, preenche a região viável.
    show_labels : bool
        Se True, escreve os rótulos das restrições.
    """

    # Geração da malha
    x1_vals = np.linspace(*x1_range, resolution)
    x2_vals = np.linspace(*x2_range, resolution)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    feasible = np.ones_like(X1, dtype=bool)

    # Setup gráfico
    fig, ax = plt.subplots(figsize=(8, 6))
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for idx, c in enumerate(constraints):
        a1, a2, b, op = c['a1'], c['a2'], c['b'], c['op']
        color = c.get('color', default_colors[idx % len(default_colors)])
        label = c.get('label', f'{a1}x₁ + {a2}x₂ {op} {b}')

        # Corrige \le e \ge para matplotlib
        label = label.replace(r'\le', r'\leq').replace(r'\ge', r'\geq')

        # Atualiza região viável
        expr = a1 * X1 + a2 * X2
        if op == '<=':
            feasible &= (expr <= b + 1e-9)
        elif op == '>=':
            feasible &= (expr >= b - 1e-9)
        else:
            raise ValueError("op deve ser '<=' ou '>='")

        # Plota linha de fronteira
        if np.isclose(a2, 0):  # linha vertical
            x_const = b / a1
            ax.axvline(x_const, color=color)
            if show_labels:
                ax.text(x_const + 0.1, 0.05*(x2_range[1]-x2_range[0]),
                        label, color=color, rotation=90, va='bottom')
        else:
            y_line = (b - a1 * x1_vals) / a2
            ax.plot(x1_vals, y_line, color=color)
            if show_labels:
                x_mid = (x1_range[0] + x1_range[1]) / 4
                y_mid = (b - a1 * x_mid) / a2
                ax.text(x_mid, y_mid + 0.3, label, color=color)

    # Condições x1 >= 0, x2 >= 0
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')
    feasible &= (X1 >= 0) & (X2 >= 0)

    if fill_region:
        ax.contourf(X1, X2, feasible, levels=[0.5, 1], colors=['#D3D3D3'])

    # Ajustes finais
    ax.set_xlim(x1_range)
    ax.set_ylim(x2_range)
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.set_title('Região Viável')
    ax.grid(True)
    ax.legend()
    plt.show()


# --- Exemplo de uso corrigido ---
if __name__ == '__main__':
    constraints_example = [
        {'a1': 2, 'a2': 3, 'b': 18, 'op': '<=',
         'color': 'orange', 'label': r'$2x_1 + 3x_2 \leq 18$'},
        {'a1': 2, 'a2': 1, 'b': 12, 'op': '<=',
         'color': 'blue',   'label': r'$2x_1 + x_2 \leq 12$'},
        {'a1': 3, 'a2': 3, 'b': 24, 'op': '<=',
         'color': 'green',  'label': r'$3x_1 + 3x_2 \leq 24$'}
    ]

    plot_feasible_region(constraints_example,
                         x1_range=(0, 8),
                         x2_range=(0, 8))
