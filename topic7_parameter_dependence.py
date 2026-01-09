import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import lognorm

# === 1. ИССЛЕДОВАНИЕ ЗАВИСИМОСТИ ПЛОТНОСТИ ОТ ПАРАМЕТРА (SHAPE) ===
x = np.linspace(0, 5, 500)
sigmas = [0.25, 0.5, 1.0] # Параметры формы (sigma)
mu = 0 # Зафиксируем среднее логарифма

plt.figure(figsize=(12, 6))

for s in sigmas:
    # В scipy.stats.lognorm: s - параметр формы, scale = exp(mu)
    pdf = lognorm.pdf(x, s, scale=np.exp(mu))
    plt.plot(x, pdf, label=f'sigma (shape) = {s}')

plt.title('Изменение плотности логнормального распределения при разных $\sigma$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# === 2. ПРОВЕРКА ФОРМУЛ ХАРАКТЕРИСТИК ДЛЯ СГЕНЕРИРОВАННЫХ ДАННЫХ ===

# Параметры для эксперимента
s_exp = 0.5
mu_exp = 0
scale_exp = np.exp(mu_exp)
n_samples = 10000

# Генерация данных
data = lognorm.rvs(s_exp, scale=scale_exp, size=n_samples, random_state=42)

# Теоретические расчеты по формулам
theoretical_mean = np.exp(mu_exp + (s_exp**2)/2)
theoretical_var = (np.exp(s_exp**2) - 1) * np.exp(2*mu_exp + s_exp**2)

# Эмпирические (статистические) значения
empirical_mean = np.mean(data)
empirical_var = np.var(data)

# === ВЫВОД РЕЗУЛЬТАТОВ ===
print("-" * 50)
print(f"ПАРАМЕТРЫ: sigma = {s_exp}, mu = {mu_exp}")
print("-" * 50)
print(f"Математическое ожидание (Теория): {theoretical_mean:.4f}")
print(f"Математическое ожидание (Эмпирика): {empirical_mean:.4f}")
print(f"Разница: {abs(theoretical_mean - empirical_mean):.4f}")
print("-" * 50)
print(f"Дисперсия (Теория): {theoretical_var:.4f}")
print(f"Дисперсия (Эмпирика): {empirical_var:.4f}")
print(f"Разница: {abs(theoretical_var - empirical_var):.4f}")
print("-" * 50)

# Визуализация сгенерированных данных
plt.figure(figsize=(10, 5))
sns.histplot(data, bins=50, kde=True, color='green', stat="density", alpha=0.4)
plt.axvline(empirical_mean, color='red', linestyle='--', label=f'E(X) = {empirical_mean:.2f}')
plt.title(f'Гистограмма сгенерированных данных ($N={n_samples}$)')
plt.legend()
plt.show()