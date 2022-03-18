import model
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard

import numpy as np

#function============
def play_game(board_size, win_seq, play_num, rule, agent):

    def get_value_y(seq_xy_board, win_code):
        turn_count = len(seq_xy_board)
        value_y = [0.] * turn_count

        if win_code < 2:
            for idx in range(turn_count):
                value_y[idx] = float(win_code == (idx % 2))
        return tuple(value_y)

    board_size = board_size
    win_seq = win_seq

    databook = DataBook()

    for idx in range(play_num):
        board = GameBoard()
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

            #when repeat pass stone
            if now_board[-10:].count((0, board_size)) >= 10:
                loc = list(rule.get_able_loc(now_board))
                loc.remove((None, None))
                loc.remove((0, board_size))

                board.put_stone(*loc[0])
                now_board = board.get_board()

        win_code = rule.game_status(now_board)['win']
        print('winner:', win_code)

        value_y = get_value_y(now_board, win_code)
        databook.add_data({'value_y': value_y})
    return databook
#End=================

board_size = 3
win_seq = 3
play_num = 1

rule = Rule(board_size=board_size, win_seq=win_seq)
agent = model.AlphaO(board_size, rule, round_num=100)


databook = play_game(
    board_size=board_size, win_seq=win_seq, play_num=play_num,
    rule=rule, agent=agent
)

dataset = databook.get_data(shuffle=True)

agent.model.fit(
    dataset['x'],
    [dataset['policy_y'], dataset['value_y']],
    batch_size = 2
)
