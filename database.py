from typing import  List
from config import Config

config = Config()

class Database:
    """
    Класс для работы с базой измерений.
    Перенести сюда логику работы с csv, наружу прокинуть интерфейсы
    """
    @classmethod
    def readlines(cls, size) -> List[str]:
        """
        Return a list last elements from DB
        """
        with open(config.csv_file) as f:
            return f.readlines()[-size:]

    @classmethod
    def writelines(cls, lines: List[str]):
        with open(config.csv_file, 'a') as f:
            f.writelines(map(lambda line: line + '\n', lines))