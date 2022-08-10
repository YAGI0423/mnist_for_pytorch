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
        
        '''
        !!!!!현재 해당 함수는 마지막 수만 고려하여 게임을 판단함
        !!!!!좌표를 매개변수로 받아 좌표가 입력되면, 해당 좌표를 바탕으로 판단하고
        !!!!!None으로 받으면 전체를 판단하도록 구성할 필요가 있음
        '''
        #자체 함수=============================
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
        
        def count_row_consecutive(cropped_yx_board, origin_yx):
            '''
            * `크롭된 좌표 리스트`[cropped_yx_board]에서 특정 좌표[origin_yx]를 기준으로 연속된 돌의 수 반환
            * [origin_yx] 기준, `가로 방향의 연속성만 판별`
            * True: 연속적, False: 비연속적

            ※ 반드시 `크롭된 좌표 리스트`만을 입력으로 하여야 함
            '''

            def count_consecutive_from_one(loc_list):
                '''
                * 입력 리스트[loc_list]에 1부터 연속적으로 존재하는 값의 수를 반환한다
                '''
                num = 1
                while num in loc_list:
                    num += 1
                return num - 1

            ori_y, ori_x = origin_yx[0], origin_yx[1]
            
            #y 좌표가 동일한 x좌표를 기준으로 하는(같은 행에 존재하는) x 좌표 값만 추출
            horizon_x_list = list(x-ori_x for y, x in cropped_yx_board if y==ori_y)
            
            right_seq_num = count_consecutive_from_one(horizon_x_list)  #원점 제외, 우측 연속 돌 수
            reflect_x_list = list(-x for x in horizon_x_list)   #원점 기준, 좌측 돌을 우측으로 행렬변환
            left_seq_num = count_consecutive_from_one(reflect_x_list)   #원점 제외, 좌측 연속 돌 수

            total_consecutive_num = left_seq_num + 1 + right_seq_num    #원점 포함 전체 연속 돌 수
            return total_consecutive_num
        #End==================================

        #전체 돌 수가 게임 종료 가능 착수 수보다 작을 때
        if len(yx_board) < self.win_seq * 2 - 1:
            return 0    #during

        #yx board를 바로 크롭할 경우, 흑, 백에 대한 정보가 소실 된다
        #따라서, 크롭 작업 이전에 마지막 수에 해당하는 돌의 색만 필터링할 필요가 있다
        last_color = Util.get_last_color(yx_board)
        print(f'last_turn: {last_color}')
        main_yx_board = yx_board[last_color::2]    #마지막 수의 플레이어 돌만 추출

        print(f'last_yx_board: {main_yx_board}')

        last_yx = yx_board[-1]  #마지막 수의 yx 좌표

        cropped_yx_board = crop_yx_board(
            yx_board=main_yx_board,
            cut_size=self.win_seq - 1,
            origin_yx=last_yx
        )
        print(f'cropped_board: {cropped_yx_board}')

        #회전 및 연속성 체크
        for degree in (0, 45, 90, 135):
            print(f'degree: {degree}')
            rotated_yx_board = Util.rotate_yx_list(
                yx_list=cropped_yx_board, rotate_degree=degree, origin_yx=last_yx
            )
            print(f'\trotated_yx_board: {rotated_yx_board}')
            seq_num = count_row_consecutive(cropped_yx_board=rotated_yx_board, origin_yx=last_yx)
            print(f'\tseq_num: {seq_num}')

            if seq_num >= self.win_seq:
                return 2 + last_color   #black win: 2, white win: 3
       
        #착수 돌 수가 보드 전체를 채웠을 때
        if len(yx_board) == self.win_seq:
            return 1    #draw
        return 0    #during

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