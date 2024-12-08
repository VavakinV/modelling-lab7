import matplotlib.pyplot as plt
import numpy as np

x1 = np.linspace(0, 15, 400)

# Граничные прямые
y1 = (2/5) * x1 + 2

y2 = -4/5 * x1 + 8

y3 = -1/5 * x1 + 1


plt.figure(figsize=(10, 8))

# Графики ограничений
plt.plot(x1, y1, label=r"$2x_1 - 5x_2 \geq -10$", color='blue')
plt.plot(x1, y2, label=r"$4x_1 + 5x_2 \leq 40$", color='green')
plt.plot(x1, y3, label=r"$x_1 + 5x_2 \geq 5$", color='red')

plt.fill_between(x1, np.maximum(0, y3), np.minimum(y1, y2), where=(np.minimum(y1, y2) >= np.maximum(0, y3)), color='gray', alpha=0.3, label="ОДР")

# Линейная форма z(x) = x1 + 2x2 -> max/min
z = (lambda x1: (10 - x1) / 2) 
plt.plot(x1, z(x1), label=r"$z = x_1 + 2x_2$", linestyle='--', color='orange')

plt.xlim(0, 10)
plt.ylim(0, 10)

plt.xlabel(r"$x_1$")
plt.ylabel(r"$x_2$")
plt.title("Решение задачи линейного программирования графическим методом")
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()

plt.show()

# Экстремальные точки полученного многоугольника:
# (0; 1) => z = 2
# (0; 2) => z = 4
# (5; 4) => z = 13
# (5; 0) => z = 5
# (10; 0) => z = 10
# Откуда:
# zmax = 13
# zmin = 2