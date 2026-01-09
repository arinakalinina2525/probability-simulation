import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. ЗАГРУЗКА И ОПИСАНИЕ ДАННЫХ ===
# Используем набор данных Adult Census (Данные переписи населения)
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/adult-all.csv"
columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 
           'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 
           'hours_per_week', 'native_country', 'income']
df = pd.read_csv(url, names=columns, na_values='?', skipinitialspace=True)

# Целевое событие A: Доход >50K
df['is_rich'] = (df['income'] == '>50K').astype(int)

print("--- Описание признаков ---")
print(f"Общее количество записей: {df.shape[0]}")
print(f"Признаки для анализа: 'sex' (Пол), 'education' (Образование)")
print(f"Целевое событие: доход >50K в год\n")

# === 2. РАСЧЕТ УСЛОВНЫХ ВЕРОЯТНОСТЕЙ (Аналог crosstab из примера) ===

# Создаем таблицу сопряженности для пола и дохода
sex_crosstab = pd.crosstab(df['sex'], df['income'], normalize='index')

# Создаем таблицу сопряженности для образования и дохода
# Ограничимся основными категориями для чистоты графика
edu_filter = df[df['education'].isin(['Bachelors', 'HS-grad', 'Masters', 'Doctorate', 'Some-college'])]
edu_crosstab = pd.crosstab(edu_filter['education'], edu_filter['income'], normalize='index')

# === 3. ВИЗУАЛИЗАЦИЯ (Как в предоставленном файле) ===

plt.figure(figsize=(16, 6))

# Левый график: Влияние пола
plt.subplot(1, 2, 1)
sns.heatmap(sex_crosstab, annot=True, cmap="YlGnBu", cbar=False)
plt.title('P(Income | Sex)\nУсловная вероятность дохода в зависимости от пола')
plt.ylabel('Пол')
plt.xlabel('Уровень дохода')

# Правый график: Влияние образования
plt.subplot(1, 2, 2)
# Визуализация через накопительную столбчатую диаграмму (как часто делают в анализе данных)
edu_crosstab.plot(kind='barh', stacked=True, ax=plt.gca(), color=['#f99191', '#91f991'])
plt.title('P(Income | Education)\nСоотношение доходов по уровням образования')
plt.legend(title='Доход', loc='lower right')
plt.xlabel('Доля (Вероятность)')
plt.ylabel('Образование')

plt.tight_layout()
plt.show()

# === 4. ТЕОРЕТИКО-ВЕРОЯТНОСТНЫЙ АНАЛИЗ ===
p_A = df['is_rich'].mean()  # Априорная вероятность

# Апостериорные вероятности (уточненные после получения данных)
p_A_cond_male = sex_crosstab.loc['Male', '>50K']
p_A_cond_female = sex_crosstab.loc['Female', '>50K']
p_A_cond_doctorate = edu_crosstab.loc['Doctorate', '>50K']

print("="*65)
print("АНАЛИЗ АПРИОРНЫХ И АПОСТЕРИОРНЫХ ВЕРОЯТНОСТЕЙ")
print("="*65)
print(f"АПРИОРНАЯ ВЕРОЯТНОСТЬ P(A): {p_A:.4f}")
print(" (Вероятность высокого дохода без учета доп. факторов)")
print("-" * 65)
print(f"АПОСТЕРИОРНАЯ ВЕРОЯТНОСТЬ P(A | Male):      {p_A_cond_male:.4f}")
print(f"АПОСТЕРИОРНАЯ ВЕРОЯТНОСТЬ P(A | Female):    {p_A_cond_female:.4f}")
print(f"АПОСТЕРИОРНАЯ ВЕРОЯТНОСТЬ P(A | Doctorate): {p_A_cond_doctorate:.4f}")
print("-" * 65)

# Проверка на независимость (как в примерах из Drive)
print("ВЫВОД:")
if abs(p_A - p_A_cond_male) > 0.05:
    print("События зависимы: априорная вероятность P(A) значительно отличается")
    print("от апостериорной P(A|B). Данный признак является информативным.")
else:
    print("События практически независимы.")
print("="*65)
# === 5. РАСЧЕТ ПО ФОРМУЛЕ БАЙЕСА ===

# 1. Априорная вероятность высокого дохода P(A)
p_high_income = df['is_rich'].mean()

# 2. Априорная вероятность, что человек - женщина P(B)
p_female = (df['sex'] == 'Female').mean()

# 3. Условная вероятность (правдоподобие) P(A|B): доход >50K, если это женщина
p_high_income_given_female = sex_crosstab.loc['Female', '>50K']

# 4. Формула Байеса: P(B|A) = (P(A|B) * P(B)) / P(A)
# Вероятность того, что человек женщина, при условии, что доход >50K
p_female_given_high_income = (p_high_income_given_female * p_female) / p_high_income

print("="*65)
print("РАСЧЕТ ОБРАТНОЙ ВЕРОЯТНОСТИ ПО ТЕОРЕМЕ БАЙЕСА")
print("="*65)
print(f"1. Вероятность высокого дохода P(High Income): {p_high_income:.4f}")
print(f"2. Вероятность встретить женщину P(Female): {p_female:.4f}")
print(f"3. Вероятность, что женщина богата P(High Income | Female): {p_high_income_given_female:.4f}")
print("-" * 65)
print(f"РЕЗУЛЬТАТ (Байес):")
print(f"Вероятность P(Female | High Income) = {p_female_given_high_income:.4f}")
print("-" * 65)
print("ИНТЕРПРЕТАЦИЯ:")
print(f"Хотя среди женщин только {p_high_income_given_female*100:.1f}% имеют высокий доход,")
print(f"среди всех богатых людей женщины составляют {p_female_given_high_income*100:.1f}%.")
print("="*65)
