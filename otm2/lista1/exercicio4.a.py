import numpy as np
import matplotlib.pyplot as plt

# Valores de x1 e x2
x1_vals = np.linspace(0, 10, 400)
x2_vals = np.linspace(0, 5, 400)

# Definindo as restrições como funções
r1 = (7 - x1_vals) / 3            # x1 + 3x2 <= 7
r2 = (8 - 2 * x1_vals) / 2        # 2x1 + 2x2 <= 8
r3 = 3 - x1_vals                  # x1 + x2 <= 3
r4 = np.full_like(x1_vals, 2)     # x2 <= 2

# Grade para preencher a região viável
X1, X2 = np.meshgrid(x1_vals, x2_vals)
region = (X1 + 3*X2 <= 7) & (2*X1 + 2*X2 <= 8) & (X1 + X2 <= 3) & (X2 <= 2) & (X1 >= 0) & (X2 >= 0)

# Criando o gráfico
fig, ax = plt.subplots(figsize=(8, 6))

# Plot das restrições
ax.plot(x1_vals, r1, label=r'$x_1 + 3x_2 \leq 7$', color='orange')
ax.plot(x1_vals, r2, label=r'$2x_1 + 2x_2 \leq 8$', color='red')
ax.plot(x1_vals, r3, label=r'$x_1 + x_2 \leq 3$', color='purple')
ax.plot(x1_vals, r4, label=r'$x_2 \leq 2$', color='magenta')
ax.axhline(0, color='black')
ax.axvline(0, color='black')

# Preenchendo a região viável
ax.contourf(X1, X2, region, levels=[0.5, 1], colors=["#D3D3D3"])

# Setas indicando o sentido da viabilidade
ax.annotate('', xy=(2.5, (7 - 2.5) / 3 - 0.2), xytext=(2.0, (7 - 2.0) / 3 + 0.2),
            arrowprops=dict(facecolor='orange', arrowstyle='->'))
ax.annotate('', xy=(2.5, (8 - 2*2.5)/2 - 0.2), xytext=(2.0, (8 - 2*2.0)/2 + 0.2),
            arrowprops=dict(facecolor='red', arrowstyle='->'))
ax.annotate('', xy=(2.5, 3 - 2.5 - 0.2), xytext=(2.0, 3 - 2.0 + 0.2),
            arrowprops=dict(facecolor='purple', arrowstyle='->'))
ax.annotate('', xy=(1.5, 1.9), xytext=(1.0, 2.1),
            arrowprops=dict(facecolor='magenta', arrowstyle='->'))

# Destacando o ponto ótimo
ax.plot(3, 0, 'ko')
ax.annotate('Ótimo (3, 0)', (3, 0), textcoords="offset points", xytext=(-30,10), ha='center')

# Estética
ax.set_xlim((0, 5))
ax.set_ylim((0, 5))
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.set_title('Região Viável com Setas (Problema a)')
ax.legend()
ax.grid(True)
plt.show()
