import numpy as np
import matplotlib.pyplot as plt

# Espaço de busca
x1_vals = np.linspace(-1, 10, 500)
x2_vals = np.linspace(-10, 1, 500)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Função objetivo
Z = 5 * X1 + 6 * X2

# Restrições com rótulos
restricoes = [
    (lambda x1, x2: 2*x1 + 3*x2 - 18, '<=', '2x₁ + 3x₂ ≤ 18'),
    (lambda x1, x2: 2*x1 + x2 - 12, '<=', '2x₁ + x₂ ≤ 12'),
    (lambda x1, x2: 3*x1 + 3*x2 - 24, '<=', '3x₁ + 3x₂ ≤ 24'),
    (lambda x1, x2: -x1, '<=', 'x₁ ≥ 0'),
    (lambda x1, x2: x2, '<=', 'x₂ ≤ 0'),
]

# Região viável
feasible_region = np.ones_like(X1, dtype=bool)
for f, tipo, _ in restricoes:
    if tipo == '<=':
        feasible_region &= f(X1, X2) <= 0
    elif tipo == '>=':
        feasible_region &= f(X1, X2) >= 0

# Plot
plt.figure(figsize=(10, 7))
plt.title('Região viável e setas de direção das restrições (e)', fontsize=15)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.xlim((-1, 10))
plt.ylim((-10, 1))
plt.grid(True)

# Curvas da função objetivo
contours = plt.contour(X1, X2, Z, levels=30, cmap='plasma', alpha=1.0)
plt.clabel(contours, inline=True, fontsize=10, fmt="%.1f", colors='white')

# Fronteiras das restrições
for f, _, _ in restricoes:
    plt.contour(X1, X2, f(X1, X2), levels=[0], colors='black', linewidths=2)

# Região viável preenchida
plt.contourf(X1, X2, feasible_region, levels=1, colors=['#0059b3'], alpha=0.5)

# Desenhar setas de direção viável
center_x, center_y = 4, -5  # ponto de origem comum
for f, tipo, label in restricoes:
    if tipo == '=':
        continue  # igualdade não tem lado viável
    delta = 0.01
    df_dx1 = (f(center_x + delta, center_y) - f(center_x - delta, center_y)) / (2 * delta)
    df_dx2 = (f(center_x, center_y + delta) - f(center_x, center_y - delta)) / (2 * delta)
    grad = np.array([df_dx1, df_dx2])
    if np.linalg.norm(grad) == 0:
        continue
    direction = -grad / np.linalg.norm(grad)

    # Desenhar seta
    plt.arrow(center_x, center_y, direction[0]*2, direction[1]*2,
              head_width=0.3, head_length=0.3, fc='lime', ec='lime')

    # Adicionar label da inequação no final da seta
    label_x = center_x + direction[0]*2.5
    label_y = center_y + direction[1]*2.5
    plt.text(label_x, label_y, label, fontsize=9, color='white',
             ha='center', va='center', bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.3'))

plt.tight_layout()
plt.show()
