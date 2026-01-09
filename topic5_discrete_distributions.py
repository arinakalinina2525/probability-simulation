import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import binom, poisson, geom, hypergeom

# 1. НАСТРОЙКИ И ДАННЫЕ
plt.style.use('seaborn-v0_8-darkgrid')
n_shots, lam, p_g, N, K, n_h = 10, 4, 0.4, 12, 4, 5

# Словарь со всеми распределениями и их параметрами
dist_info = {
    'Биномиальное': (binom(n_shots, 0.3), np.arange(n_shots + 1), 'blue'),
    'Пуассона': (poisson(lam), np.arange(15), 'green'),
    'Геометрическое': (geom(p_g), np.arange(10), 'orange'),  # (Scipy geom = попытки, мы вычтем 1 для неудач)
    'Гипергеом.': (hypergeom(N, K, n_h), np.arange(min(K, n_h) + 1), 'purple')
}

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
summary = []

# 2. ЕДИНЫЙ ЦИКЛ ОБРАБОТКИ
for (name, (dist, x_range, color)), ax in zip(dist_info.items(), axes.flatten()):
    # Корректировка для геометрического (число промахов, а не номер попытки)
    if name == 'Геометрическое':
        pmf = dist.pmf(x_range + 1)
        mean, var = dist.mean() - 1, dist.var()
    else:
        pmf = dist.pmf(x_range)
        mean, var = dist.mean(), dist.var()

    mode = x_range[np.argmax(pmf)]

    # Визуализация
    ax.bar(x_range, pmf, color=color, alpha=0.6, edgecolor='black', label='PMF')
    ax.step(x_range, pmf, where='mid', color='red', alpha=0.5)
    ax.set_title(f'{name}\nE[X]={mean:.2f}, D[X]={var:.2f}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Сбор данных для итоговой таблицы
    summary.append([name, f"{mean:.3f}", f"{var:.3f}", mode, f"0-{x_range[-1]}"])

# 3. ТАБЛИЦА И ВЫВОД
comparison_df = pd.DataFrame(summary, columns=['Тип', 'M[X]', 'D[X]', 'Mo[X]', 'Диапазон'])
print("\nСРАВНИТЕЛЬНАЯ ТАБЛИЦА:")
print(comparison_df.to_string(index=False))

plt.suptitle('АНАЛИЗ ДИСКРЕТНЫХ РАСПРЕДЕЛЕНИЙ', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()