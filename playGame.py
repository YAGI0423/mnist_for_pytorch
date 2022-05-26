import os

import model
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np


def get_main_agent_dir():
    main_root = './model/main_model/'
    model_list = os.listdir(main_root)
    if model_list:   #Exist
        return main_root + model_list[0]
    return None   #Empty


#해결 필요 문제======
#End=================

board_size = 10
win_seq = 5
board = GameBoard()
rule = Rule(board_size=board_size, win_seq=win_seq)


player_info = {
    'black': model.AlphaO(board_size, rule, model_dir=get_main_agent_dir(), round_num=1024),
    'white': model.User(board_size, rule)
}

now_board = board.get_board()

while rule.game_status(now_board)['during']:
    print("=" * 100)
    print(Util.seq_to_square(now_board, board_size))
    print(board.get_board())

    now_turn = Util.now_turn(now_board)
    now_player = player_info['black'] if now_turn else player_info['white']

    print('\nnow turn: ', end='')
    print('Black') if now_turn else print('White')

    act_loc = now_player.act(now_board, diri_TF=False)['xy_loc']
    board.put_stone(*act_loc)

    print(f'\nact loc: {act_loc}\n\n')
    now_board = board.get_board()

print('winner:', rule.game_status(now_board)['win'])
