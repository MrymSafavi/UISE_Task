import unittest

import numpy as np

from main import get_row, check_terminal, get_action_mask, is_win


class TestMain(unittest.TestCase):

    def setUp(self):
        self.board = np.zeros((6, 7))
        self.board[5][0] = 1

    def test_get_row(self):
        self.assertEqual(get_row(self.board, 0), 4)
        self.assertEqual(get_row(self.board, 1), 5)

    def test_check_terminal(self):
        self.assertFalse(check_terminal(self.board))

    def test_get_action_mask(self):
        valid_locations = [1, 2, 3, 4, 5, 6]
        self.assertEqual(get_action_mask(self.board), valid_locations)

    def test_is_win(self):
        self.assertFalse(is_win(self.board, 1))


if __name__ == '__main__':
    unittest.main()
