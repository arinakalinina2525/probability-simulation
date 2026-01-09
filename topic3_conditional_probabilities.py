import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. ГЕНЕРАЦИЯ ДАННЫХ (Парадокс: A лучше в группах, но хуже в общем)
np.random.seed(42)
# Структура: [Группа, Лекарство, Успехи, Всего]
# Группа 1 (Молодые): A(80/100), B(70/100) -> A лучше
# Группа 2 (Пожилые): A(40/400), B(30/400) -> A лучше
groups = [
    ('Молодой', 'A', 80, 100), ('Молодой', 'B', 70, 100),
    ('Пожилой', 'A', 160, 400), ('Пожилой', 'B', 120, 400)
]
df = pd.DataFrame(groups, columns=['Возраст', 'Лекарство', 'Успех', 'Всего'])
df['Вероятность'] = df['Успех'] / df['Всего']

# 2. АГРЕГАЦИЯ (Общие данные)
total = df.groupby('Лекарство').sum(numeric_only=True)
total['Вероятность'] = total['Успех'] / total['Всего']

# 3. ВЫВОД РЕЗУЛЬТАТОВ
print("ЭФФЕКТИВНОСТЬ ПО ГРУППАМ:")
print(df[['Возраст', 'Лекарство', 'Вероятность']].to_string(index=False))
print("\nОБЩАЯ ЭФФЕКТИВНОСТЬ (ПАРАДОКС):")
print(total[['Вероятность']])

# 4. ВИЗУАЛИЗАЦИЯ
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# График 1: По группам
for i, age in enumerate(['Молодой', 'Пожилой']):
    data = df[df['Возраст'] == age]
    ax1.bar(np.arange(2) + i*0.3, data['Вероятность'], width=0.3, label=f'Группа: {age}')

ax1.set_title('Эффективность в подгруппах (A > B)')
ax1.set_xticks([0.15, 1.15])
ax1.set_xticklabels(['Лекарство A', 'Лекарство B'])
ax1.legend()

# График 2: Итого (Парадокс)
ax2.bar(total.index, total['Вероятность'], color=['blue', 'red'], alpha=0.6)
ax2.set_title('Общая эффективность (A < B?)')

for ax in [ax1, ax2]:
    ax.set_ylim(0, 1)
    ax.grid(axis='y', linestyle='--', alpha=0.7)



plt.suptitle('Парадокс Симпсона: Влияние весов групп на общий результат', fontsize=15)
plt.tight_layout()
plt.show()