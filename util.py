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
    def rotate_yx_list(yx_list: list, rotate_degree: int, origin_yx=(0, 0)):
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

        #회전각[rotate_degree] 체크
        if rotate_degree % 45 or rotate_degree > 135:   #회전 각이 45º 단위가 아니면 예외
            raise Exception('[rotate_degree] must be 45º ~ 135º')

    
        rotate_radian = math.radians(rotate_degree)
        sin, cos = round(math.sin(rotate_radian)), round(math.cos(rotate_radian))
        R = ((cos, sin), (-sin, cos))   #회전 변환 행렬

        yx_list_moved_origin = list(    #설정한 좌표를 원점으로 설정
            [y-origin_yx[0], x-origin_yx[1]] for y, x in yx_list
        )
       
        rotated_yx_list = list( #회전된 yx 리스트
            return_type(np.dot(R, yx) + origin_yx) for yx in yx_list_moved_origin
        )
        return rotated_yx_list
            
