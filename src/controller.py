import logging

class Controller:
    def __init__(self, user_interface, database, calculator, sender):
        self.user_interface = user_interface
        self.database = database
        self.calculator = calculator
        self.sender = sender

    def run(self):
        a_str, b_str, c_str = self.user_interface.get_sides()

        record = self.database.get(a_str, b_str, c_str)
        if record is None:
            logging.info("Записи в БД нет - выполняется расчёт")
            kind, points = self.calculator.classify_triangle(a_str, b_str, c_str)
            error = self.get_error(points)
            self.database.add(a_str, b_str, c_str, kind, error)
        else:
            logging.info("Запись найдена в БД - расчёт не требуется")
            kind, error = record

        message = f"Стороны {a_str}, {b_str}, {c_str} -> {kind or 'нет результата'}"
        if error:
            message = f"{message} (ошибка: {error})"

        self.sender.send(message)
        logging.info(f"Результат: {message}")
        return message

    def get_error(self, points):
        if points[0] == (-2, -2):
            return "нечисловые данные"
        if points[0] == (-1, -1):
            return "стороны не образуют треугольник"
        return ""
