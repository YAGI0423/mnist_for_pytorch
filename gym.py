import model
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard

import numpy as np

#해결 필요 문제======
#End=================

board_size = 3
win_seq = 3
board = GameBoard()
rule = Rule(board_size=board_size, win_seq=win_seq)
databook = DataBook()
agent = model.AlphaO(board_size, rule, round_num=100)


now_board = board.get_board()

while rule.game_status(now_board)['during']:
    print("=" * 100)
    print(Util.seq_to_square(now_board, board_size))

    print('\nnow turn: ', end='')
    print('Black') if Util.now_turn(now_board) else print('White')

    act = agent.act(now_board)
    act_loc = act['xy_loc']

    board.put_stone(*act_loc)

    databook.add_data(act)

    print(f'\nact loc: {act_loc}\n\n')
    now_board = board.get_board()

win_code = rule.game_status(now_board)['win']
print('winner:', win_code)

turn_count = len(now_board)
value_y = [0.] * turn_count

if win_code < 2:
    for idx in range(turn_count):
        value_y[idx] = float(win_code == (idx % 2))
