import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === ПАРАМЕТРЫ ЭКСПЕРИМЕНТА ===
np.random.seed(42)  # Для воспроизводимости результатов
total_trials = 2000  # Общее число бросков монеты
# Моделируем броски: 1 - Орел (Успех), 0 - Решка
tosses = np.random.choice([0, 1], size=total_trials)

# === ВЫЧИСЛЕНИЕ ЧАСТОТНОЙ ВЕРОЯТНОСТИ ===
# Кумулятивная сумма орлов (1) нарастающим итогом
cumulative_heads = np.cumsum(tosses)
# Номера испытаний: 1, 2, 3, ..., total_trials
trial_numbers = np.arange(1, total_trials + 1)
# Относительная частота (Частотная вероятность) выпадения Орла
frequency_probability = cumulative_heads / trial_numbers

# === КЛАССИЧЕСКАЯ (ТЕОРЕТИЧЕСКАЯ) ВЕРОЯТНОСТЬ ===
# Для правильной монеты: P(Орел) = 1/2 = 0.5
theoretical_prob = 0.5

# === ВИЗУАЛИЗАЦИЯ ===
plt.figure(figsize=(14, 7))

# График сходимости частотной вероятности к классической
plt.subplot(1, 2, 1)  # Создаем первую ячейку для графика (1 строка, 2 столбца, ячейка 1)
plt.plot(trial_numbers, frequency_probability,
         color='blue', alpha=0.7, linewidth=0.8, label='Частотная вероятность P(Орел)')
plt.axhline(y=theoretical_prob, color='red', linestyle='--',
            linewidth=2, label=f'Классическая вероятность = {theoretical_prob}')
plt.title('Стремление частотной вероятности к классической\n(Бросок монеты)', fontsize=14)
plt.xlabel('Число испытаний (бросков)', fontsize=12)
plt.ylabel('Вероятность / Частота', fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.ylim([0.3, 0.7])  # Фиксируем масштаб по оси Y для наглядности

# Гистограмма распределения исходов (для наглядности всего эксперимента)
plt.subplot(1, 2, 2)  # Вторая ячейка для графика
final_counts = np.bincount(tosses)  # Считаем итоговое количество Орлов и Решек
labels = ['Решка (0)', 'Орел (1)']
colors = ['gray', 'gold']
bars = plt.bar(labels, final_counts, color=colors, edgecolor='black')
plt.title(f'Распределение исходов после {total_trials} бросков', fontsize=14)
plt.ylabel('Количество', fontsize=12)
# Подписываем значения на столбцах
for bar, count in zip(bars, final_counts):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{count}\n({count/total_trials*100:.1f}%)',
             ha='center', va='bottom')
plt.ylim([0, max(final_counts) * 1.2])

plt.tight_layout()  # Автоматическая подгонка отступов между графиками
plt.show()

# === ВЫВОД РЕЗУЛЬТАТОВ ===
print("="*60)
print("ЭКСПЕРИМЕНТ: БРОСОК МОНЕТЫ")
print("="*60)
print(f"Общее число испытаний (бросков): N = {total_trials}")
print(f"Количество выпавших 'Орлов' (успехов): k = {cumulative_heads[-1]}")
print(f"Частотная вероятность P*(Орел) = k/N = {frequency_probability[-1]:.4f}")
print(f"Классическая (теоретическая) вероятность P(Орел) = {theoretical_prob:.4f}")
print(f"Абсолютная разница: |P* - P| = {abs(frequency_probability[-1] - theoretical_prob):.4f}")
print("-"*60)
print("ВЫВОД: При увеличении числа испытаний (N → ∞) частота события")
print("       стабилизируется и приближается к его классической вероятности.")
print("="*60)