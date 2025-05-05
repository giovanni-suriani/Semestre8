import numpy as np
import matplotlib.pyplot as plt

# Espaço de busca
x1_vals = np.linspace(-6, 1, 500)
x2_vals = np.linspace(-8, 8, 500)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Função objetivo
Z = X1 - 5 * X2

# Restrições com vetores normais (para desenhar setas)
restricoes = [
    (lambda x1, x2: -2*x1 + 3*x2 - 6, '<=', '2x₁ - 3x₂ ≥ -6', np.array([-2, 3])),
    (lambda x1, x2: -4*x1 + 2*x2 + 8, '<=', '-4x₁ + 2x₂ ≤ -8', np.array([-4, 2])),
    (lambda x1, x2: x1, '<=', 'x₁ ≤ 0', np.array([1, 0])),
]

# Região viável
feasible_region = np.ones_like(X1, dtype=bool)
for f, tipo, _, _ in restricoes:
    feasible_region &= f(X1, X2) <= 0

# Plot
plt.figure(figsize=(10, 7))
plt.title('Questão (c) - Região viável com setas e labels', fontsize=16)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.xlim((-6, 1))
plt.ylim((-8, 8))
plt.grid(True)

# Curvas de nível
contours = plt.contour(X1, X2, Z, levels=30, cmap='plasma', alpha=1.0)
plt.clabel(contours, inline=True, fontsize=10, fmt="%.1f", colors='white')

# Setas e labels
for f, _, label, vetor in restricoes:
    cs = plt.contour(X1, X2, f(X1, X2), levels=[0], colors='black', linewidths=2)
    centro_x, centro_y = -2.5, 0
    norm = np.linalg.norm(vetor)
    dx, dy = vetor / norm
    plt.arrow(centro_x, centro_y, dx, dy, head_width=0.25, head_length=0.4, fc='red', ec='red')
    plt.text(centro_x + dx * 1.3, centro_y + dy * 1.3, label, fontsize=9, color='red',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))

# Região viável
plt.contourf(X1, X2, feasible_region, levels=1, colors=['#0059b3'], alpha=0.4)

plt.tight_layout()
plt.show()
