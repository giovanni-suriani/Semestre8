import numpy as np
import matplotlib.pyplot as plt

# Espaço de busca
x1_vals = np.linspace(-6, 10, 500)
x2_vals = np.linspace(-2, 12, 500)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Função objetivo
Z = 3 * X1 + 2 * X2

# Restrições contínuas
restricoes = [
    (lambda x1, x2: x1 - x2 - 1, '<='),         # x1 - x2 <= 1
    (lambda x1, x2: x1 - x2 - 2, '<='),         # x1 - x2 <= 2
    (lambda x1, x2: -x1 - 5, '<='),             # x1 >= -5 → -x1 - 5 <= 0
    (lambda x1, x2: 2*x1 + x2 - 8, '='),        # 2x1 + x2 = 8
    (lambda x1, x2: x1 + x2 - 10, '<='),        # x1 + x2 <= 10
    (lambda x1, x2: x1 + 2*x2 - 12, '<='),      # x1 + 2x2 <= 12
    (lambda x1, x2: x2 - 10, '<='),             # x2 <= 10
    (lambda x1, x2: -x2, '<=')                  # x2 >= 0 → -x2 <= 0
]

# Construir a região viável
feasible_region = np.ones_like(X1, dtype=bool)
for f, sentido in restricoes:
    if sentido == '<=':
        feasible_region &= f(X1, X2) <= 0
    elif sentido == '>=':
        feasible_region &= f(X1, X2) >= 0
    elif sentido == '=':
        feasible_region &= np.isclose(f(X1, X2), 0, atol=1e-2)

# Plot
plt.figure(figsize=(10, 7))
plt.title('Região viável e função objetivo (d)', fontsize=16)
plt.xlabel('$x_1$', fontsize=14)
plt.ylabel('$x_2$', fontsize=14)
plt.xlim((-6, 10))
plt.ylim((-2, 12))
plt.grid(True)

# Curvas de nível da função objetivo
contours = plt.contour(X1, X2, Z, levels=30, cmap='plasma', alpha=1.0)
plt.clabel(contours, inline=True, fontsize=10, fmt="%.1f", colors='white')

# Fronteiras das restrições
for f, tipo in restricoes:
    level = 0 if tipo != '=' else [0]
    plt.contour(X1, X2, f(X1, X2), levels=level, colors='black', linewidths=2)

# Região viável preenchida
plt.contourf(X1, X2, feasible_region, levels=1, colors=['#0059b3'], alpha=0.5)

# Marcar os ticks de 0.5 em 0.5
plt.xticks(np.arange(-6, 10.5, 0.5))
plt.yticks(np.arange(-2, 12.5, 0.5))

# ➤ Adicionar setas indicando a direção da região viável
# ➤ Adicionar setas indicando a direção da região viável
# ➤ Adicionar setas indicando a direção da região viável
# ➤ Adicionar setas com labels a partir do centro do gráfico
center_x, center_y = 2, 5  # ponto comum de origem

# Expressões correspondentes às restrições para rótulo
labels = [
    'x₁ − x₂ ≤ 1',
    'x₁ − x₂ ≤ 2',
    'x₁ ≥ −5',
    '2x₁ + x₂ = 8',
    'x₁ + x₂ ≤ 10',
    'x₁ + 2x₂ ≤ 12',
    'x₂ ≤ 10',
    'x₂ ≥ 0'
]

for (f, tipo), label in zip(restricoes, labels):
    if tipo == '=':
        continue  # não desenhamos seta para igualdade

    delta = 0.01
    x0, y0 = center_x, center_y

    # Gradiente numérico
    df_dx1 = (f(x0 + delta, y0) - f(x0 - delta, y0)) / (2 * delta)
    df_dx2 = (f(x0, y0 + delta) - f(x0, y0 - delta)) / (2 * delta)
    grad = np.array([df_dx1, df_dx2])

    if np.linalg.norm(grad) == 0:
        continue  # pular plano nulo

    direction = -grad / np.linalg.norm(grad)

    # Desenhar seta
    plt.arrow(x0, y0, direction[0]*1.5, direction[1]*1.5,
              head_width=0.3, head_length=0.3, fc='lime', ec='lime')

    # Adicionar label no final da seta
    label_x = x0 + direction[0]*1.8
    label_y = y0 + direction[1]*1.8
    plt.text(label_x, label_y, label, fontsize=10, color='white',
             ha='center', va='center', bbox=dict(facecolor='black', edgecolor='none', alpha=0.7))



plt.tight_layout()
plt.show()
