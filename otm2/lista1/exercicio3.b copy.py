import numpy as np
import matplotlib.pyplot as plt

# Espaço de busca
x1_vals = np.linspace(-2, 6, 500)
x2_vals = np.linspace(-2, 6, 500)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Função objetivo
Z = X1 + 3 * X2

# Restrições da questão (b): (função, tipo, label, vetor normal)
restricoes = [
    (lambda x1, x2: -x1 - x2 + 3, '<=', '-x₁ - x₂ ≤ -3', np.array([-1, -1])),
    (lambda x1, x2: -x1 + x2 + 1, '<=', '-x₁ + x₂ ≤ -1', np.array([-1, 1])),
    (lambda x1, x2: x1 + 2*x2 - 4, '<=', 'x₁ + 2x₂ ≤ 4', np.array([1, 2])),
    (lambda x1, x2: -x1, '<=', 'x₁ ≥ 0', np.array([-1, 0])),
    (lambda x1, x2: -x2, '<=', 'x₂ ≥ 0', np.array([0, -1])),
]

# Construir região viável
feasible_region = np.ones_like(X1, dtype=bool)
for f, tipo, _, _ in restricoes:
    if tipo == '<=':
        feasible_region &= f(X1, X2) <= 0
    elif tipo == '>=':
        feasible_region &= f(X1, X2) >= 0

# Plot
plt.figure(figsize=(10, 7))
plt.title('Questão (b) - Região viável com setas e labels', fontsize=16)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.xlim((-2, 6))
plt.ylim((-2, 6))
plt.grid(True)

# Curvas de nível da função objetivo
contours = plt.contour(X1, X2, Z, levels=30, cmap='plasma', alpha=1.0)
plt.clabel(contours, inline=True, fontsize=10, fmt="%.1f", colors='white')

# Fronteiras e vetores normais (setas)
for f, _, label, vetor in restricoes:
    cs = plt.contour(X1, X2, f(X1, X2), levels=[0], colors='black', linewidths=2)
    
    # Origem da seta (centro do gráfico)
    centro_x, centro_y = 2.5, 2.5
    norm = np.linalg.norm(vetor)
    dx, dy = vetor / norm

    # Setas para fora da região viável
    plt.arrow(centro_x, centro_y, dx, dy, head_width=0.15, head_length=0.3, fc='red', ec='red')
    
    # Label da seta
    plt.text(centro_x + dx * 1.1, centro_y + dy * 1.1, label, fontsize=9, color='red',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))

# Região viável
plt.contourf(X1, X2, feasible_region, levels=1, colors=['#0059b3'], alpha=0.4)

plt.xticks(np.arange(-2, 6.5, 0.5))
plt.yticks(np.arange(-2, 6.5, 0.5))
plt.tight_layout()
plt.show()
