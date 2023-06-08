import unittest

import numpy as np

from main import get_row, check_terminal, get_action_mask, is_win

board = np.zeros((6, 7))
board[5][0] = 1


class TestMain(unittest.TestCase):

    def test_get_row(self):
        self.assertEqual(get_row(board, 0), 4)
        self.assertEqual(get_row(board, 1), 5)

    def test_check_terminal(self):
        self.assertFalse(check_terminal(board))

    def test_get_action_mask(self):
        valid_locations = [1, 2, 3, 4, 5, 6]
        self.assertEqual(get_action_mask(board), valid_locations)

    def test_is_win(self):
        self.assertFalse(is_win(board, 1))


if __name__ == '__main__':
    unittest.main()
