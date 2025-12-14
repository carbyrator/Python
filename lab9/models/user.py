class User:
    """
    Класс, представляющий пользователя с его идентификатором и именем.

    Атрибуты:
        id (int): Идентификатор пользователя (положительное целое число).
        name (str): Имя пользователя (строка длиной минимум 2 символа).

    Методы:
        id: Получить или установить идентификатор пользователя.
        name: Получить или установить имя пользователя.
    """

    def __init__(self, id: int, name: str):
        """ Инициализирует объект пользователя. """
        self.__id: int = id
        self.__name: str = name

    @property
    def id(self) -> int:
        """ Возвращает идентификатор пользователя. """
        return self.__id

    @id.setter
    def id(self, id: int):
        """ Устанавливает идентификатор пользователя. """
        if isinstance(id, int) and id > 0:
            self.__id = id
        else:
            raise ValueError('ID должен быть положительным целым числом')

    @property
    def name(self) -> str:
        """ Возвращает имя пользователя. """
        return self.__name

    @name.setter
    def name(self, name: str):
        """ Устанавливает имя пользователя. """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Имя пользователя должно быть строкой минимум 2 символа')
