import model
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard

import os
import time
import random
import pandas as pd


#function============
def get_main_agent_dir():
    main_root = './model/main_model/'
    model_list = os.listdir(main_root)
    if model_list:   #Exist
        return main_root + model_list[0]
    return None   #Empty

def play_game(board_size, rule, databook, black, white, diri_TF=False):

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

        act = now_player.act(now_board, diri_TF)
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
#End=================


#to do list==========
#1. 이동 가능한 함수는 이동 할 것
    #(1) save_agent: model로 이동   #완료
    #(2) data_augment: databook으로 이동   #완료
    #(3) get_main_agent_dir: model로 이동

#2. 중간 save를 수행하도록 변경하기

#3. 함수화 해야할 것
    #(1) 데이터셋 불러오기
    #(2) 데이터셋 저장하기
#End=================


board_size = 10
win_seq = 5

round_num = 800

batch_size = 4
buffer_size = 8192

play_num = 16
train_turm = 2

COMPETE_NUM = 7


main_agent_dir = get_main_agent_dir()


rule = Rule(board_size=board_size, win_seq=win_seq)
main_agent = model.AlphaO(board_size, rule, model_dir=main_agent_dir, round_num=round_num)

#load databook===================
if 'buffer_dataset.pickle' in os.listdir('./dataset/'):
    databook = DataBook(buffer_size=buffer_size, load_dir='./dataset/buffer_dataset.pickle')
else:
    databook = DataBook(buffer_size=buffer_size)
#End=============================

epoch_count = 0

for p in range(play_num):
    print(f'\nTRAIN ROUND: {p}\n\n')
    _ = play_game(
        board_size=board_size, rule=rule,databook=databook,
        black=main_agent, white=main_agent,
        diri_TF=True
    )

    if p % train_turm == 0 or p == (play_num - 1):
        dataset = databook.get_data(shuffle=True, augment_rate=0.8)
        
        if len(dataset['value_y']) >= (buffer_size * 0.5):
            epoch_count += 1
            train_histroy = main_agent.train_model(dataset, batch_size=batch_size)


#save_pickle=====================
databook.save_databook(save_dir='./dataset/buffer_dataset.pickle')
#End=============================


if main_agent_dir is None:    #has no main agent
    #save model
    main_agent.save_model('./model/main_model/', idx=0, start_round=0, end_round=play_num)
    main_agent.save_model('./model/previous_model/', idx=0, start_round=0, end_round=play_num)

    #create pandas
    csv = pd.DataFrame({
        'idx': list(), 'date': list(),
        'train_round': list(), 'train_epoch': list(), 'train_buffer_size': list(),
        'train_loss': list(), 'train_val_loss': list(),
        'win_num': list(), 'lose_num': list(), 'draw_num': list(),

    })
    csv.to_csv('./train_history.csv', index=False)

    print('has no main agent')
else:   #have main agent
    args = {
        'board_size': board_size,
        'databook': databook,
        'rule': rule
    }

    
    win_count, lose_count, draw_count = 0, 0, 0

    for e in range(COMPETE_NUM):
        print(f'\nCOMPETE ROUND: {e}\n\n')

        pre_agent_dir = os.listdir('./model/previous_model/')
        pre_agent_dir = random.choice(pre_agent_dir)
        pre_agent_dir = './model/previous_model/' + pre_agent_dir

        pre_agent = model.AlphaO(board_size, rule, model_dir=pre_agent_dir, round_num=round_num)

        if main_agent_color := random.randint(0, 1):
            args['black'], args['white'] = pre_agent, main_agent
        else:
            args['black'], args['white'] = main_agent, pre_agent

        win_code = play_game(**args)

        if win_code == main_agent_color:   #when main agent win
            win_count += 1
        elif win_code == 2:
            draw_count += 1
        else:
            lose_count += 1


    print(f'win rate: {(win_count - lose_count+draw_count) / COMPETE_NUM}')

    agent_info = main_agent_dir[len('./model/main_model/'):-3]
    idx, start_round, end_round, month, day, hour, min = agent_info.split('_')

    now = time.localtime()
    now = f'{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}'

    csv =pd.read_csv('./train_history.csv')
    csv = csv.append({
        'idx': int(idx) + 1,
        'date': now,
        'train_round': play_num,
        'train_epoch': epoch_count,
        'train_buffer_size': len(databook.value_y),
        'train_loss': train_histroy.history['loss'][-1],
        'train_val_loss': train_histroy.history['val_loss'][-1],
        'win_num': win_count,
        'lose_num': lose_count,
        'draw_num': draw_count
    }, ignore_index=True)
    csv.to_csv('./train_history.csv', index=False)

    if (win_count - lose_count) > 0.:
        main_agent.save_model('./model/main_model/', int(idx)+1, int(end_round), int(end_round)+play_num)

        if not agent_info + '.h5' in os.listdir('./model/previous_model/'):
            os.rename(main_agent_dir, f'./model/previous_model/{agent_info}.h5')
        else:
            os.remove(main_agent_dir)
    else:
        main_agent.save_model('./model/previous_model/', int(idx)+1, int(end_round), int(end_round)+play_num)


#save_pickle=====================
databook.save_databook(save_dir='./dataset/buffer_dataset.pickle')
#End=============================