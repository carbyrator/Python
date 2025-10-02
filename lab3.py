from pprint import pprint
from typing import Callable, Dict, List

# Тип для дерева: ключ — str, значение — список поддеревьев
Tree = Dict[str, List['Tree']]


def left_branch(root: int) -> int:
    """
    Вычисляет значение левого потомка узла дерева.

    :param root: Значение текущего узла
    :return: Значение левого потомка
    """
    return 2 * (root + 1)


def right_branch(root: int) -> int:
    """
    Вычисляет значение правого потомка узла дерева.

    :param root: Значение текущего узла
    :return: Значение правого потомка
    """
    return 2 * (root - 1)


def gen_bin_tree(height: int = 6, root: int = 15,
                 l_b: Callable[[int], int] = left_branch,
                 r_b: Callable[[int], int] = right_branch) -> Tree:
    """
    Генерация бинарного дерева в виде словаря со списком потомков.

    :param height: Высота дерева
    :param root: Значение корня дерева
    :param l_b: Функция вычисления левого потомка
    :param r_b: Функция вычисления правого потомка
    :return: Словарь, где ключ — значение узла, а значение — список дочерних ветвей
    """
    if height <= 0:
        return {str(root): []}  # Лист дерева

    left_b = gen_bin_tree(height - 1, l_b(root), l_b, r_b)
    right_b = gen_bin_tree(height - 1, r_b(root), l_b, r_b)

    return {str(root): [left_b, right_b]}


if __name__ == "__main__":
    # Генерация дерева
    tree = gen_bin_tree(height=6, root=15)
    print("Сгенерированное бинарное дерево:")
    pprint(tree)
