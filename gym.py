import model
from GUI import GUI
from rule import Rule
from util import Util
from dataBook import DataBook
from gameBoard import GameBoard
from playGame import PlayGame

import os
import math
import time
import random
import numpy as np
import pandas as pd


#function============
def get_main_agent_dir():
    main_root = './model/main_model/'
    model_list = os.listdir(main_root)
    if model_list:   #Exist
        return main_root + model_list[0]
    return None   #Empty

def get_now_epoch():
    epoch = 0
    if 'train_history.csv' in os.listdir('./'):
        df = pd.read_csv('./train_history.csv')
        epoch = df['train_epoch'].sum()
    return epoch    

def lr_decay(init_lr, lim_lr, now_epoch, total_epochs):
    zero_x = -(init_lr * total_epochs)  #cosin이 0이 되는 x값
    zero_x /= (lim_lr - init_lr)
    zero_x /= 2.8

    return 0.5 * init_lr * (1. + math.cos(now_epoch/zero_x))
#End=================



board_size = 3
win_seq = 3

round_num = 5

total_epochs = 500
batch_size = 4
buffer_size = 4096
augment_rate = 0.8

play_num = 16
train_turm = 2

COMPETE_NUM = 7


while (now_epoch := get_now_epoch()) < total_epochs:
    learning_rate = lr_decay(init_lr=2e-5, lim_lr=6e-6, now_epoch=now_epoch, total_epochs=total_epochs)

    main_agent_dir = get_main_agent_dir()


    rule = Rule(board_size=board_size, win_seq=win_seq)
    play_game = PlayGame(board_size=board_size, rule=rule)
    main_agent = model.AlphaO(board_size, rule, model_dir=main_agent_dir, lr=learning_rate, round_num=round_num)

    gui = GUI(board_size=board_size, black_info=2, white_info=2)
    
    #load databook===================
    if 'buffer_dataset.pickle' in os.listdir('./dataset/'):
        databook = DataBook(buffer_size=buffer_size, load_dir='./dataset/buffer_dataset.pickle')
    else:
        databook = DataBook(buffer_size=buffer_size)
    #End=============================


    epoch_count = 0
    train_history = None

    for p in range(play_num):
        print(f'\n\n{now_epoch} / {total_epochs}\n\n')

        print(f'\nTRAIN ROUND: {p}\n\n')
        play_game.play(
            black=main_agent, white=main_agent,
            databook=databook, diri_TF=True, gui=gui
        )

        if p % train_turm == 0 or p == (play_num - 1):
            dataset = databook.get_data(shuffle=True, augment_rate=augment_rate)
            
            
            if len(dataset['value_y']) >= (buffer_size * 0.5):
                epoch_count += 1
                train_history = main_agent.train_model(dataset, batch_size=batch_size)

    #save_pickle=====================
    databook.save_databook(save_dir='./dataset/buffer_dataset.pickle')
    #End=============================


    if main_agent_dir is None:    #has no main agent
        #save model
        main_agent.save_model('./model/main_model/', idx=0, start_round=0, end_round=play_num)
        main_agent.save_model('./model/previous_model/', idx=0, start_round=0, end_round=play_num)

        #create pandas
        csv = pd.DataFrame({
            'idx': list(), 'agent_name': list(), 'date': list(),
            'learning_rate': list(), 'batch_size': list(),
            'train_round': list(), 'train_epoch': list(), 'train_buffer_size': list(),
            'PNN_loss': list(), 'VNN_loss': list(), 'train_loss': list(),
            'val_PNN_loss': list(), 'val_VNN_loss': list(), 'val_loss': list(),
            'win_num': list(), 'lose_num': list(), 'draw_num': list(),

        })
        csv.to_csv('./train_history.csv', index=False)

        print('has no main agent')
        

    win_count, lose_count, draw_count = 0, 0, 0

    for e in range(COMPETE_NUM):
        print(f'\nCOMPETE ROUND: {e}\n\n')

        pre_agent_dir = os.listdir('./model/previous_model/')
        pre_agent_dir = random.choice(pre_agent_dir)
        pre_agent_dir = './model/previous_model/' + pre_agent_dir

        pre_agent = model.AlphaO(board_size, rule, model_dir=pre_agent_dir, round_num=round_num)

        if main_agent_color := random.randint(0, 1):
            black, white = pre_agent, main_agent
            print('STONE'.center(50, '='))
            print(f'BLACK(●): PREVIOUS_AGENT')
            print(f'WHITE(○): MAIN_AGENT')
            print('=' * 50)
        else:
            black, white = main_agent, pre_agent
            print('STONE'.center(50, '='))
            print(f'BLACK(●): MAIN_AGENT')
            print(f'WHITE(○): PREVIOUS_AGENT')
            print('=' * 50)
        

        win_code = play_game.play(black=black, white=white, databook=databook, diri_TF=False, gui=gui)

        if win_code == main_agent_color:   #when main agent win
            win_count += 1
        elif win_code == 2:
            draw_count += 1
        else:
            lose_count += 1


    print(f'win rate: {win_count / COMPETE_NUM}')


    main_agent_dir = get_main_agent_dir()
    agent_info = main_agent_dir[len('./model/main_model/'):-3]
    idx, start_round, end_round, month, day, hour, min = agent_info.split('_')

    now = time.localtime()
    now = f'{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}'

    if train_history:
        tr_PNN_loss, tr_VNN_loss = np.mean(train_history.history['PNN_loss']), np.mean(train_history.history['VNN_loss'])
        tr_val_PNN_loss, tr_val_VNN_loss = np.mean(train_history.history['val_PNN_loss']), np.mean(train_history.history['val_VNN_loss'])

        tr_loss, tr_val_loss = np.mean(train_history.history['loss']), np.mean(train_history.history['val_loss'])
    else:
        tr_PNN_loss, tr_VNN_loss, tr_loss = None, None, None
        tr_val_PNN_loss, tr_val_VNN_loss, tr_val_loss = None, None, None

    csv =pd.read_csv('./train_history.csv')
    csv = csv.append({
        'idx': int(idx) + 1,
        'agent_name': f'{idx}_{start_round}_{end_round}_{now}',
        'date': now,
        'learning_rate': learning_rate,
        'batch_size': batch_size,
        'train_round': play_num,
        'train_epoch': epoch_count,
        'train_buffer_size': len(databook.value_y),
        'PNN_loss': tr_PNN_loss,
        'VNN_loss': tr_VNN_loss,
        'train_loss': tr_loss,
        'val_PNN_loss': tr_val_PNN_loss,
        'val_VNN_loss': tr_val_VNN_loss,
        'val_loss': tr_val_loss,
        'win_num': win_count,
        'lose_num': lose_count,
        'draw_num': draw_count
    }, ignore_index=True)
    csv.to_csv('./train_history.csv', index=False)

    if (win_count - lose_count) > 0.:   #win
        main_agent.save_model('./model/main_model/', int(idx)+1, int(end_round), int(end_round)+play_num)

        if not agent_info + '.h5' in os.listdir('./model/previous_model/'):
            os.rename(main_agent_dir, f'./model/previous_model/{agent_info}.h5')
        else:
            os.remove(main_agent_dir)
    else:   #lose
        # main_agent.save_model('./model/previous_model/', int(idx)+1, int(end_round), int(end_round)+play_num)
        main_agent.save_model('./model/main_model/', int(idx)+1, int(end_round), int(end_round)+play_num)
        
        if not agent_info + '.h5' in os.listdir('./model/previous_model/'):
            os.rename(main_agent_dir, f'./model/previous_model/{agent_info}.h5')
        

    #save_pickle=====================
    databook.save_databook(save_dir='./dataset/buffer_dataset.pickle')
    #End=============================
    
    gui.root.destroy()