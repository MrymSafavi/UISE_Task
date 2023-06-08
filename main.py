import math
import random
import sys

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
ME_PLAYER = 0
AI_PLAYER = 1
ME_PLAYER_PIECE = 1
AI_PLAYER_PIECE = 2
NUMBER_OF_PIECE = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def get_row(board, col):
    for r in range(ROW_COUNT - 1, 0, -1):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def is_win(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and \
                    board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and \
                    board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check diagonals - v1
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece \
                    and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check diagonals - v2
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece \
                    and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def give_score_for_move(res_move, piece):
    score = 0
    temp_piece = ME_PLAYER_PIECE
    if piece == ME_PLAYER_PIECE:
        temp_piece = AI_PLAYER_PIECE

    if res_move.count(piece) == 4:
        score += 100
    elif res_move.count(piece) == 3 and res_move.count(0) == 1:
        score += 10
    elif res_move.count(piece) == 2 and res_move.count(0) == 2:
        score += 5
    if res_move.count(temp_piece) == 3 and res_move.count(0) == 1:
        score -= 4

    return score


def position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            choice = row_array[c:c + NUMBER_OF_PIECE]
            score += give_score_for_move(choice, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            choice = col_array[r:r + NUMBER_OF_PIECE]
            score += give_score_for_move(choice, piece)

    # Score diagonal v1
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            choice = [board[r + i][c + i] for i in range(NUMBER_OF_PIECE)]
            score += give_score_for_move(choice, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            choice = [board[r + 3 - i][c + i] for i in range(NUMBER_OF_PIECE)]
            score += give_score_for_move(choice, piece)

    return score


def check_terminal(board):
    if is_win(board, ME_PLAYER_PIECE) or is_win(board, AI_PLAYER_PIECE) or len(get_action_mask(board)) == 0:
        return True


def get_action_mask(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if board[ROW_COUNT - 1][col] == 0:
            valid_locations.append(col)
    return valid_locations


def minimax(board, depth, alpha, beta, player):
    valid_locations = get_action_mask(board)
    is_terminal = check_terminal(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if is_win(board, AI_PLAYER_PIECE):
                return None, sys.maxsize
            elif is_win(board, ME_PLAYER_PIECE):
                return None, -sys.maxsize
            else:
                return None, 0
        else:
            return None, position(board, AI_PLAYER_PIECE)
    if player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = AI_PLAYER_PIECE
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = ME_PLAYER_PIECE
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def main():
    global action
    # env = connect_four_v3.env(render_mode="human")
    # env.reset()

    print("Game Started...")
    board = create_board()
    print("---------Board---------")
    print_board(board)
    game_over = False

    turn = random.randint(ME_PLAYER, AI_PLAYER)

    while not game_over:
        if turn == ME_PLAYER:
            print("-You should move")
            col = random.randint(0, 6)
            action = col

            print(board[ROW_COUNT - 1][col])
            if board[ROW_COUNT - 1][col] == 0:
                row = get_row(board, col)
                board[row][col] = ME_PLAYER_PIECE
                if is_win(board, ME_PLAYER_PIECE):
                    print("Player 1 wins!!")
                    game_over = True

                turn += 1
                turn = turn % 2

        elif turn == AI_PLAYER and not game_over:
            print("-AI should move")
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            action = col

            if board[ROW_COUNT - 1][col] == 0:
                row = get_row(board, col)
                board[row][col] = AI_PLAYER_PIECE
                if is_win(board, AI_PLAYER_PIECE):
                    print("Player 2 wins!!")
                    game_over = True

                turn += 1
                turn = turn % 2
        # env.step(action)
        print('--------Updated Board--------')
        print_board(board)

        if game_over:
            print("Game Over!!!")
            break
    # env.close()


if __name__ == '__main__':
    main()
