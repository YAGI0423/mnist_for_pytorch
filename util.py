import numpy as np

class Util:
    @staticmethod
    def now_turn(seq_xy_board):
        return len(seq_xy_board) % 2 == 0   #True: 흑, False: 백

    @staticmethod
    def seq_to_square(seq_xy_board, board_size):
        square_board = np.zeros((board_size, board_size))
        for turn, (x, y) in enumerate(seq_xy_board):
            surrender_TF = (x, y) != (0, board_size)   #surrender
            pass_TF = (x, y) != (-1, -1)   #stone pass

            if surrender_TF and pass_TF:
                stone_color = -1 if turn % 2 == 0 else 1
                square_board[y][x] = stone_color
        return square_board
