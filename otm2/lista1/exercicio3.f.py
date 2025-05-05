import numpy as np
import matplotlib.pyplot as plt

# Espaço de busca (x2 ≤ 0)
x1_vals = np.linspace(-1, 10, 500)
x2_vals = np.linspace(-10, 1, 500)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Função objetivo
Z = 5 * X1 + 6 * X2

# Restrições com expressões para rótulo
restricoes = [
    (lambda x1, x2: 2*x1 + 3*x2 - 18, '<=', '2x₁ + 3x₂ ≤ 18'),
    (lambda x1, x2: 2*x1 + x2 - 12, '<=', '2x₁ + x₂ ≤ 12'),
    (lambda x1, x2: 3*x1 + 3*x2 - 24, '<=', '3x₁ + 3x₂ ≤ 24'),
    (lambda x1, x2: -x1, '<=', 'x₁ ≥ 0'),
    (lambda x1, x2: x2, '<=', 'x₂ ≤ 0'),
]

# Construir região viável
feasible_region = np.ones_like(X1, dtype=bool)
for f, tipo, _ in restricoes:
    if tipo == '<=':
        feasible_region &= f(X1, X2) <= 0
    elif tipo == '>=':
        feasible_region &= f(X1, X2) >= 0

# Plot
plt.figure(figsize=(10, 7))
plt.title('Região viável com labels nas restrições', fontsize=16)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.xlim((-1, 10))
plt.ylim((-10, 1))
plt.grid(True)

# Curvas de nível da função objetivo
contours = plt.contour(X1, X2, Z, levels=30, cmap='plasma', alpha=1.0)
plt.clabel(contours, inline=True, fontsize=10, fmt="%.1f", colors='white')

# Fronteiras das restrições e labels
for f, _, label in restricoes:
    cs = plt.contour(X1, X2, f(X1, X2), levels=[0], colors='black', linewidths=2)
    p = cs.collections[0].get_paths()[0]
    x_label, y_label = p.vertices[len(p.vertices)//2]
    plt.text(x_label, y_label, label, fontsize=9, color='black',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7))

# Região viável
plt.contourf(X1, X2, feasible_region, levels=1, colors=['#0059b3'], alpha=0.4)

plt.xticks(np.arange(-1, 10, 0.5))
plt.yticks(np.arange(-10, 1, 0.5))

plt.tight_layout()
plt.show()
