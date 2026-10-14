import logging
from abc import ABC, abstractmethod

class ResultSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailSender(ResultSender):
    def send(self, message):
        logging.info(f"[ИМИТАЦИЯ] Отправка на email-сервер: {message}")
        return True
