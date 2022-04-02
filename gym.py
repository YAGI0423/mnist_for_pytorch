import model
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard

import os
import time
import random
import numpy as np

#function============
def get_main_agent_dir():
    main_root = './model/main_model/'
    model_list = os.listdir(main_root)
    if model_list:   #Exist
        return main_root + model_list[0]
    return None   #Empty

def play_game(board_size, win_seq, play_num, rule, black, white):

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

    player_info = {'black': black, 'white': white}
    databook = DataBook()
    win_code_list = []

    for idx in range(play_num):
        board = GameBoard()
        now_board = board.get_board()

        while rule.game_status(now_board)['during']:
            print("=" * 100)
            print(Util.seq_to_square(now_board, board_size))

            now_turn = Util.now_turn(now_board)
            now_player = player_info['black'] if now_turn else player_info['white']

            print('\nnow turn: ', end='')
            print('Black') if now_turn else print('White')

            act = now_player.act(now_board)
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
        win_code_list.append(win_code)

        print('winner:', win_code, end='\n\n')

        value_y = get_value_y(now_board, win_code, discount_factor=1.)
        databook.add_data({'value_y': value_y})
    return win_code_list, databook

def save_agent(agent, root_dir, idx, start_epoch, end_epoch):
    # #file name rule
    # #IDX_START EPOCH_END EPOCH_TIME.h5

    now = time.localtime()
    now = f'{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}'

    info_dir = f'{idx}_{start_epoch}_{end_epoch}_'
    agent.save_model(root_dir + info_dir + now + '.h5')
#End=================


board_size = 3
win_seq = 3
buffer_num = 4

epoch = 2


main_agent_dir = get_main_agent_dir()

rule = Rule(board_size=board_size, win_seq=win_seq)
main_agent = model.AlphaO(board_size, rule, model_dir=main_agent_dir, round_num=500)


if main_agent_dir is None:    #has no main agent
    for e in range(epoch):
        _, databook = play_game(
            board_size=board_size, win_seq=win_seq, play_num=buffer_num,
            rule=rule, black=main_agent, white=main_agent
        )

        dataset = databook.get_data(shuffle=True)
        main_agent.train_model(dataset, batch_size=4)

    #save model
    save_agent(main_agent, './model/main_model/', 0, 0, epoch)
    save_agent(main_agent, './model/previous_model/', 0, 0, epoch)

    print('has no main agent')
else:   #have main agent
    pre_agent_dir = os.listdir('./model/previous_model/')
    pre_agent_dir = random.choice(pre_agent_dir)
    pre_agent_dir = './model/previous_model/' + pre_agent_dir

    pre_agent = model.AlphaO(board_size, rule, model_dir=pre_agent_dir, round_num=500)
    
    args = {
        'board_size': board_size,
        'win_seq': win_seq,
        'play_num': 1,
        'rule': rule
    }

    COMPETE_NUM = 5
    win_num = 0

    for e in range(COMPETE_NUM):
        if main_agent_color := random.randint(0, 1):
            args['black'], args['white'] = pre_agent, main_agent
        else:
            args['black'], args['white'] = main_agent, pre_agent

        win_code_list, _ = play_game(**args)

        if win_code_list[0] == main_agent_color:   #when main agent win
            win_num += 1.
        elif win_code_list[0] == 2:
            win_num += 0.5

print(win_num)
print(win_num / COMPETE_NUM)

#     if (win_num / COMPETE_NUM) > 0.5:
#         pass    #success
#     #새롭게 업데이트된 모델을 main으로 두고
#     #기존 모델은 previous에 넣기
