class UserCurrency:
    """
    Класс, представляющий связь между пользователем и валютой.

    Атрибуты:
        id (int): Идентификатор связи.
        user_id (int): Идентификатор пользователя (положительное целое число).
        currency_id (str): Идентификатор валюты (непустая строка).

    Методы:
        id: Получить или установить идентификатор связи.
        user_id: Получить или установить идентификатор пользователя.
        currency_id: Получить или установить идентификатор валюты.
    """

    def __init__(self, id: int, user_id: int, currency_id: str):
        """ Инициализирует объект связи между пользователем и валютой. """
        self.__id: int = id
        self.__user_id: int = user_id
        self.__currency_id: str = currency_id

    @property
    def id(self) -> int:
        """ Возвращает идентификатор связи. """
        return self.__id

    @id.setter
    def id(self, id: int):
        """ Устанавливает идентификатор связи. """
        if isinstance(id, int) and id > 0:
            self.__id = id
        else:
            raise ValueError('ID должен быть положительным целым числом')

    @property
    def user_id(self) -> int:
        """ Возвращает идентификатор пользователя. """
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        """ Устанавливает идентификатор пользователя. """
        if isinstance(user_id, int) and user_id > 0:
            self.__user_id = user_id
        else:
            raise ValueError('ID пользователя должен быть положительным целым числом')

    @property
    def currency_id(self) -> str:
        """ Возвращает идентификатор валюты. """
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: str):
        """ Устанавливает идентификатор валюты. """
        if isinstance(currency_id, str) and len(currency_id) >= 1:
            self.__currency_id = currency_id
        else:
            raise ValueError('ID валюты должен быть непустой строкой')
