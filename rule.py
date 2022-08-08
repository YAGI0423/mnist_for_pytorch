from util import Util

import math
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
        
        def crop_yx_board(yx_board, origin_yx, cut_size: int):
            '''
            * [yx_board]를 특정 좌표[origin_yx]를 기준으로 [cut_size] 만큼 크롭하여 반환
            '''

            def is_in_crop_range(yx, min_y: int, max_y: int, min_x: int, max_x: int):
                '''
                * (y, x) 좌표[yx]가 크롭 범위인 [min_y], ~ [max_x] 내부에 있는지 여부 반환
                * True: 해당 좌표[yx]가 크롭 범위 내에 있음,
                * False: 크롭 범위 외부에 있음
                '''
                y, x = yx
                if y < min_y or max_y < y: return False;
                if x < min_x or max_x < x: return False;
                return True
            
            ori_y, ori_x = origin_yx
            crop_range_args = {
                'min_y': max(0, ori_y - cut_size),
                'max_y': min(self.board_size - 1, ori_y + cut_size),
                'min_x': max(0, ori_x - cut_size),
                'max_x': min(self.board_size - 1, ori_x + cut_size)
            }

            cropped_yx_board = list(    #크롭 범위 내 좌표만 필터링한 리스트
                yx for yx in yx_board if is_in_crop_range(yx, **crop_range_args)
            )
            return cropped_yx_board
        #End==================================

        #전체 돌 수가 게임 종료 가능 착수 수보다 작을 때
        if len(yx_board) < self.win_seq * 2 - 1:
            return 0

        #yx board를 크롭할 경우, 흑, 백에 대한 정보가 소실 된다
        #따라서, 크롭 작업 이전에 마지막 수에 해당하는 돌의 색만 필터링할 필요가 있다

        cropped_board = crop_yx_board(
            yx_board=yx_board,
            cut_size=self.win_seq - 1,
            origin_yx = yx_board[-1]
        )
        print(cropped_board)

        rotate_radian = math.radians(45)
        print(Util.rotate_yx_list(
            yx_list=cropped_board, rotate_radian=rotate_radian, origin_yx=yx_board[-1]
        ))
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
        #기존 보드에 평가하고자 하는 수의 좌표를 추가하여 평가
        moved_yx_board = yx_board.copy()
        moved_yx_board.append(yx)

        print(self.evaluate_board(yx_board=moved_yx_board))