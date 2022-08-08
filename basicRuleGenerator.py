import math
import numpy as np


class Generator:
    def __init__(self, board_size: int):
        self.board_size = board_size

    def get_seq_yx_list(self, seq_num: int, rotate_degree: int=0):
        '''
        * [rotate_degree]만큼 회전된 [seq_num]개가 한 줄인 돌의 위치 yx 리스트 반환
        * 끝 단의 위치도 함께 반환

        * [rotate_degree] = 0: oooo
        '''
        
        if rotate_degree % 45 or rotate_degree > 135:   #회전 각이 45º 단위가 아니면 예외
            raise Exception('[rotate_degree] must be 45º ~ 135º')

        seq_num += 2   #양 쪽 위치를 함께 반환하기 위해 +2
        center_loc = int(seq_num / 2)

        if rotate_degree == 0:   #회전 없을 시 그대로 반환
            seq_yx_list = [[0, x] for x in range(-1, seq_num)]   #회전되지 않은 yx 리스트
            side_yx_list = list(seq_yx_list.pop(pop_idx) for pop_idx in (0, -1))   #양 끝 yx 추출
            return seq_yx_list, side_yx_list

        #중심을 기준으로 회전하기 위해 y,x에서 [center_loc] 만큼 차감한 돌의 위치 yx 리스트
        seq_yx = [(0, x) for x in range(seq_num)]

        rot_radian = math.radians(rotate_degree)
        sin, cos = round(math.sin(rot_radian)), round(math.cos(rot_radian))
        R = ((cos, sin), (-sin, cos))   #회전 변환 행렬

        rot_seq_yx_list = [list(np.dot(R, yx)) for yx in seq_yx]   #회전된 yx 리스트
        
        #회전한 yx 좌표를 원점(0, 0) 기준에 맞추어 정렬
        rot_seq_yx_list -= np.min(rot_seq_yx_list, axis=0)   #y와 x 각각의 최소값을 튜플로 반환 e.g. (y_min, x_min)
        rot_seq_yx_list -= (abs(sin), abs(cos)) #회전된 yx의 좌표 범위가 -1 ~ [seq_num]이 되도록 수정
        rot_seq_yx_list = rot_seq_yx_list.tolist()

        side_yx_list = list(rot_seq_yx_list.pop(pop_idx) for pop_idx in (0, -1))   #양 끝 yx 추출
        return rot_seq_yx_list, side_yx_list

    def get_limit_loc(self, seq_yx_list):
        '''
        * 게임 보드에서 sequance YX 필터가 이동 가능한 최대 Y, X 좌표를 반환
        '''
        height, width =  np.max(seq_yx_list, axis=0)
        y_limit = self.board_size - height - 1  #이동 가능한 최대 x 좌표
        x_limit = self.board_size - width - 1   #이동 가능한 최대 y 좌표
        return y_limit, x_limit

    def is_out_loc(self, yx):
        '''
        * [yx] 좌표가 게임 보드 내에 위치 하였는지 boolean 형태로 반환
        * True: 게임 보드 외부에 위치
        * False: 게임 보드 내부에 위치
        '''
        for loc in yx:
            if loc < 0: return True;
            if loc >= self.board_size: return True;
        return False

    def attack_four(self, noise_rate: float, size: int):
        '''
        현재 플레이어 돌이 막히지 않고 4개 연속 이어져있음, 
        5개가 되는 위치에 각각 0.5 할당, 
        z = 1
        '''
        SEQUENCE_NUM = 4
        LIMIT_SIDE_NUM = 1  #최소 side space

        rot_degree = np.random.choice((0, 45, 90, 135))
        print(f'degree: {rot_degree}')
        seq_yx_list, side_yx_list = self.get_seq_yx_list(seq_num=SEQUENCE_NUM, rotate_degree=rot_degree)
        y_limit, x_limit = self.get_limit_loc(seq_yx_list=seq_yx_list)  #이동 가능한 최대 yx 좌표

        move_yx = (np.random.randint(0, y_limit + 1), np.random.randint(0, x_limit + 1))  #위치 좌표 뮈작위 선택

        seq_yx_list = np.add(seq_yx_list, move_yx).tolist() #seq 필터 및 사이드 yx 좌표 이동하기
        side_yx_list = np.add(side_yx_list, move_yx).tolist()

        side_yx_list = list(yx for yx in side_yx_list if not self.is_out_loc(yx))  #보드에 위치한 yx 필터링

        if len(side_yx_list) < LIMIT_SIDE_NUM: #최소 side space 개수가 확보되지 않으면 continue
            print('CONTINUE')
    
        print(seq_yx_list)
        print(side_yx_list)

        #착수 가능한 좌표 리스트를 바탕으로 noise 수 두기
        #1. current player 선정
        #2. nose 개수 정의
        #3. win_seq 만큼 상호 착수 수행
        #4. 착수 전, 체크
        disable_yx_list = seq_yx_list + side_yx_list

        able_yx_list = list(
            [y, x] for x in range(self.board_size) for y in range(self.board_size) if not [y, x] in disable_yx_list
        )

        board = list()
        # print(able_yx_board)
        exit()

        # able_yx_board = []
        # for y in range(self.board_size):
        #     for x in range(self.board_size):
        #         if not (y, x) in seq_yx_list:
        #             if not (y, x) in side_yx_list:
        #                 able_yx_board.append((y, x))
        # print(seq_yx_list)
        # print(side_yx_list)

        # print(empty_yx_board)
        exit()



        #선택된 y, x만큼 filter 좌표 이동하기


        #degree: 0
        #degree: 45
        #degree: 90
        #degree: 135
        exit()

        # current_player_list = np.random.choice([-1, +1], size=size)
        # seq_stone_ch = np.zeros((self.win_seq, self.win_seq))
        # seq_stone_ch[base] += 1.

        

        # print(seq_stone_ch)
        # xy = tuple(tuple((x-base, y-base) for x in range(self.win_seq)) for y in range(self.win_seq))
        
        # print(xy)

        # rot_array = np.array([[[[1, -1], [1, 1]]]])
        # rot_array = np.tile(rot_array, reps=[3, 3, 1, 1])


        # print(rot_array)
        # print(rot_array.shape)
        # print(np.dot(rot_array, xy) + base)
        # exit()

        # for player in current_player_list:
        #     print(player)

    def defend_four(self, noise_rate, size):
        pass

    def attack_three(self, noise_rate, size):
        pass

    def defend_three(self, noise_rate, size):
        pass

    def attack_space_three(self, noise_rate, size):
        pass

    def defend_space_three(self, noise_rate, size):
        pass
    



