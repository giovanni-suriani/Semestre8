import numpy as np
import matplotlib.pyplot as plt

# Espaço de busca
x1_vals = np.linspace(-6, 1, 500)
x2_vals = np.linspace(-8, 8, 500)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Função objetivo
Z = X1 - 5 * X2

# Restrições convertidas para a forma f(x1,x2) <= 0
restricoes = [
    (lambda x1, x2: -2*x1 + 3*x2 - 6, '<=', '2x₁ - 3x₂ ≥ -6'),
    (lambda x1, x2: -4*x1 + 2*x2 + 8, '<=', '-4x₁ + 2x₂ ≤ -8'),
    (lambda x1, x2: x1, '<=', 'x₁ ≤ 0'),
]

# Construir região viável
feasible_region = np.ones_like(X1, dtype=bool)
for f, tipo, _ in restricoes:
    feasible_region &= f(X1, X2) <= 0

# Plot
plt.figure(figsize=(10, 7))
plt.title('Questão (c) - Região viável com labels nas restrições', fontsize=16)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.xlim((-6, 1))
plt.ylim((-8, 8))
plt.grid(True)

# Curvas de nível da função objetivo
contours = plt.contour(X1, X2, Z, levels=30, cmap='plasma', alpha=1.0)
plt.clabel(contours, inline=True, fontsize=10, fmt="%.1f", colors='white')

# Bordas e labels
for f, _, label in restricoes:
    cs = plt.contour(X1, X2, f(X1, X2), levels=[0], colors='black', linewidths=2)
    p = cs.collections[0].get_paths()[0]
    verts = p.vertices
    idx = len(verts) // 2
    x_label, y_label = verts[idx]
    plt.text(x_label, y_label, label, fontsize=9, color='black',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7))

# Região viável
plt.contourf(X1, X2, feasible_region, levels=1, colors=['#0059b3'], alpha=0.4)

plt.tight_layout()
plt.show()
