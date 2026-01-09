import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rv_continuous
from scipy.integrate import quad

# === 1. СОЗДАНИЕ КЛАССА РАСПРЕДЕЛЕНИЯ ===
class MyDistribution(rv_continuous):
    def _pdf(self, x):
        # f(x) = 3/4 * (1 - x^2) на интервале [-1, 1]
        # Эта функция не является стандартной (как нормальное или экспоненциальное)
        return np.where((x >= -1) & (x <= 1), 0.75 * (1 - x**2), 0)

# Инициализируем объект распределения на отрезке [-1, 1]
my_rv = MyDistribution(a=-1, b=1, name='CustomParabolic')

# === 2. ПРОВЕРКА И ГЕНЕРАЦИЯ ДАННЫХ ===
norm_cond, _ = quad(my_rv.pdf, -1, 1)
size = 2000  # Размер выборки для графиков
sample = my_rv.rvs(size=size)

# === 3. ВИЗУАЛИЗАЦИЯ (Как в примере) ===
x_range = np.linspace(-1.3, 1.3, 500)
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Левый график: Функция распределения (CDF)
ax[0].hist(sample, bins=50, density=True, cumulative=True,
           alpha=0.6, color='steelblue', label='Эмпирическая CDF')
ax[0].plot(x_range, my_rv.cdf(x_range), 'r-', lw=2.5, label='Теоретическая CDF')
ax[0].set_title('Функция распределения F(x)', fontsize=14)
ax[0].grid(True, alpha=0.3)
ax[0].legend()

# Правый график: Плотность вероятности (PDF)
ax[1].hist(sample, bins=50, density=True, alpha=0.6,
           color='steelblue', label='Гистограмма выборки')
ax[1].plot(x_range, my_rv.pdf(x_range), 'r-', lw=2.5, label='Теоретическая PDF')
ax[1].set_title('Плотность вероятности f(x)', fontsize=14)
ax[1].grid(True, alpha=0.3)
ax[1].legend()

plt.tight_layout()
plt.show()

# === 4. РАСЧЕТЫ ПО ЗАДАНИЮ ===

# Вероятность попадания в интервал [a, b]
a_int, b_int = -0.5, 0.5
prob_interval = my_rv.cdf(b_int) - my_rv.cdf(a_int)

# Характеристики
mean = my_rv.mean()
var = my_rv.var()
std = my_rv.std()
skew = my_rv.stats(moments='s')
kurt = my_rv.stats(moments='k')

# Квантили
q = 0.8 # Квантиль уровня 0.8
p_point = 0.05 # 5%-ная точка (квантиль уровня 0.05)

print("-" * 50)
print(f"1. Условие нормировки: {norm_cond:.4f}")
print(f"2. Вероятность P({a_int} < X < {b_int}): {prob_interval:.4f}")
print("-" * 50)
print(f"3. Математическое ожидание (E): {mean:.4f}")
print(f"4. Дисперсия (D): {var:.4f}")
print(f"5. СКО (sigma): {std:.4f}")
print(f"6. Коэффициент асимметрии: {skew:.4f}")
print(f"7. Эксцесс: {kurt:.4f}")
print("-" * 50)
print(f"8. Квантиль уровня q={q}: {my_rv.ppf(q):.4f}")
print(f"9. {p_point*100}%-ная точка: {my_rv.ppf(p_point):.4f}")
print("-" * 50)