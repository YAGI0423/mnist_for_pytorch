import math
import numpy as np

class Util:
    @staticmethod
    def get_current_color(yx_board):
        '''
        * 좌표 보드를 입력받아 현재 시점에서 착수할 플레이어 돌 색을 반환한다.
        * 0: 흑, 1: 백
        '''
        return len(yx_board) % 2

    @staticmethod
    def get_move_idx_to_color(move_idx):
        '''
        * 착수 순서[move_idx]를 입력받아 해당 플레이어 돌 색을 반환한다.
        * 0: black, 1: white
        '''
        return move_idx % 2

    @staticmethod
    def translate_matrix(yx_list, origin_yx):
        '''
        * yx 좌표 리스트[yx_list]의 원점을 특정 좌표[origin_yx]로 행렬이동
        '''
        ori_y, ori_x = origin_yx
        return list((y-ori_y, x-ori_x) for y, x in yx_list)

    @staticmethod
    def rotate_yx_list(yx_list: list, rotate_degree: int, origin_yx=(0, 0)):
        '''
        * 좌표 리스트[yx_list]를 원점[origin_yx]를 기준으로,
        * 특정 각도[rotate_radian] 만큼 회전한 리스트를 반환
        '''

        def rotate_matrix(yx_list, degree):
            '''
            * 원점 (0, 0)을 기준으로 각도[degree]만큼 시계 반향으로 회전
            '''
            def dot_product(A, B):
                '''
                * A와 B를 행렬곱한 후, 정수로 변환하여 반환한다
                '''
                X = np.dot(A, B)
                X = np.round(X).astype(int)
                return tuple(X)

            rotate_radian = math.radians(degree)
            sin, cos = math.sin(rotate_radian), math.cos(rotate_radian)
            R = ((cos, sin), (-sin, cos))   #회전 변환 행렬

            return list(dot_product(R, yx) for yx in yx_list)
        
        #좌표 yx의 type 저장 및 체크
        if type(yx_list[0]) is list:
            return_type = list
        elif type(yx_list[0]) is tuple:
            return_type = tuple
        else:
            raise Exception(f'yx type must be `list` or `tuple`')

        #회전각[rotate_degree] 체크
        if not rotate_degree in (0, 90, 180, 270):   #회전 각이 45º 단위가 아니면 예외
            raise Exception('[rotate_degree] must be 0º, 90º, 180º, 270º')

        ori_y, ori_x = origin_yx
        return_yx = Util.translate_matrix(yx_list=yx_list, origin_yx=origin_yx)   #좌표 원점 이동
        return_yx = rotate_matrix(yx_list=return_yx, degree=rotate_degree)    #원점 기준 회전
        return_yx = Util.translate_matrix(yx_list=return_yx, origin_yx=(-ori_y, -ori_x))
        return list(return_type(yx) for yx in return_yx)
    
    @staticmethod
    def check_consecutive_is_N(yx_board, origin_yx, N: int, yx_color=None):
        '''
        * yx 좌표 보드[yx_board]에서 특정 yx 좌표[origin_yx] 기준,
        [N]개 또는 그 이상의 연속된 돌의 존재 여부를 반환
        *True: 존재, False: 존재하지 않음

        *만약 [yx_board] 내부에 [origin_yx] 위치의 수가 없으면,
        [origin_yx] 수의 플레이어 색[yx_color]에 따라 연속성 확인
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

            ori_y, ori_x = origin_yx
            
            #y 좌표가 동일한 x좌표를 기준으로 하는(같은 행에 존재하는) x 좌표 값만 추출
            horizon_x_list = list(x-ori_x for y, x in cropped_yx_board if y==ori_y)
            
            right_seq_num = count_consecutive_from_one(horizon_x_list)  #원점 제외, 우측 연속 돌 수
            reflect_x_list = list(-x for x in horizon_x_list)   #원점 기준, 좌측 돌을 우측으로 행렬변환
            left_seq_num = count_consecutive_from_one(reflect_x_list)   #원점 제외, 좌측 연속 돌 수

            total_consecutive_num = left_seq_num + 1 + right_seq_num    #원점 포함 전체 연속 돌 수
            return total_consecutive_num
        
        def count_diagonal_consecutive(cropped_yx_board, origin_yx):
            '''
            * `크롭된 좌표 리스트`[cropped_yx_board]에서 특정 좌표[origin_yx]를 기준으로 45º 대각선 연속된 돌의 수 반환
            * [origin_yx] 기준, `45º 대각선 방향의 연속성만 판별`
            * True: 연속적, False: 비연속적

            ※ 반드시 `크롭된 좌표 리스트`만을 입력으로 하여야 함
            '''
            # 특정 좌표[origin_yx]를 원점(0, 0)으로 행렬 이동
            return_yx = Util.translate_matrix(yx_list=cropped_yx_board, origin_yx=origin_yx)
            
            #y를 모두 0으로 통일하여 같은 행으로 위치
            return_yx = list((0, x) for y, x in return_yx if -y == x)
            seq_num = count_row_consecutive(cropped_yx_board=return_yx, origin_yx=(0, 0))
            return seq_num
        #End===================================

        check_yx_board = yx_board.copy()

        #[origin_yx] 존재 여부 확인
        if not origin_yx in check_yx_board:
            if yx_color is None:
                raise Exception(f'If [origin_yx] not in [yx_board], must input [yx_color]')
            current_color = Util.get_current_color(check_yx_board)
            if yx_color == current_color:
                check_yx_board.append(origin_yx)
            else:
                check_yx_board.extend(((999, 999), origin_yx))
        
        check_yx_color = Util.get_move_idx_to_color(check_yx_board.index(origin_yx))
        check_yx_board = check_yx_board[check_yx_color::2]    #체크할 플레이어 색의 돌만 추출

        cropped_yx_board = crop_yx_board(
            yx_board=check_yx_board, cut_size=N - 1, origin_yx=origin_yx
        )

        for degree in (0, 90):
            rotated_yx_board = Util.rotate_yx_list(
                yx_list=cropped_yx_board, rotate_degree=degree, origin_yx=origin_yx
            )
            seq_num = count_row_consecutive(cropped_yx_board=rotated_yx_board, origin_yx=origin_yx)
            if seq_num >= N:
                return True #N만큼 연속된 돌 존재

            seq_num = count_diagonal_consecutive(cropped_yx_board=rotated_yx_board, origin_yx=origin_yx)
            if seq_num >= N:
                return True #N만큼 연속된 돌 존재
        return False

    @staticmethod
    def yx_board_to_state(yx_board, main_color: int, board_size: int):
        '''
        * yx 좌표로 이루어진 보드[yx_board]를 모델에 입력 가능한 형태[state]로 변환하여 반환
        '''
        black_yx_list = yx_board[::2]   #흑돌 좌표만 필터링
        white_yx_list = yx_board[1::2]  #백돌 좌표만 필터링
        last_y, last_x = yx_board[-1]  #마지막 수의 좌표

        square_board = np.zeros(shape=(board_size, board_size, 3), dtype=np.float32)
        

        for y, x in black_yx_list:
            square_board[y][x][main_color] = 1.
        
        for y, x in white_yx_list:
            square_board[y][x][int(not main_color)] = 1.
        
        square_board[last_y][last_x][2] = 1.
        return square_board

    @staticmethod
    def yx_to_idx(yx, board_size: int):
        '''
        *좌표 보드[yx_board]를 입력받아 1차원 좌표 idx로 반환
        '''
        y, x = yx
        return y * board_size + x