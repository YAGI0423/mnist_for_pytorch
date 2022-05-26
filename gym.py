import model
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard

import os
import time
import random
import pickle
import numpy as np
import pandas as pd


#function============
def get_main_agent_dir():
    main_root = './model/main_model/'
    model_list = os.listdir(main_root)
    if model_list:   #Exist
        return main_root + model_list[0]
    return None   #Empty

def play_game(board_size, rule, databook, black, white):

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
    player_info = {'black': black, 'white': white}
 
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
        if now_board[-4:].count((0, board_size)) >= 4:
            loc = list(rule.get_able_loc(now_board))
            loc.remove((None, None))
            loc.remove((0, board_size))

            board.put_stone(*loc[0])
            now_board = board.get_board()

    win_code = rule.game_status(now_board)['win']

    print('winner:', win_code, end='\n\n')

    value_y = get_value_y(now_board, win_code, discount_factor=1.)
    databook.add_data({'value_y': value_y})

    return win_code

def save_agent(agent, root_dir, idx, start_epoch, end_epoch):
    # #file name rule
    # #IDX_START EPOCH_END EPOCH_TIME.h5

    now = time.localtime()
    now = f'{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}'

    info_dir = f'{idx}_{start_epoch}_{end_epoch}_'
    agent.save_model(root_dir + info_dir + now + '.h5')
#End=================



board_size = 10
win_seq = 5
buffer_size = 4096

play_num = 16
train_turm = 2

COMPETE_NUM = 3


main_agent_dir = get_main_agent_dir()


rule = Rule(board_size=board_size, win_seq=win_seq)
main_agent = model.AlphaO(board_size, rule, model_dir=main_agent_dir, round_num=1600)
databook = DataBook()


#load pickle=====================
if 'buffer_dataset.pickle' in os.listdir('./model/'):
    with open('./model/buffer_dataset.pickle', 'rb') as pick:
        data = pickle.load(pick)
    
    databook.state = data['state']
    databook.policy_y = data['policy_y']
    databook.value_y = data['value_y']
#End=============================


def data_augment(dict_dataset, rate=0.3):
    return_dataset = dict()

    data_len = len(dict_dataset['value_y'])
    augment_num = int(data_len * rate)

    aug_idx_list = random.choices(range(data_len), k=augment_num)

    data_x = dict_dataset['x'][aug_idx_list].copy()
    policy_y = dict_dataset['policy_y'][aug_idx_list].copy()
    value_y = dict_dataset['value_y'][aug_idx_list].copy()

    aug_data_x = np.rot90(data_x, k=random.randint(1, 4), axes=(1, 2))
    if random.randint(0, 2):
        aug_data_x = np.flip(aug_data_x, axis=2)
    
    return_dataset['x'] = np.concatenate(dict_dataset['x'], aug_data_x)
    return_dataset['policy_y'] = np.concatenate(dict_dataset['policy_y'], policy_y)
    return_dataset['value_y'] = np.concatenate(dict_dataset['value_y'], value_y)

    return return_dataset



for p in range(play_num):
    print(f'\nTRAIN ROUND: {p}\n\n')
    _ = play_game(
        board_size=board_size, rule=rule, databook=databook, black=main_agent, white=main_agent
    )

    if p % train_turm == 0 or p == (play_num - 1):
        databook.update_databook(buffer_size=buffer_size)
 
        dataset = databook.get_data(shuffle=True)
        dataset = data_augment(dataset)

        main_agent.train_model(dataset, batch_size=4)


#save_pickle=====================
with open('./model/buffer_dataset.pickle', 'wb') as pick:
    save_databook = {
        'state': databook.state,
        'policy_y': databook.policy_y,
        'value_y': databook.value_y
    }
    pickle.dump(save_databook, pick)
#End=============================


if main_agent_dir is None:    #has no main agent
    #save model
    save_agent(main_agent, './model/main_model/', 0, 0, play_num)
    save_agent(main_agent, './model/previous_model/', 0, 0, play_num)

    #create pandas
    csv = pd.DataFrame({
        'idx': list(),
        'date': list(),
        'start_epoch': list(),
        'end_epoch': list(),
        'win_num': list()
        })
    csv.to_csv('./train_history.csv', index=False)

    print('has no main agent')
else:   #have main agent
    args = {
        'board_size': board_size,
        'databook': databook,
        'rule': rule
    }

    
    win_num = 0

    for e in range(COMPETE_NUM):
        print(f'\nCOMPETE ROUND: {e}\n\n')

        pre_agent_dir = os.listdir('./model/previous_model/')
        pre_agent_dir = random.choice(pre_agent_dir)
        pre_agent_dir = './model/previous_model/' + pre_agent_dir

        pre_agent = model.AlphaO(board_size, rule, model_dir=pre_agent_dir, round_num=500)

        if main_agent_color := random.randint(0, 1):
            args['black'], args['white'] = pre_agent, main_agent
        else:
            args['black'], args['white'] = main_agent, pre_agent

        win_code = play_game(**args)

        if win_code == main_agent_color:   #when main agent win
            win_num += 1.
        elif win_code != 2:
            win_num -= 1.


    print(f'win rate: {win_num / COMPETE_NUM}')

    agent_info = main_agent_dir[len('./model/main_model/'):-3]
    idx, start_epoch, end_epoch, month, day, hour, min = agent_info.split('_')

    now = time.localtime()
    now = f'{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}'

    csv =pd.read_csv('./train_history.csv')
    csv = csv.append({
        'idx': int(idx) + 1,
        'date': now,
        'start_epoch': int(end_epoch),
        'end_epoch': int(end_epoch) + play_num,
        'win_num': win_num
    }, ignore_index=True)
    csv.to_csv('./train_history.csv', index=False)

    if (win_num / COMPETE_NUM) > 0.:
        save_agent(main_agent, './model/main_model/', int(idx)+1, int(end_epoch), int(end_epoch)+play_num)

        if not agent_info + '.h5' in os.listdir('./model/previous_model/'):
            os.rename(main_agent_dir, f'./model/previous_model/{agent_info}.h5')
        else:
            os.remove(main_agent_dir)
    else:
        save_agent(main_agent, './model/previous_model/', int(idx)+1, int(end_epoch), int(end_epoch)+play_num)


#save_pickle=====================
with open('./model/buffer_dataset.pickle', 'wb') as pick:
    save_databook = {
        'state': databook.state,
        'policy_y': databook.policy_y,
        'value_y': databook.value_y
    }
    pickle.dump(save_databook, pick)
#End=============================