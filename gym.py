import model
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard

import numpy as np

#function============
def play_game(board_size, win_seq, play_num, rule, agent):

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
        print('winner:', win_code, end='\n\n')

        value_y = get_value_y(now_board, win_code, discount_factor=1.)
        databook.add_data({'value_y': value_y})
    return databook
#End=================

board_size = 3
win_seq = 3
buffer_num = 4
epoch = 10

rule = Rule(board_size=board_size, win_seq=win_seq)
agent = model.AlphaO(board_size, rule, model_dir=None, round_num=500)

for e in range(epoch):
    databook = play_game(
        board_size=board_size, win_seq=win_seq, play_num=buffer_num,
        rule=rule, agent=agent
    )

    dataset = databook.get_data(shuffle=True)

    agent.train_model(dataset, batch_size=8)

agent.save_model(epoch)
