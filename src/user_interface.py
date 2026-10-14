import logging
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_sides(self):
        pass


class ConsoleUserInterface(UserInterface):

    def get_sides(self):
        a_str = input("Сторона A: ")
        b_str = input("Сторона B: ")
        c_str = input("Сторона C: ")
        logging.info(f"От пользователя получено: {a_str}, {b_str}, {c_str}")
        return a_str, b_str, c_str
