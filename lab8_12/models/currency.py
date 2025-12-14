class Currency:
    """
    Класс, представляющий валюту с её идентификатором, кодами, названием, курсом и номиналом.

    Атрибуты:
        id (str): Идентификатор валюты.
        num_code (str): Цифровой код валюты (три символа).
        char_code (str): Символьный код валюты (три символа).
        name (str): Название валюты.
        value (float): Курс за 1 единицу валюты.
        nominal (int): Номинал валюты из API ЦБ.

    Методы:
        id: Получить или установить идентификатор валюты.
        num_code: Получить или установить цифровой код валюты.
        char_code: Получить или установить символьный код валюты.
        name: Получить или установить название валюты.
        value: Получить или установить курс валюты.
        nominal: Получить или установить номинал валюты.
        get_value_per_unit: Получить курс за 1 единицу валюты.
    """

    def __init__(
        self,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int,
        id: int | None = None,
    ):
        """Инициализирует объект валюты."""
        self.__id: int | None = id
        self.__num_code: str = num_code
        self.char_code = char_code
        self.__name: str = name
        self.value = value
        self.__nominal: int = nominal

    @property
    def id(self) -> int | None:
        """ Возвращает идентификатор валюты. """
        return self.__id

    @id.setter
    def id(self, id: int | None):
        """ Устанавливает идентификатор валюты. """
        if id is None or isinstance(id, int):
            self.__id = id
            return
        raise ValueError('ID валюты должен быть целым числом или None')

    @property
    def num_code(self) -> str:
        """ Возвращает цифровой код валюты. """
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str):
        """ Устанавливает цифровой код валюты. """
        if isinstance(num_code, str) and len(num_code) == 3:
            self.__num_code = num_code
        else:
            raise ValueError('Цифровой код должен быть строкой из 3 символов')

    @property
    def char_code(self) -> str:
        """ Возвращает символьный код валюты. """
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        """ Устанавливает символьный код валюты. """
        if not isinstance(char_code, str) or len(char_code) != 3:
            raise ValueError('Символьный код должен быть строкой из 3 символов')
        self.__char_code = char_code.upper()

    @property
    def name(self) -> str:
        """ Возвращает название валюты. """
        return self.__name

    @name.setter
    def name(self, name: str):
        """ Устанавливает название валюты. """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Название валюты должно быть строкой минимум 2 символа')

    @property
    def value(self) -> float:
        """ Возвращает курс валюты. """
        return self.__value

    @value.setter
    def value(self, value: float):
        """ Устанавливает курс валюты. """
        if not isinstance(value, (int, float)):
            raise ValueError('Курс должен быть числом')
        if value < 0:
            raise ValueError('Курс валюты не может быть отрицательным')
        self.__value = float(value)

    @property
    def nominal(self) -> int:
        """ Возвращает номинал валюты. """
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        """ Устанавливает номинал валюты. """
        if isinstance(nominal, int) and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError('Номинал должен быть положительным целым числом')

    def get_value_per_unit(self) -> float:
        """Возвращает курс за 1 единицу валюты."""
        return self.__value
