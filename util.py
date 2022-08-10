import math
import statistics
import numpy as np

class Util:
    @staticmethod
    def get_current_color(yx_board):
        '''
        * 좌표 보드를 입력받아 현재 시점에서 착수할 플레이어 돌 색을 반환한다.
        * 0: 흑, 1: 백
        '''
        return len(yx_board) % 2

    @classmethod
    def get_last_color(cls, yx_board):
        '''
        * 좌표 보드를 입력받아 마지막 수의 플레이어 돌 색을 반환한다.
        * 0: black, 1: white
        ※ `get_current_color` 메소드와 구분할 것
        '''
        current_color = cls.get_current_color(yx_board)
        return (current_color + 1) % 2

    @staticmethod
    def get_idx_color(move_idx):
        '''
        * 착수 순서[move_idx]를 입력받아 해당 플레이어 돌 색을 반환한다.
        * 0: black, 1: white
        '''
        return move_idx % 2

    @staticmethod
    def rotate_yx_list(yx_list: list, rotate_degree: int, origin_yx=(0, 0)):
        '''
        * 좌표 리스트[yx_list]를 원점[origin_yx]를 기준으로,
        * 특정 각도[rotate_radian] 만큼 회전한 리스트를 반환
        '''

        def scaling_rotated_yx(rotated_yx):
            '''
            *회전 후, 행렬 스케일링
            '''
            y, x = rotated_yx
            if abs(y) == abs(x):
                y, x = math.ceil(y), math.ceil(x)
                return (y, x)

            y, x = math.trunc(y), math.trunc(x)
            return (y, x)
        
        #좌표 yx의 type 저장 및 체크
        if type(yx_list[0]) is list:
            return_type = list
        elif type(yx_list[0]) is tuple:
            return_type = tuple
        else:
            raise Exception(f'yx type must be `list` or `tuple`')

        #회전각[rotate_degree] 체크
        if rotate_degree % 45 or rotate_degree > 135:   #회전 각이 45º 단위가 아니면 예외
            raise Exception('[rotate_degree] must be 45º ~ 135º')

        ori_y, ori_x = origin_yx

        print(f'degree: {rotate_degree}')
        rotate_radian = math.radians(rotate_degree)
        sin, cos = (math.sin(rotate_radian)), (math.cos(rotate_radian))
        R = ((cos, sin), (-sin, cos))   #회전 변환 행렬

        #설정한 좌표를 원점으로 설정
        yx_list_moved_origin = list([y-ori_y, x-ori_x] for y, x in yx_list)

        rotated_yx_list = list( #회전된 yx 리스트
            np.dot(R, yx) + origin_yx for yx in yx_list_moved_origin
        )
        print(f'rotated_yx_list: {rotated_yx_list}')
        #회전 후, 행렬 스케일링
        scaled_yx_list = list(scaling_rotated_yx(yx) for yx in rotated_yx_list)

        #입력 type으로 변환
        type_yx_list = list(return_type(yx) for yx in scaled_yx_list)
        return type_yx_list
    
    @staticmethod
    def check_consecutive_is_N(yx_board, origin_yx, N: int):
        '''
        * yx 좌표 보드[yx_board]에서 특정 yx 좌표[origin_yx] 기준,
        [N]개 또는 그 이상의 연속된 돌의 존재 여부를 반환
        *True: 존재, False: 존재하지 않음
        ※ [yx_board]에는 [origin_yx]의 좌표가 존재해야함
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
                'max_y': ori_y + cut_size,
                'min_x': max(0, ori_x - cut_size),
                'max_x': ori_x + cut_size
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
        #End===================================

        print(yx_board)
        print(origin_yx)
        

        #[origin_yx] 존재 여부 확인
        if not origin_yx in yx_board:
            raise Exception(f'must [origin_yx] in [yx_board]')
        
        check_yx_color = Util.get_idx_color(yx_board.index(origin_yx))
        check_yx_board = yx_board[check_yx_color::2]    #체크할 플레이어 색의 돌만 추출

        cropped_yx_board = crop_yx_board(
            yx_board=check_yx_board,
            cut_size=N - 1,
            origin_yx=origin_yx
        )
        print(cropped_yx_board)

        for degree in (0, 45, 90, 135):
            print(f'degree: {degree}')
            rotated_yx_board = Util.rotate_yx_list(
                yx_list=cropped_yx_board, rotate_degree=degree, origin_yx=origin_yx
            )
            print(f'\trotated_yx_board: {rotated_yx_board}')
            seq_num = count_row_consecutive(cropped_yx_board=rotated_yx_board, origin_yx=origin_yx)
            
            if seq_num >= N:
                return True
        return False