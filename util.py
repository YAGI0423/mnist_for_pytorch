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

    @classmethod
    def get_model_input(cls, seq_xy_board, board_size):
        #list_board ==> moel input tensor

        def filt_board(square_board, stone_color):
            #filt squre board stone
            board = (square_board == stone_color)
            board = board.astype(np.float64)
            return board

        square_board = cls.seq_to_square(seq_xy_board, board_size)
        black_board = filt_board(square_board, -1)
        white_board = filt_board(square_board, 1)

        turn_board = np.zeros((board_size, board_size))
        if len(seq_xy_board) % 2 == 1:   #흑: 0, 백: 1
            turn_board[:] = 1.

        input_tensor = np.array((black_board, white_board, turn_board))
        input_tensor = input_tensor.reshape(1, board_size, board_size, 3)
        return input_tensor
