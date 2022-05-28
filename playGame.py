import os

import model
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np

class playGame:
    def __init__(
            self,
            board_size, win_seq
        ):

        self.board_size = board_size
        self.rule = Rule(board_size=board_size, win_seq=win_seq)
        

    def play(self, black, white, databook, diri_TF=False):
        def get_value_y(seq_xy_board, win_code, discount_factor):
            turn_count = len(seq_xy_board)
            value_y = [0.] * turn_count

            if win_code < 2:
                for idx in range(turn_count):
                    value_y[idx] = float(win_code == (idx % 2)) * 2 - 1

                #discount factor
                gamma = 1.
                for idx in range(turn_count):
                    value_y[idx] *= gamma

                    if idx % 2:
                        gamma *= discount_factor
            return tuple(value_y)

        board = GameBoard()
        now_board = board.get_board()

        while self.rule.game_status(now_board)['during']:
            print("=" * 100)
            print(Util.seq_to_square(now_board, self.board_size))

            now_turn = Util.now_turn(now_board)
            now_player = black if now_turn else white

            print('\nnow turn: ', end='')
            print('Black') if now_turn else print('White')

            act = now_player.act(now_board, diri_TF)
            act_loc = act['xy_loc']

            board.put_stone(*act_loc)

            databook.add_data(act)

            print(f'\nact loc: {act_loc}\n\n')
            now_board = board.get_board()

            #when repeat pass stone
            if now_board[-4:].count((0, self.board_size)) >= 4:
                loc = list(self.rule.get_able_loc(now_board))
                loc.remove((None, None))
                loc.remove((0, self.board_size))

                board.put_stone(*loc[0])
                now_board = board.get_board()

        win_code = self.rule.game_status(now_board)['win']

        print('winner:', win_code, end='\n\n')

        value_y = get_value_y(now_board, win_code, discount_factor=1.)
        databook.add_data({'value_y': value_y})

        return win_code


# def get_main_agent_dir():
#     main_root = './model/main_model/'
#     model_list = os.listdir(main_root)
#     if model_list:   #Exist
#         return main_root + model_list[0]
#     return None   #Empty


# #해결 필요 문제======
# #End=================

# board_size = 10
# win_seq = 5
# board = GameBoard()
# rule = Rule(board_size=board_size, win_seq=win_seq)


# player_info = {
#     'black': model.AlphaO(board_size, rule, model_dir=get_main_agent_dir(), round_num=1024),
#     'white': model.User(board_size, rule)
# }

# now_board = board.get_board()

# while rule.game_status(now_board)['during']:
#     print("=" * 100)
#     print(Util.seq_to_square(now_board, board_size))
#     print(board.get_board())

#     now_turn = Util.now_turn(now_board)
#     now_player = player_info['black'] if now_turn else player_info['white']

#     print('\nnow turn: ', end='')
#     print('Black') if now_turn else print('White')

#     act_loc = now_player.act(now_board, diri_TF=False)['xy_loc']
#     board.put_stone(*act_loc)

#     print(f'\nact loc: {act_loc}\n\n')
#     now_board = board.get_board()

# print('winner:', rule.game_status(now_board)['win'])
