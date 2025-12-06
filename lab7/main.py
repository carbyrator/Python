import io
import logging
import math
from decorator import logger
from currencies import get_currencies

# Настройка логирования
file_logger = logging.getLogger("file_logger")
file_handler = logging.FileHandler('currency.log')

# Добавляем форматирование, включающее время
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

file_logger.addHandler(file_handler)
file_logger.setLevel(logging.INFO)  # Установим уровень логирования

print("ДЕМОНСТРАЦИЯ ДЕКОРАТОРА")

# Вариант 2: Логирование в файл
@logger(handle=file_logger)
def test2(codes):
    return get_currencies(codes)


# Часть 1: Получение курсов
print("\n1. Тест курсов валют")

print("\nа) Нормальная работа:")
try:
    res = test2(['USD', 'EUR'])
    print(f"   USD: {res['USD']}, EUR: {res['EUR']}")
except Exception as e:
    print(f"   Ошибка: {e}")

print("\nб) Ошибка - нет такой валюты:")
try:
    res = test2(['USD', 'XYZ'])
    print(res)
except Exception as e:
    print(f"   Ошибка: {e}")

print("\nв) Логирование в файл:")
try:
    res = test2(['USD', 'EUR'])
    print(f"   Результат сохранен в currency.log")
except Exception as e:
    print(f"   Ошибка: {e}")

# Часть 2: Квадратное уравнение
print("\n\n2. Квадратное уравнение")


@logger(handle=file_logger)
def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение
    """
    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise TypeError("Нужны числа")

    if a == 0 and b == 0:
        raise ValueError("Это не уравнение")

    if a == 0:
        return (-c / b,)

    D = b * b - 4 * a * c

    # Если дискриминант отрицателен, действительных корней нет
    if D < 0:
        return tuple()

    # Вычисляем корни
    sqrt_d = math.sqrt(D)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)

    # При D == 0 оба корня совпадают — возвращаем единственный корень
    if D == 0:
        return (x1,)

    # Для двух различных корней возвращаем их в порядке возрастания
    return tuple(sorted((x1, x2)))


# Тесты
test_cases = [
    (1, -3, 2, "Нормальный случай"),
    (1, 2, 5, "Дискриминант < 0"),
    (0, 2, -4, "Линейное"),
    (0, 0, 5, "Не уравнение"),
    ("a", 2, 3, "Не числа")
]

for a, b, c, desc in test_cases:
    print(f"\n   {desc}: {a}x² + {b}x + {c} = 0")
    try:
        res = solve_quadratic(a, b, c)
        print(f"   Корни: {res}")
    except Exception as e:
        print(f"   Ошибка: {e}")

# Часть 3: Логи в файл
print("\n\n3. Логирование в файл:")
print("   Логи записываются в файл currency.log")
