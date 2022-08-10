from util import Util


class Rule:
    def __init__(self, board_size, win_sequence):
        self.board_size = board_size
        self.win_seq = win_sequence

    def evaluate_board(self, yx_board, check_location=None):
        '''
        * yx board를 입력받아, 현재 게임 상태를 반환
        * 특정 수의 좌표 [check_location]를 입력할 경우,
        > 해당 좌표만을 중심으로 평가하고,
        > None일 경우, 게임 보드 전체를 확인하여 평가한다

        *0: during, 1: draw, 2: black win, 3: white win
        '''
        pass

    def evaluate_move(self, yx_board, check_yx):
        '''
        * 특정 수의 좌표[yx]를 보드[yx_board]에 착수하였을 때,
        게임의 상태를 반환

        *0: during, 1: draw, 2: black win, 3: white win
        '''
        pass