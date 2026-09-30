import logging
import sys

from src.triangle import classify_triangle


def Main():
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    try:
        examples = [
            ("3", "4", "5"),
            ("5", "5", "5"),
            ("5", "5", "8"),
            ("7", "3", "5"),
            ("1", "2", "10"),
            ("-3", "4", "5"),
            ("abc", "4", "5")
        ]

        for a, b, c in examples:
            kind, points = classify_triangle(a, b, c)
            print(f"{a}, {b}, {c} -> {kind} {points}")

        print("\nВведите три стороны (или просто Enter, чтобы выйти):")
        while True:
            a = input("Сторона A: ")
            if a == "":
                break
            b = input("Сторона B: ")
            c = input("Сторона C: ")

            kind, points = classify_triangle(a, b, c)
            print(f"Вид треугольника: {kind}")
            print(f"Координаты вершин: {points}\n")

    except Exception:
        logging.error("Что-то пошло не так...")
        logging.exception("Заход в блок обработки исключения:")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    Main()

