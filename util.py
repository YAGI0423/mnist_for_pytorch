import numpy as np

class Util:
    def __init__(self, board_size):
        self.board_size = board_size

    def now_turn(self, list_board):
        return len(list_board) % 2 == 0   #True: 흑, False: 백

    def get_square_board(self, list_board):
        square_board = np.zeros((self.board_size, self.board_size))
        for turn, (x, y) in enumerate(list_board):
            stone_color = -1 if turn % 2 == 0 else 1
            square_board[y][x] = stone_color
        return square_board
