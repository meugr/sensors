from typing import List
from config import Config

config = Config()


class Database:
    """
    Класс для работы с базой измерений.
    TODO Перенести сюда логику работы с csv, наружу прокинуть интерфейсы
    """
    @classmethod
    def tail(cls, size) -> List[str]:
        """
        Return a list last elements from DB
        """
        with open(config.csv_file) as f:
            return [i for i in f.readlines()[-size:] if i]

    @classmethod
    def writelines(cls, lines: List[str]):
        with open(config.csv_file, 'a') as f:
            f.write('\n'.join(lines) + '\n')
