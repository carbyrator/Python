from collections import deque
from typing import Callable, Dict, List
from pprint import pprint


def gen_bin_tree(
        height: int = 6,
        root: int = 15,
        left_branch: Callable[[int], int] = lambda x: 2 * (x + 1),
        right_branch: Callable[[int], int] = lambda x: 2 * (x - 1)
) -> Dict[str, List[int]]:
    """ Функция строит бинарное дерево, где каждый узел имеет до двух потомков:
    левый и правый. Значения потомков вычисляются на основе переданных лямбда-функций. """
    if height < 1:
        return {}

    tree = {str(root): []}

    queue = deque([(root, 1, tree[str(root)])])

    while queue:
        node, level, container = queue.popleft()

        if level < height:
            left_val = left_branch(node)
            right_val = right_branch(node)

            # создаём поддеревья для потомков
            left_subtree = {str(left_val): []}
            right_subtree = {str(right_val): []}

            # добавляем потомков в контейнер текущего узла
            container.extend([left_subtree, right_subtree])

            # добавляем потомков в очередь
            queue.append((left_val, level + 1, left_subtree[str(left_val)]))
            queue.append((right_val, level + 1, right_subtree[str(right_val)]))

    return tree


if __name__ == "__main__":
    tree = gen_bin_tree(height=6, root=15)
    pprint(tree)
