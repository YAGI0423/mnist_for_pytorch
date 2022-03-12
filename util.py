import numpy as np

class Util:
    @staticmethod
    def now_turn(list_board):
        return len(list_board) % 2 == 0   #True: 흑, False: 백

    @staticmethod
    def get_square_board(list_board, board_size):
        square_board = np.zeros((board_size, board_size))
        for turn, (x, y) in enumerate(list_board):
            stone_color = -1 if turn % 2 == 0 else 1
            square_board[y][x] = stone_color
        return square_board
