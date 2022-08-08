from util import Util

import numpy as np

class Rule:
    def __init__(self, board_size, win_sequence):
        self.board_size = board_size
        self.win_seq = win_sequence

    def evaluate_board(self, yx_board):
        '''
        * yx board를 입력받아, 현재 게임 상태를 반환
        *0: during, 1: draw, 2: black win, 3: white win
        '''

        #자체 함수=============================
        def crop_board(square_board, stone_location, cut_size: int):
            '''
            * [square_board]를 [stone_locate]기준으로 ±[cut_size]만큼 크롭하여 반환
            '''

            def get_crop_index(location: int, cut_size: int, board_size: int):
                '''
                * 크롭을 위한 위치(Index)를 반환
                * board cut idx: cut_min_idx, cut_max_idx
                * board shift idx: shift_min_idx, shift_max_idx
                '''
                cut_min_idx = np.clip(location - cut_size, 0, None)
                cut_max_idx = np.clip(location + cut_size, 0, board_size - 1) + 1

                shift_min_idx = cut_size - location + cut_min_idx
                shift_max_idx = shift_min_idx + cut_max_idx - cut_min_idx
                return (cut_min_idx, cut_max_idx), (shift_min_idx, shift_max_idx)

            y, x = stone_location
            tensor_board = np.zeros((cut_size*2+1, cut_size*2+1))

            cut_x, shift_x = get_crop_index(x, cut_size, self.board_size)
            cut_y, shift_y = get_crop_index(y, cut_size, self.board_size)

            cropped_board = square_board[   #cropping board
                cut_y[0]:cut_y[1],
                cut_x[0]:cut_x[1]
            ]

            tensor_board[   #마지막 착수를 중심으로 정방 행렬 생성
                shift_y[0]:shift_y[1],
                shift_x[0]:shift_x[1]
            ] = cropped_board

            return tensor_board
        #End==================================

        #전체 돌 수가 게임 종료 가능 착수 수보다 작을 때
        if len(yx_board) < self.win_seq * 2 - 1:
            return 0

        print(yx_board)
        exit()

        square_board = Util.yx_to_square_board(yx_board=yx_board, board_size=self.board_size)
        cropped_board = crop_board(
            square_board=square_board,  #게임 보드에서
            stone_location=yx_board[-1],    #마지막 수를 기준으로
            cut_size=self.win_seq - 1   #±[cut_size] 만큼 크롭
        )
        print(cropped_board)
        exit()

    def evaluate_move(self, yx_board, yx):
        '''
        * 특정 수의 좌표[yx]를 보드[yx_board]에 착수하였을 때,
        게임의 상태를 반환

        *0: during, 1: draw, 2: black win, 3: white win
        '''
        print(f'yx_board: {yx_board}')
        print(f'yx: {yx}')
        moved_yx_board = yx_board.copy()
        moved_yx_board.append(yx)

        print(self.evaluate_board(yx_board=moved_yx_board))