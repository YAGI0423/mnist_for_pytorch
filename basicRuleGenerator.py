from util import Util
from rule import Rule

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
        

        seq_num += 2   #양 쪽 위치를 함께 반환하기 위해 +2

        if rotate_degree == 0:   #회전 없을 시 그대로 반환
            seq_yx_list = [[0, x] for x in range(-1, seq_num-1)]   #회전되지 않은 yx 리스트
            side_yx_list = list(seq_yx_list.pop(pop_idx) for pop_idx in (0, -1))   #양 끝 yx 추출
            return seq_yx_list, side_yx_list

        #중심을 기준으로 회전하기 위한 돌의 위치 yx 리스트
        seq_yx = list([0, x] for x in range(seq_num))

        rotate_radian = math.radians(rotate_degree)

        rot_seq_yx_list = Util.rotate_yx_list(yx_list=seq_yx, rotate_degree=rotate_degree)
        rot_seq_yx_list -= np.min(rot_seq_yx_list, axis=0)   #y와 x 각각의 최소값을 튜플로 반환 e.g. (y_min, x_min)
        
        sin, cos = round(math.sin(rotate_radian)), round(math.cos(rotate_radian))
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

    def get_able_move_yx_list(self, disable_yx_list: list=[]):
        '''
        * 보드에서 불가능한 좌표인 [disable_yx_list]의 좌표들을 제외한 가능한 yx 좌표 리스트를 반환
        '''
        able_move_yx_list = list ()
        for y in range(self.board_size):
            for x in range(self.board_size):
                yx = (y, x)
                if not yx in disable_yx_list:
                    able_move_yx_list.append(yx)
        return able_move_yx_list

    def return_current_player(self, current_turn, black, white):
        '''
        * 현재 플레이어 순서[current_turn]를 토대로 흑 또는 백 플레이어 반환
        '''
        return white if current_turn else black

    def noise_rate_to_num(self, noise_rate: float, disable_num: int=0):
        '''
        * [noise_rate]에 해당하는 noise 돌의 수를 반환
        * [disable_num]은 사전에 예약된 수로, 이를 제외하고 noise 돌 수를 계산
        '''
        noise_num = self.board_size ** 2
        noise_num -= disable_num
        noise_num = round(noise_num * noise_rate)
        noise_num -= (noise_num + 1) % 2    #노이즈 돌 개수는 반드시 홀수여야함
        return noise_num

    def attack_four(self, noise_rate: float, size: int):
        '''
        현재 플레이어 돌이 막히지 않고 4개 연속 이어져있음, 
        5개가 되는 위치에 각각 0.5 할당, 
        z = 1
        '''
        
        test = [(0, 0), (0, 1), (0, 2)]
        print(test)

        rotated_test = Util.rotate_yx_list(yx_list=test, rotate_degree=45, origin_yx=(0, 0))
        
        print(rotated_test)

        print()
        test = [(0, 0), (1, 1), (2, 2)]
        print(test)

        rotated_test = Util.rotate_yx_list(yx_list=test, rotate_degree=45, origin_yx=(0, 0))
        print(rotated_test)

        print()
        test = [(0, 0), (1, 0), (2, 0)]
        print(test)

        rotated_test = Util.rotate_yx_list(yx_list=test, rotate_degree=45, origin_yx=(0, 0))
        print(rotated_test)

        print()
        test = [(0, 0), (1, -1), (2, -2)]
        print(test)

        rotated_test = Util.rotate_yx_list(yx_list=test, rotate_degree=45, origin_yx=(0, 0))
        print(rotated_test)
        exit()

        if noise_rate < 0 or 0.8 < noise_rate:  #[noise_rate] 제한 0 ~ 0.8
            raise Exception(f'[noise_rate] must be 0 ~ 0.8')

        SEQUENCE_NUM = 4
        LIMIT_SIDE_NUM = 1  #최소 side space
        NOISE_SEQ_LIMIT = 3 #노이즈 수의 연속성 제한
        
        main_color = np.random.randint(0, 2) #흑: 0, 백: 1
        rot_degree = np.random.choice((0, 45, 90, 135))


        print(f'degree: {rot_degree}')
        seq_yx_list, side_yx_list = self.get_seq_yx_list(seq_num=SEQUENCE_NUM, rotate_degree=rot_degree)
        y_limit, x_limit = self.get_limit_loc(seq_yx_list=seq_yx_list)  #이동 가능한 최대 yx 좌표
        move_yx = (np.random.randint(0, y_limit + 1), np.random.randint(0, x_limit + 1))  #이동 좌표 무작위 선택

        #seq 필터 및 사이드 yx 좌표 이동하기
        seq_yx_list = np.add(seq_yx_list, move_yx).tolist()
        side_yx_list = np.add(side_yx_list, move_yx).tolist()
        
        #유효 좌표 필터링 및 yx 좌표 튜플 변환
        seq_yx_list = list(tuple(yx) for yx in seq_yx_list)
        side_yx_list = list(tuple(yx) for yx in side_yx_list if not self.is_out_loc(yx))  #보드에 위치한 yx만 추출

        if len(side_yx_list) < LIMIT_SIDE_NUM: #최소 side space 개수가 확보되지 않으면 continue
            print('CONTINUE')
            exit()

        
        yx_board = list()  #state로 데이터셋에 추가될 보드
        
        #착수 가능한 yx 좌표 리스트
        able_yx_list = self.get_able_move_yx_list(disable_yx_list=seq_yx_list + side_yx_list)
        np.random.shuffle(able_yx_list)   #착수 가능 좌표 섞기

        print(f'current_color: {main_color}')

        #main_color에 따른 흑, 백 플레이어 좌표 리스트 할당하기
        black_yx_list = self.return_current_player(current_turn=main_color, black=seq_yx_list, white=able_yx_list)
        white_yx_list = self.return_current_player(current_turn=not main_color, black=seq_yx_list, white=able_yx_list)
        
        #basic rule 착수하기
        while seq_yx_list:  #seq_yx_list의 yx를 소진할때 까지 반복
            current_turn = Util.get_current_color(yx_board)  #현재 플레이어 돌 색 얻기
            current_yx_list = self.return_current_player(  #현재 플레이어 yx_list 반환
                current_turn=current_turn,
                black=black_yx_list,
                white=white_yx_list
            )
            move_yx = current_yx_list.pop() #좌표 yx 추출

            #착수 가능 수인지 확인 필요   
            # if current_turn != main_color:

            concat_yx_board = yx_board.copy()
            concat_yx_board.append(move_yx)

            is_consecutive = Util.check_consecutive_is_N(
                yx_board=concat_yx_board, origin_yx=move_yx, N=NOISE_SEQ_LIMIT
            )
            print(is_consecutive)
                # if seq_num >= NOISE_SEQ_LIMIT:
                #     print('NONO')
                #     exit()
                #     continue
            

            yx_board.append(move_yx)
        print(yx_board)
        exit()
        
        
        print(f'now board: {yx_board}')
        noise_num = self.noise_rate_to_num(  #[noise_rate]에 따른 noise 돌 수
            noise_rate=noise_rate,
            disable_num=len(yx_board) + len(side_yx_list)   #사전에 예약된 수(move)
        )
        
        #noise stone 착수하기
        noise_stone_num = 0
        while noise_stone_num < noise_num:
            move_yx = able_yx_list.pop()

            #착수 가능 수인지 확인 필요
            #---
            yx_board.append(move_yx)
            noise_stone_num += 1
        
        print(yx_board)
        # print(able_yx_board)
        exit()


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
    gen.attack_four(noise_rate=0.2, size=10)

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