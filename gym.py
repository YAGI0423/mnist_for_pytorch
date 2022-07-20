import model
from GUI import GUI
from rule import Rule
from dataBook import DataBook
from playGame import PlayGame

import os
import math
import time
import random
import numpy as np
import pandas as pd

from tensorflow.keras import backend


#function============
def get_agent_dir(path):
    model_list = os.listdir(path)
    if model_list:   #Exist
        return path + model_list[-1]
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



#해결 문제===========
#End=================

board_size = 10
win_seq = 5

round_num = 4#16

total_epochs = 20
batch_size = 32#2048

buffer_size = 32768 * (board_size ** 2)#50000 * (board_size ** 2)
window_size = 8192#32768
augment_rate = 1.

play_num = 80#2500

COMPETE_NUM = 16

learning_rate = 0.001

gui = GUI(board_size=board_size, black_info=2, white_info=2)


while (now_epoch := get_now_epoch()) < total_epochs:
    best_agent_dir = get_agent_dir('./model/best_model/')
    # learning_rate = lr_decay(init_lr=2e-5, lim_lr=6e-6, now_epoch=now_epoch, total_epochs=total_epochs)


    rule = Rule(board_size=board_size, win_seq=win_seq)
    play_game = PlayGame(board_size=board_size, rule=rule)
    best_agent = model.AlphaO(board_size, rule, model_dir=best_agent_dir, lr=learning_rate, round_num=round_num)

    if now_epoch % 3 == 0:
        gui.root.destroy()
        gui = GUI(board_size=board_size, black_info=2, white_info=2)
    gui.clear_canvas()
    
    #load databook===================
    if 'buffer_dataset.pickle' in os.listdir('./dataset/'):
        databook = DataBook(buffer_size=buffer_size, window_size=window_size, load_dir='./dataset/buffer_dataset.pickle')
    else:
        databook = DataBook(buffer_size=buffer_size, window_size=window_size)
    #End=============================



    for p in range(play_num):
        print(f'\n\n{now_epoch} / {total_epochs}\n\n')

        print(f'\nTRAIN ROUND: {p}\n\n')
        play_game.play(
            black=best_agent, white=best_agent,
            databook=databook, diri_TF=True, gui=gui
        )


    if best_agent_dir is None:    #has no main agent
        
        #save model
        best_agent.save_model('./model/best_model/', idx=0, start_round=0, end_round=play_num)
        best_agent.save_model('./model/current_model/', idx=0, start_round=0, end_round=play_num)
        
        best_agent_dir = get_agent_dir('./model/best_model/')


        #create pandas
        csv = pd.DataFrame({
            'idx': list(), 'current_agent_name': list(), 'best_agent_name': list(), 'date': list(),
            'learning_rate': list(), 'batch_size': list(), 'round_num': list(),
            'play_num': list(), 'train_epoch': list(), 'train_buffer_size': list(),
            'PNN_loss': list(), 'VNN_loss': list(), 'train_loss': list(),
            'val_PNN_loss': list(), 'val_VNN_loss': list(), 'val_loss': list(),
            'win_num': list(), 'lose_num': list(), 'draw_num': list(),

        })
        csv.to_csv('./train_history.csv', index=False)

        print('has no main agent')
    
    #train===========================
    train_history = None

    dataset = databook.get_data(shuffle=True, augment_rate=augment_rate)

    current_agent_dir = get_agent_dir('./model/current_model/')
    current_agent = model.AlphaO(board_size, rule, model_dir=current_agent_dir, lr=learning_rate, round_num=round_num)
    train_history = current_agent.train_model(dataset, batch_size=batch_size)
    #End=============================
        

    win_count, lose_count, draw_count = 0, 0, 0

    for e in range(COMPETE_NUM):
        print(f'\nCOMPETE ROUND: {e}\n\n')

        compete_databook = DataBook(buffer_size=buffer_size, window_size=window_size)

        if current_agent_color := random.randint(0, 1):
            black, white = current_agent, best_agent
            print('STONE'.center(50, '='))
            print(f'BLACK(●): CURRENT_AGENT')
            print(f'WHITE(○): BEST_AGENT')
            print('=' * 50)
        else:
            black, white = best_agent, current_agent
            print('STONE'.center(50, '='))
            print(f'BLACK(●): BEST_AGENT')
            print(f'WHITE(○): CURRENT_AGENT')
            print('=' * 50)

        win_code = play_game.play(black=black, white=white, databook=compete_databook, diri_TF=False, gui=gui)
        
        
        #RECORAD ONLY MAIN AGENT DATA========
        # comp_data = compete_databook.get_data(shuffle=False)
        # state_x, policy_y, value_y = comp_data['x'], comp_data['policy_y'], comp_data['value_y']

        # comp_data['x'] = comp_data['x'][current_agent_color::2]
        # comp_data['policy_y'] = comp_data['policy_y'][current_agent_color::2]
        # comp_data['value_y'] = comp_data['value_y'][current_agent_color::2]
        #End=================================

        if win_code == current_agent_color:   #when main agent win
            win_count += 1
        elif win_code == 2:
            draw_count += 1
        else:
            lose_count += 1

    print(f'win rate: {win_count / COMPETE_NUM}')


    best_agent_info = best_agent_dir[len('./model/best_model/'):-3]

    current_agent_info = current_agent_dir[len('./model/current_model/'):-3]

    idx, start_round, end_round, month, day, hour, min = current_agent_info.split('_')

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
        'current_agent_name': f'{current_agent_info}',
        'best_agent_name': f'{best_agent_info}',
        'date': now,
        'learning_rate': learning_rate,
        'batch_size': batch_size,
        'round_num': round_num,
        'play_num': play_num,
        'train_epoch': 1,
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

    #save_pickle=====================
    databook.save_databook(save_dir='./dataset/buffer_dataset.pickle')
    databook = None
    #End=============================

    if (win_count / COMPETE_NUM) > 0.55:   #wins

        #pre best agent move to previous
        best_agent.model.save(f'./model/previous_model/{best_agent_info}.h5', include_optimizer=False)
        os.remove(best_agent_dir)

        #new best agent add to best dir
        current_agent.save_model(
            root_dir='./model/best_model/',
            idx=int(idx) + 1,
            start_round=int(end_round),
            end_round=int(end_round) + play_num,
            include_optimizer=False
        )

        #update current_agent
        current_agent.save_model(
            root_dir='./model/current_model/',
            idx=int(idx) + 1,
            start_round=int(end_round),
            end_round=int(end_round) + play_num,
            include_optimizer=True
        )
        os.remove(current_agent_dir)
    else:
        current_agent.save_model(
            root_dir='./model/current_model/',
            idx=int(idx) + 1,
            start_round=start_round,
            end_round=int(end_round) + play_num,
            include_optimizer=True
        )
        os.remove(current_agent_dir)
    
    backend.clear_session()