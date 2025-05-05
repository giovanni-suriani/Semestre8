import numpy as np
import matplotlib.pyplot as plt

# Intervalo de valores para x1 e x2
x1_vals = np.linspace(0, 10, 400)
x2_vals = np.linspace(0, 10, 400)

# Restrições resolvidas isolando x2
r1 = (18 - 2 * x1_vals) / 3        # 2x1 + 3x2 <= 18
r2 = (12 - 2 * x1_vals)            # 2x1 + x2 <= 12
r3 = (24 - 3 * x1_vals) / 3        # 3x1 + 3x2 <= 24

# Malha para verificar região viável
X1, X2 = np.meshgrid(x1_vals, x2_vals)
region = (2*X1 + 3*X2 <= 18) & (2*X1 + X2 <= 12) & (3*X1 + 3*X2 <= 24) & (X1 >= 0) & (X2 >= 0)

# Criar gráfico
fig, ax = plt.subplots(figsize=(8, 6))

# Plotar as retas das restrições
ax.plot(x1_vals, r1, label=r'$2x_1 + 3x_2 \leq 18$', color='orange')
ax.plot(x1_vals, r2, label=r'$2x_1 + x_2 \leq 12$', color='blue')
ax.plot(x1_vals, r3, label=r'$3x_1 + 3x_2 \leq 24$', color='green')

# Eixos coordenados
ax.axhline(0, color='black')
ax.axvline(0, color='black')

# Região viável preenchida
ax.contourf(X1, X2, region, levels=[0.5, 1], colors=["#D3D3D3"])

# Labels nas bordas das retas
ax.text(2, (18 - 2*2)/3 + 0.3, r'$2x_1 + 3x_2 \leq 18$', color='orange')
ax.text(2, (12 - 2*2) + 0.3, r'$2x_1 + x_2 \leq 12$', color='blue')
ax.text(2, (24 - 3*2)/3 + 0.3, r'$3x_1 + 3x_2 \leq 24$', color='green')

# Estética do gráfico
ax.set_xlim((0, 8))
ax.set_ylim((0, 8))
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.set_title('Região Viável com Labels (Problema b)')
ax.legend()
ax.grid(True)

# Mostrar o gráfico
plt.show()
