import timeit
import matplotlib.pyplot as plt
import random
from lab3 import *
from lab5.lab5 import *


def benchmark(func, root: int, height: int, l_b, r_b, repeat=5, number=10) -> float:
    """Замеряет минимальное время выполнения программы."""
    t = timeit.repeat(lambda: func(height, root, l_b, r_b), repeat=repeat, number=number)
    return min(t)


def main() -> None:
    """Сравнивает производительность рекурсивного и итеративного
    алгоритмов построения бинарного дерева на разных высотах.
    Строит график зависимости времени выполнения от высоты дерева
    и выводит численные результаты в консоль."""
    random.seed(42)
    test_data = list(range(1, 16))

    res_recursive = []
    res_iterative = []

    root_value = 15

    for h in test_data:
        res_recursive.append(benchmark(gen_bin_tree1, root_value, h, left_branch, right_branch))
        res_iterative.append(benchmark(gen_bin_tree, root_value, h, left_branch, right_branch))

    # Визуализация результатов
    plt.plot(test_data, res_recursive, label="Рекурсивный", marker='o')
    plt.plot(test_data, res_iterative, label="Итеративный", marker='x')
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного построения дерева")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Вывод численных значений
    for h, r, i in zip(test_data, res_recursive, res_iterative):
        print(f"Высота {h}: рекурсивный = {r:.6f}s, итеративный = {i:.6f}s")


if __name__ == "__main__":
    main()
