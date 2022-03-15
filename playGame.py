import model
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np

#해결 필요 문제======
# 차례 넘기기 규칙
#End=================

board_size = 3
win_seq = 3
board = GameBoard()
rule = Rule(board_size=board_size, win_seq=win_seq)

player_info = {
    'black': model.AlphaO(board_size, rule),
    'white': model.AlphaO(board_size, rule)
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

    act_loc = now_player.act(now_board)
    board.put_stone(*act_loc)

    print(f'\nact loc: {act_loc}\n\n')
    now_board = board.get_board()

print('winner:', rule.game_status(now_board)['win'])
