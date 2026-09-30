import logging
import math


def get_vertices(a, b, c):
    x1, y1 = 0.0, 0.0
    x2, y2 = c, 0.0
    x3 = (b * b + c * c - a * a) / (2 * c)
    y3 = math.sqrt(b * b - x3 * x3)

    min_x = min(x1, x2, x3)
    min_y = min(y1, y2, y3)
    x1, x2, x3 = x1 - min_x, x2 - min_x, x3 - min_x
    y1, y2, y3 = y1 - min_y, y2 - min_y, y3 - min_y

    width = max(x1, x2, x3)
    height = max(y1, y2, y3)
    scale = min(100 / width, 100 / height)

    points = [
        (int(round(x1 * scale)), int(round(y1 * scale))),
        (int(round(x2 * scale)), int(round(y2 * scale))),
        (int(round(x3 * scale)), int(round(y3 * scale)))
    ]
    logging.debug(f"Координаты вершин: {points}")
    return points

def classify_triangle(a_str, b_str, c_str):
    logging.info(f"Запрос: A={a_str}, B={b_str}, C={c_str}")

    try:
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
    except ValueError:
        logging.error("Введены нечисловые данные")
        logging.exception("Заход в блок обработки исключения:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    logging.debug(f"Числа получены: a={a}, b={b}, c={c}")
    all_finite = math.isfinite(a) and math.isfinite(b) and math.isfinite(c)
    if not all_finite or a <= 0 or b <= 0 or c <= 0:
        logging.error("Стороны должны быть положительными числами")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning("Неравенство треугольника не выполняется")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b and b == c:
        kind = "равносторонний"
    elif a == b or b == c or a == c:
        kind = "равнобедренный"
    else:
        kind = "разносторонний"

    points = get_vertices(a, b, c)
    logging.info(f"Результат: {kind}, вершины {points}")
    return kind, points
