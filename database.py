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
        TODO игнорировать пустые строки
        """
        with open(config.csv_file) as f:
            return f.readlines()[-size:]

    @classmethod
    def writelines(cls, lines: List[str]):
        with open(config.csv_file, 'a') as f:
            # TODO иногда пишем лишний \n, который ломает SensorsData.__init__()
            # попробовать '\n'.join(lines) + '\n'
            f.writelines(map(lambda line: '\n' + line, lines))
