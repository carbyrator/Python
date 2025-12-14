from .author import Author


class App:
    """
    Класс, представляющий приложение с именем, версией и автором.

    Атрибуты:
        name (str): Название приложения.
        version (str): Версия приложения.
        author (Author): Автор приложения (экземпляр класса Author).

    Методы:
        name: Получить или установить название приложения.
        version: Получить или установить версию приложения.
        author: Получить или установить автора приложения.
    """

    def __init__(self, name: str, version: str, author: Author):
        """ Инициализирует объект приложения. """
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author

    @property
    def name(self) -> str:
        """ Возвращает название приложения. """
        return self.__name

    @name.setter
    def name(self, name: str):
        """ Устанавливает название приложения. """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Название приложения должно быть строкой минимум 2 символа')

    @property
    def version(self) -> str:
        """ Возвращает версию приложения. """
        return self.__version

    @version.setter
    def version(self, version: str):
        """ Устанавливает версию приложения. """
        if isinstance(version, str) and len(version) >= 1:
            self.__version = version
        else:
            raise ValueError('Версия должна быть строкой минимум 1 символ')

    @property
    def author(self) -> Author:
        """ Возвращает автора приложения. """
        return self.__author

    @author.setter
    def author(self, author: Author):
        """ Устанавливает автора приложения. """
        if isinstance(author, Author):
            self.__author = author
        else:
            raise ValueError('Автор должен быть экземпляром класса Author')
