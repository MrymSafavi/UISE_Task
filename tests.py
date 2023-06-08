import unittest

import numpy as np

from main import get_row, check_terminal, get_action_mask, is_win


class TestMathFunctions(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.board = np.zeros((6, 7))

    def test_get_row(self):
        self.board[5][0] = 1
        self.assertEqual(get_row(self.board, 0), 4)
        self.assertEqual(get_row(self.board, 1), 5)

    def test_check_terminal(self):
        self.assertFalse(check_terminal(self.board))

    def test_get_action_mask(self):
        valid_locations = [0, 1, 2, 3, 4, 5, 6]
        assert valid_locations == get_action_mask(self.board)

    def test_is_win(self):
        self.assertFalse(is_win(self.board, 1))
