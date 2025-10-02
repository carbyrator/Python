import unittest
from lab3 import gen_bin_tree, left_branch, right_branch


class TestGenBinTreeSimple(unittest.TestCase):

    def test_leaf_node(self):
        """Проверяем дерево высотой 0"""
        tree = gen_bin_tree(height=0, root=10)
        self.assertEqual(tree, {"10": []})

    def test_height_1(self):
        """Дерево высотой 1: корень и две ветки"""
        tree = gen_bin_tree(height=1, root=10)
        expected = {'10': [{'22': []}, {'18': []}]}
        self.assertEqual(tree, expected)

    def test_root_only(self):
        """Проверяем, что корень совпадает с переданным"""
        tree = gen_bin_tree(height=3, root=99)
        self.assertIn("99", tree)

    def test_left_child_value(self):
        """Проверяем правильность вычисления левого потомка"""
        tree = gen_bin_tree(height=1, root=5)
        left_child_value = list(tree["5"][0].keys())[0]  # получаем ключ первого потомка
        self.assertEqual(left_child_value, "12")  # 2*(5+1)=12

    def test_right_child_value(self):
        """Проверяем правильность вычисления правого потомка"""
        tree = gen_bin_tree(height=1, root=5)
        right_child_value = list(tree["5"][1].keys())[0]  # ключ второго потомка
        self.assertEqual(right_child_value, "8")  # 2*(5-1)=8

    def test_custom_branch_functions(self):
        """Проверяем дерево с другими функциями ветвей"""
        tree = gen_bin_tree(height=1, root=5,
                            l_b=lambda x: x + 100,
                            r_b=lambda x: x - 2)
        expected = {"5": [{"105": []}, {"3": []}]}
        self.assertEqual(tree, expected)

    def test_height_2_tree(self):
        """Проверяем дерево высотой 2: должно быть 2 уровня потомков"""
        tree = gen_bin_tree(height=2, root=1)
        self.assertIn("1", tree)
        self.assertEqual(len(tree["1"]), 2)
        for child in tree["1"]:
            self.assertEqual(len(child[list(child.keys())[0]]), 2)


if __name__ == "__main__":
    unittest.main()
