import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np


def geometric_probability_four_regions(size):
    # Квадрат
    square_side = 10
    square_area = square_side ** 2
    center_x, center_y = square_side / 2, square_side / 2

    # Круг ВПИСАН в квадрат (касается сторон)
    circle_radius = square_side / 2
    circle_area = np.pi * circle_radius ** 2

    # Равносторонний треугольник ВПИСАН в круг (вершины на окружности)
    triangle_radius = circle_radius
    triangle_vertices = []
    for i in range(3):
        angle = 2 * np.pi * i / 3 - np.pi / 2
        x = center_x + triangle_radius * np.cos(angle)
        y = center_y + triangle_radius * np.sin(angle)
        triangle_vertices.append([x, y])

    # Сторона треугольника
    a = np.sqrt(3) * triangle_radius
    triangle_area = (np.sqrt(3) / 4) * a ** 2

    # Круг ВПИСАН в треугольник (касается сторон изнутри)
    inscribed_circle_radius = a * np.sqrt(3) / 6  # для равностороннего треугольника
    inscribed_circle_area = np.pi * inscribed_circle_radius ** 2

    # ТЕОРЕТИЧЕСКИЕ ВЕРОЯТНОСТИ
    P_square = 1.0  # вся площадь
    P_outer_circle = circle_area / square_area
    P_triangle = triangle_area / square_area
    P_inscribed_circle = inscribed_circle_area / square_area

    # Площади колец
    P_triangle_minus_inner = P_triangle - P_inscribed_circle  # треугольник без внутреннего круга
    P_outer_minus_triangle = P_outer_circle - P_triangle  # круг без треугольника
    P_square_minus_outer = 1 - P_outer_circle  # квадрат без внешнего круга

    print("=== ГЕОМЕТРИЧЕСКАЯ ВЕРОЯТНОСТЬ ===")
    print(f"Площадь квадрата: {square_area:.2f}")
    print(f"Площадь внешнего круга: {circle_area:.2f}")
    print(f"Площадь треугольника: {triangle_area:.2f}")
    print(f"Площадь внутреннего круга: {inscribed_circle_area:.2f}")
    print()

    print("=== ТЕОРЕТИЧЕСКИЕ ВЕРОЯТНОСТИ ===")
    print(f"P(внутренний круг) = {P_inscribed_circle:.4f}")
    print(f"P(треугольник без круга) = {P_triangle_minus_inner:.4f}")
    print(f"P(внешний круг без треугольника) = {P_outer_minus_triangle:.4f}")
    print(f"P(квадрат без внешнего круга) = {P_square_minus_outer:.4f}")
    print(f"Σ = {P_inscribed_circle + P_triangle_minus_inner + P_outer_minus_triangle + P_square_minus_outer:.4f}")
    print()

    # Моделирование бросков
    X = np.random.uniform(0, square_side, size)
    Y = np.random.uniform(0, square_side, size)

    hits = {
        'inscribed_circle': 0,  # внутренний круг
        'triangle_only': 0,  # треугольник без внутреннего круга
        'outer_ring': 0,  # внешний круг без треугольника
        'square_only': 0  # квадрат без внешнего круга
    }

    for i in range(size):
        x, y = X[i], Y[i]
        dist_to_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

        # Проверяем попадание по областям от внутренней к внешней
        if dist_to_center <= inscribed_circle_radius:
            hits['inscribed_circle'] += 1
        elif point_in_triangle(x, y, triangle_vertices):
            hits['triangle_only'] += 1
        elif dist_to_center <= circle_radius:
            hits['outer_ring'] += 1
        else:
            hits['square_only'] += 1

    # Экспериментальные вероятности
    exp_P_inscribed = hits['inscribed_circle'] / size
    exp_P_triangle_only = hits['triangle_only'] / size
    exp_P_outer_ring = hits['outer_ring'] / size
    exp_P_square_only = hits['square_only'] / size

    print("=== РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ ===")
    print(f"Всего бросков: {size}")
    print(f"Внутренний круг: {hits['inscribed_circle']} (P={exp_P_inscribed:.4f})")
    print(f"Треугольник без круга: {hits['triangle_only']} (P={exp_P_triangle_only:.4f})")
    print(f"Внешний круг без треугольника: {hits['outer_ring']} (P={exp_P_outer_ring:.4f})")
    print(f"Квадрат без круга: {hits['square_only']} (P={exp_P_square_only:.4f})")
    print(f"Σ = {exp_P_inscribed + exp_P_triangle_only + exp_P_outer_ring + exp_P_square_only:.4f}")
    print()

    # ВИЗУАЛИЗАЦИЯ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # График 1: Геометрическая схема
    # Квадрат
    ax1.add_patch(Rectangle((0, 0), square_side, square_side,
                            fill=False, edgecolor='black', linewidth=3))

    # Внешний круг
    ax1.add_patch(Circle((center_x, center_y), circle_radius,
                         fill=False, edgecolor='red', linewidth=2))

    # Треугольник
    triangle = Polygon(triangle_vertices, fill=False,
                       edgecolor='blue', linewidth=2)
    ax1.add_patch(triangle)

    # Внутренний круг
    ax1.add_patch(Circle((center_x, center_y), inscribed_circle_radius,
                         fill=False, edgecolor='green', linewidth=2))

    # Точки разными цветами
    colors = []
    for i in range(min(size, 1000)):  # ограничим для наглядности
        x, y = X[i], Y[i]
        dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

        if dist <= inscribed_circle_radius:
            colors.append('green')  # внутренний круг
        elif point_in_triangle(x, y, triangle_vertices):
            colors.append('blue')  # треугольник
        elif dist <= circle_radius:
            colors.append('red')  # внешний круг
        else:
            colors.append('lightgray')  # квадрат

    ax1.scatter(X[:1000], Y[:1000], c=colors, alpha=0.6, s=15)
    ax1.set_xlim(0, square_side)
    ax1.set_ylim(0, square_side)
    ax1.set_aspect('equal')
    ax1.set_title('Геометрическая вероятность: 4 области')
    ax1.grid(True, alpha=0.3)

    # Легенда
    ax1.plot([], [], 'o', color='green', markersize=8, label='Внутренний круг')
    ax1.plot([], [], 'o', color='blue', markersize=8, label='Треугольник')
    ax1.plot([], [], 'o', color='red', markersize=8, label='Внешний круг')
    ax1.plot([], [], 'o', color='lightgray', markersize=8, label='Квадрат')
    ax1.legend()

    # График 2: Сравнение теория/эксперимент
    regions = ['Внутр. круг', 'Треуг. без круга', 'Внеш. кольцо', 'Квадрат']
    theoretical = [P_inscribed_circle, P_triangle_minus_inner, P_outer_minus_triangle, P_square_minus_outer]
    experimental = [exp_P_inscribed, exp_P_triangle_only, exp_P_outer_ring, exp_P_square_only]

    x_pos = np.arange(len(regions))
    width = 0.35

    ax2.bar(x_pos - width / 2, theoretical, width, label='Теория', alpha=0.7)
    ax2.bar(x_pos + width / 2, experimental, width, label='Эксперимент', alpha=0.7)

    ax2.set_xlabel('Области')
    ax2.set_ylabel('Вероятность')
    ax2.set_title('Сравнение теоретической и экспериментальной вероятностей')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(regions)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Добавим значения на столбцы
    for i, (t, e) in enumerate(zip(theoretical, experimental)):
        ax2.text(i - width / 2, t + 0.01, f'{t:.3f}', ha='center', va='bottom')
        ax2.text(i + width / 2, e + 0.01, f'{e:.3f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    return hits, theoretical, experimental


def point_in_triangle(x, y, vertices):
    """Проверка точки в треугольнике методом барицентрических координат"""
    x1, y1 = vertices[0]
    x2, y2 = vertices[1]
    x3, y3 = vertices[2]

    # Векторы
    v0 = [x3 - x1, y3 - y1]
    v1 = [x2 - x1, y2 - y1]
    v2 = [x - x1, y - y1]

    # Скалярные произведения
    dot00 = v0[0] * v0[0] + v0[1] * v0[1]
    dot01 = v0[0] * v1[0] + v0[1] * v1[1]
    dot02 = v0[0] * v2[0] + v0[1] * v2[1]
    dot11 = v1[0] * v1[0] + v1[1] * v1[1]
    dot12 = v1[0] * v2[0] + v1[1] * v2[1]

    # Барицентрические координаты
    inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return (u >= 0) and (v >= 0) and (u + v <= 1)


# Запуск
print("ГЕОМЕТРИЧЕСКАЯ ВЕРОЯТНОСТЬ: 4 вложенные области")
print("=" * 70)
results = geometric_probability_four_regions(2000)