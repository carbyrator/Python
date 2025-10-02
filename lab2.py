from typing import List


def guess_number(target: int, s: List[int], m: str) -> str:
    """
    Поиск числа в списке с помощью линейного или бинарного перебора.

    Args:
        target (int): Число, которое нужно найти.
        s (list[int]): Отсортированный список чисел, в котором ищем.
        m (str): Метод перебора:
            - '1' — медленный (линейный поиск),
            - '2' — быстрый (бинарный поиск).

    Returns:
        str: Сообщение с результатом:
            - если число найдено → "Угадываемое число: X, количество попыток: N",
            - если число не найдено → "Число не найдено".
    """
    if m == '1':  # Линейный перебор
        k: int = 0
        s.sort()
        for i in range(len(s)):
            k += 1
            if s[i] == target:
                return f'Угадываемое число: {target}, количество попыток: {k}'
        return 'Число не найдено'

    else:  # Бинарный перебор
        k: int = 0
        s.sort()
        low: int = 0
        high: int = len(s) - 1
        while low <= high:
            k += 1
            mid: int = (low + high) // 2
            if s[mid] == target:
                return f'Угадываемое число: {target}, количество попыток: {k}'
            elif s[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return 'Число не найдено'


m: str = ''
while m not in ['1', '2']:
    m = input('Введите 1 для использования медленного перебора или 2 для использования бинарного перебора: ')
    if m not in ['1', '2']:
        print('Введите только 1 или 2')

valid_target: bool = False
target: int
while not valid_target:
    target_str: str = input('Введите угадываемое число: ')
    try:
        target = int(target_str)
        if isinstance(target, int):
            valid_target = True
    except ValueError:
        print('Введите целочисленное значение')

valid_start: bool = False
start: int
while not valid_start:
    start_str: str = input('Введите первое число диапазона: ')
    try:
        start = int(start_str)
        if isinstance(start, int):
            valid_start = True
    except ValueError:
        print('Введите целочисленное значение')

valid_end: bool = False
end: int
while not valid_end:
    end_str: str = input('Введите второе число диапазона: ')
    try:
        end = int(end_str)
        if isinstance(end, int):
            if start >= end:
                print('Первое число должно быть меньше второго')
            else:
                valid_end = True
    except ValueError:
        print('Введите целочисленное значение')

s: List[int] = list(range(start, end + 1))
print(guess_number(target, s, m))
