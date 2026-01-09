import numpy as np
import matplotlib.pyplot as plt

# 1. ПАРАМЕТРЫ И ТЕОРЕТИЧЕСКИЙ РАСЧЕТ
side = 2.0
area_total = side**2
radii = [0.3, 0.7, 1.0] # Красный, Синий, Желтый
colors = ['red', 'blue', 'yellow', 'gray']
labels = ['Красный', 'Синий', 'Желтый', 'Белый']

# Теоретические площади и вероятности
areas_theory = [np.pi * radii[0]**2] # Первый круг
areas_theory.append(np.pi * radii[1]**2 - np.pi * radii[0]**2) # Второе кольцо
areas_theory.append(np.pi * radii[2]**2 - np.pi * radii[1]**2) # Третье кольцо
areas_theory.append(area_total - np.pi * radii[2]**2)        # Остаток
p_theory = [a / area_total for a in areas_theory]

# 2. МОДЕЛИРОВАНИЕ МОНТЕ-КАРЛО
n = 50000
x = np.random.uniform(0, side, n)
y = np.random.uniform(0, side, n)
dist = np.sqrt((x - side/2)**2 + (y - side/2)**2)

# Определение зон
zones = [dist <= radii[0],
         (dist > radii[0]) & (dist <= radii[1]),
         (dist > radii[1]) & (dist <= radii[2]),
         dist > radii[2]]
p_sim = [np.sum(z) / n for z in zones]

# 3. ВЫВОД РЕЗУЛЬТАТОВ В ТАБЛИЦУ
print(f"{'Зона':<10} | {'Теория':<10} | {'Модель':<10} | {'Ошибка':<10}")
print("-" * 50)
for i in range(4):
    print(f"{labels[i]:<10} | {p_theory[i]:.4f}     | {p_sim[i]:.4f}     | {abs(p_theory[i]-p_sim[i]):.6f}")

# 4. ВИЗУАЛИЗАЦИЯ
plt.figure(figsize=(10, 8))
plt.gca().set_aspect('equal')

# Отрисовка подмножества точек (2000 для скорости)
for i, zone_mask in enumerate(zones):
    plt.scatter(x[:2000][zone_mask[:2000]], y[:2000][zone_mask[:2000]],
                c=colors[i], s=10, label=f"{labels[i]} ({p_sim[i]*100:.1f}%)")

# Отрисовка контуров мишени
for r in radii:
    circle = plt.Circle((side/2, side/2), r, color='black', fill=False, linestyle='--')
    plt.gca().add_patch(circle)

plt.title(f'Моделирование геометрической вероятности (N={n})')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()