if __name__ == '__main__':
    gen = Generator(board_size=7)
    gen.attack_four(noise_rate=1, size=10)

    #현재 플레이어 돌이 막히지 않고 4개 연속 이어져있음. 5개가 되는 위치에 각각 0.5 할당. 승률 1
    # print(gen.generate_live_4_attack(1).get_sample(1.))
    

    #적 플레이어 돌이 막히지 않고 4개 연속 이어져있음. 5개가 되는 위치에 각각 0.5 할당. 승률 -1
    # obs, color, last_move, pi, z = gen.generate_live_4_defend(1).get_sample(1.)
    # print(obs, color, last_move, np.array(pi).reshape(15, 15), z)


    #현재 플레이어 돌이 막히지 않고 3개 연속 이어져있음. 4개가 되는 위치에 각각 0.5 할당. 승률 1
    # obs, color, last_move, pi, z = gen.generate_live_3_ooo_attack(1).get_sample(1.)
    # print(obs, end='\n\n')
    # print(np.array(pi).reshape(15, 15), end='\n\n')
    # print(color, end='\n\n')
    # print(last_move, end='\n\n')
    # print(z, end='\n\n')


    #적 플레이어 돌이 막히지 않고 3개 연속 이어져있음. 4개가 되는 위치에 각각 0.5 할당. 승률 0
    # obs, color, last_move, pi, z = gen.generate_live_3_ooo_defend(1).get_sample(1.)
    # print(obs, end='\n\n')
    # print(np.array(pi).reshape(15, 15), end='\n\n')
    # print(color, end='\n\n')
    # print(last_move, end='\n\n')
    # print(z, end='\n\n')
   
    #현재 플레이어 돌이 00_0 형태로 되어있음. 4개가 되는 위치에 각각 1 할당. 승률 1
    # obs, color, last_move, pi, z = gen.generate_live_3_oo_o_attack(1).get_sample(1.)
    # print(obs, end='\n\n')
    # print(np.array(pi).reshape(15, 15), end='\n\n')
    # print(color, end='\n\n')
    # print(last_move, end='\n\n')
    # print(z, end='\n\n')

    #적 플레이어 돌이 00_0 형태로 되어있음. 비어있는 중앙 0.5, 양쪽 0.25 할당. 승률 0
    # obs, color, last_move, pi, z = gen.generate_live_3_oo_o_defend(1).get_sample(1.)
    # print(obs, end='\n\n')
    # print(np.array(pi).reshape(15, 15), end='\n\n')
    # print(color, end='\n\n')
    # print(last_move, end='\n\n')
    # print(z, end='\n\n')