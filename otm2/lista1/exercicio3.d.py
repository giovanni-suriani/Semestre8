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
    (lambda x1, x2: x1 - x2 - 2, '<='),         # x1 - x2 <= 2 (redundant but added)
    (lambda x1, x2: -x1 - 5, '<='),             # x1 >= -5 → -x1 - 5 <= 0
    (lambda x1, x2: 2*x1 + x2 - 8, '='),        # 2x1 + x2 = 8
    (lambda x1, x2: x1 + x2 - 10, '<='),        # x1 + x2 <= 10
    
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

plt.tight_layout()
plt.show()
