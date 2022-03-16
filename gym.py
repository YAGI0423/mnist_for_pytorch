import model
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np

#해결 필요 문제======
#End=================

board_size = 3
win_seq = 3
board = GameBoard()
rule = Rule(board_size=board_size, win_seq=win_seq)

agent = model.AlphaO(board_size, rule, round_num=500)

player_info = {
    'black': agent,
    'white': agent
}

now_board = board.get_board()

while rule.game_status(now_board)['during']:
    print("=" * 100)
    print(Util.seq_to_square(now_board, board_size))

    now_turn = Util.now_turn(now_board)
    now_player = player_info['black'] if now_turn else player_info['white']

    print('\nnow turn: ', end='')
    print('Black') if now_turn else print('White')

    act_loc = now_player.act(now_board)['xy_loc']
    board.put_stone(*act_loc)

    print(f'\nact loc: {act_loc}\n\n')
    now_board = board.get_board()

print('winner:', rule.game_status(now_board)['win'])
