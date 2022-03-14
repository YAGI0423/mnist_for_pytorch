import model
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np

#해결 필요 문제======

#End=================

board_size = 4
win_seq = 3
player_info = {
    'black': model.User(board_size),
    'white': model.User(board_size)
}

board = GameBoard()
rule = Rule(board_size=board_size, win_seq=win_seq)


now_board = board.get_board()

while rule.game_status(now_board)['during']:
    print("=" * 100)
    print(Util.seq_to_square(now_board, board_size))

    now_turn = Util.now_turn(now_board)
    now_player = player_info['black'] if now_turn else player_info['white']

    status = {
        'seq_xy_board': now_board,
        'able_loc': rule.get_able_loc(now_board)
    }

    print('\nnow turn: ', end='')
    print('Black') if now_turn else print('White')

    act_loc = now_player.act(status)
    board.put_stone(*act_loc)

    print(f'\nact loc: {act_loc}\n\n')
    now_board = board.get_board()

print('winner:', rule.game_status(now_board)['win'])
