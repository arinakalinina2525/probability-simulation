from random import sample
import plotly.graph_objs as go
import numpy as np

# Функция для одного эксперимента
def draw_two_balls():
    urn = ['Red'] * 3 + ['Blue'] * 2  # 3 красных, 2 синих
    balls = sample(urn, 2)  # вынимаем 2 шара без возвращения
    return balls[0] == balls[1]  # True если оба одного цвета

# Параметры моделирования
N_values = np.array(range(10, 10001, 50))  # от 10 до 10000 экспериментов с шагом 50
frequencies = []

# Моделирование для разных N
for N in N_values:
    successes = 0
    for _ in range(N):
        if draw_two_balls():
            successes += 1
    frequencies.append(successes / N)

# Теоретическая вероятность
classical_probability = 0.4  # (C(3,2) + C(2,2)) / C(5,2) = (3 + 1)/10 = 0.4
theory_line = [classical_probability] * len(N_values)

print(f"Частотная вероятность при N=10000: {frequencies[-1]:.4f}")
print(f"Классическая вероятность: {classical_probability:.4f}")

# Построение графика
fig = go.Figure()
fig.add_trace(go.Scatter(x=N_values, y=frequencies,
                         name='Частотная вероятность',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=N_values, y=theory_line,
                         name='Классическая вероятность',
                         line=dict(color='red', dash='dash')))

fig.update_layout(
    title='Сходимость частотной вероятности к классической',
    xaxis_title='Количество экспериментов N',
    yaxis_title='Вероятность P(A)',
    width=700,
    height=400,
    showlegend=True
)

fig.show()