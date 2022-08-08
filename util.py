import math
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
    def rotate_yx_list(yx_list: list, rotate_radian: float, origin_yx=(0, 0)):
        '''
        * 좌표 리스트[yx_list]를 원점[origin_yx]를 기준으로,
        * 특정 각도[rotate_radian] 만큼 회전한 리스트를 반환
        '''
        
        #좌표 yx의 type 저장 및 체크
        if type(yx_list[0]) is list:
            return_type = list
        elif type(yx_list[0]) is tuple:
            return_type = tuple
        else:
            raise Exception(f'yx type must be `list` or `tuple`')

        sin, cos = round(math.sin(rotate_radian)), round(math.cos(rotate_radian))
        R = ((cos, sin), (-sin, cos))   #회전 변환 행렬

        yx_list_moved_origin = list(    #설정한 좌표를 원점으로 설정
            [y-origin_yx[0], x-origin_yx[1]] for y, x in yx_list
        )
       
        rotated_yx_list = list( #회전된 yx 리스트
            return_type(np.dot(R, yx) + origin_yx) for yx in yx_list_moved_origin
        )
        return rotated_yx_list
            
