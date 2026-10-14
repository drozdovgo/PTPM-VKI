import logging
import os
import sys

from src.controller import Controller
from src.database import Database
from src.notifier import EmailSender
from src.triangle import Triangle
from src.user_interface import ConsoleUserInterface


def configure_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | [%(levelname)-7s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8")
        ]
    )
    logging.info("Логгер успешно сконфигурирован")


def build_controller(db_path="triangles.db"):
    return Controller(
        ConsoleUserInterface(),
        Database(db_path),
        Triangle(),
        EmailSender()
    )


def Main():
    configure_logging()
    logging.info("Приложение запущено")

    try:
        print(build_controller().run())
    except Exception:
        logging.error("Что-то пошло не так...")
        logging.exception("Заход в блок обработки исключения:")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    Main()
