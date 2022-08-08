import numpy as np

class Util:
    @staticmethod
    def get_current_turn(yx_board):
        '''
        * 좌표 보드를 입력받아 현재 시점에서 착수할 플레이어를 반환한다.
        * 0: 흑, 1: 백
        '''
        return len(yx_board) % 2

    @staticmethod
    def yx_to_square_board(yx_board, board_size):
        '''
        * yx 보드를 square_board로 변환하여 반환
        * -1: black, 0: empty, +1: white
        '''
        square_board = np.zeros(shape=(board_size, board_size), dtype=np.float32)

        for idx, yx in enumerate(yx_board):
            current_color = (idx % 2) * 2 - 1 #-1:흑, 1: 백
            square_board[yx] = current_color
        return square_board
            
