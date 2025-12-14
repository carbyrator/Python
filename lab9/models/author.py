class Author:
    """
    Класс, представляющий автора с именем и группой.

    Атрибуты:
        name (str): Имя автора.
        group (str): Группа, к которой принадлежит автор.

    Методы:
        name: Получить или установить имя автора.
        group: Получить или установить группу автора.
    """

    def __init__(self, name: str, group: str):
        """ Инициализирует объект автора. """
        self.__name: str = name
        self.__group: str = group

    @property
    def name(self) -> str:
        """ Возвращает имя автора. """
        return self.__name

    @name.setter
    def name(self, name: str):
        """ Устанавливает имя автора. """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Имя автора должно быть строкой минимум 2 символа')

    @property
    def group(self) -> str:
        """ Возвращает группу автора. """
        return self.__group

    @group.setter
    def group(self, group: str):
        """ Устанавливает группу автора. """
        if isinstance(group, str) and len(group) >= 3:
            self.__group = group
        else:
            raise ValueError('Группа должна быть строкой минимум 3 символа')
