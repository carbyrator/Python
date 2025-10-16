import unittest
from lab5.lab5 import gen_bin_tree


class TestGenBinTreeSimple(unittest.TestCase):

    def test_height_one(self):
        """Отсутствие потомков"""
        tree = gen_bin_tree(height=1)
        self.assertEqual(list(tree.values())[0], [])

    def test_height_zero(self):
        """дерево пустое при height=0"""
        tree = gen_bin_tree(height=0)
        self.assertEqual(tree, {})

    def test_children_default(self):
        """Должно быть 2 потомка"""
        tree = gen_bin_tree(height=2, root=1)
        children = list(tree.values())[0]
        self.assertEqual(len(children), 2)

    def test_custom_left_right_branch(self):
        """Проверка корректности первых потомков"""
        tree = gen_bin_tree(height=2, root=1, left_branch=lambda x: x + 10, right_branch=lambda x: x + 20)
        children = list(tree.values())[0]
        self.assertIn({'11': []}, children)
        self.assertIn({'21': []}, children)

    def test_depth_two(self):
        """Проверка глубины"""
        tree = gen_bin_tree(height=2, root=5)

        def get_depth(node):
            if not node:
                return 0
            children = list(node.values())[0]
            if not children:
                return 1
            return 1 + max(get_depth(c) for c in children)

        self.assertEqual(get_depth(tree), 2)

    def test_children_values(self):
        """Тестируем корректность потомков для небольшой глубины"""
        tree = gen_bin_tree(height=2, root=1, left_branch=lambda x: x + 1, right_branch=lambda x: x + 2)
        expected = {
            '1': [
                {'2': []},
                {'3': []}
            ]
        }
        self.assertEqual(tree, expected)


if __name__ == "__main__":
    unittest.main()
