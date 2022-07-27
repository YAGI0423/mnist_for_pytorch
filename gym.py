import model
from GUI import GUI
from rule import Rule
from dataBook import DataBook
from playGame import PlayGame

import os
import shutil
import pickle
import json
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

def initial_setting(best_agent):
    #save model
    best_agent.save_model('./model/best_model/', idx=0, start_round=0, end_round=0)
    best_agent.save_model('./model/current_model/', idx=0, start_round=0, end_round=0)

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
#End=================



#해결 문제===========
#End=================

board_size = 10
win_seq = 5

round_num = 64#16

total_epochs = 200
batch_size = 32#2048

buffer_size = 32768 * (board_size ** 2)#50000 * (board_size ** 2)
window_size = 8192#32768
augment_rate = 1.

play_num = 7#2500

COMPETE_NUM = 16

learning_rate = 0.001


use_colab_collector = True
colab_main_dir = 'G:/내 드라이브/alphaO/colab_collector/'


best_agent_dir = get_agent_dir('./model/best_model/')
gui = GUI(board_size=board_size, black_info=2, white_info=2)
rule = Rule(board_size=board_size, win_seq=win_seq)
play_game = PlayGame(board_size=board_size, rule=rule)
best_agent = model.AlphaO(board_size, rule, model_dir=best_agent_dir, lr=learning_rate, round_num=round_num)

if best_agent_dir is None:
    initial_setting(best_agent)
    best_agent_dir = get_agent_dir('./model/best_model/')




def cleaning_folder(dir):
     for file_name in os.listdir(dir):
        file_dir = dir + file_name
        os.remove(file_dir)

def create_init_communication(board_size, win_seq, round_num, best_agent_name):
    communication_data = {
        'common_info': {
            'board_size': board_size,
        'win_seq': win_seq,
        'round_num': round_num,
        'best_agent_name': best_agent_name
        },

        'local_info': {
        'status': 0
        },

        'colab_info': {
            'status': False,
            'play_num': 0
        }
    }
    return communication_data

def load_communication_window(main_dir):
    with open(main_dir + 'communication_window.json', 'r') as st_json:
        js_data = json.load(st_json)
    return js_data

def write_communication_window(main_dir, board_size, win_seq, round_num, best_agent_name, status):
  commu_data = load_communication_window(main_dir)
  commu_data['common_info']['board_size'] = board_size
  commu_data['common_info']['win_seq'] = win_seq
  commu_data['common_info']['round_num'] = round_num
  commu_data['common_info']['best_agent_name'] = best_agent_name
  commu_data['local_info']['status'] = status

  with open(main_dir + 'communication_window.json', 'w') as json_file:
    json.dump(commu_data, json_file)

def get_colab_data(communication_window):
  status = communication_window['colab_info']['status']
  play_num = communication_window['colab_info']['play_num']
  return status, play_num


if use_colab_collector:
    local_agent_name = best_agent_dir.split('/')[-1]
    colab_agent_name = os.listdir(colab_main_dir + 'agent/')[-1]

    print(f'Synchronizing the model...', end='')
    if local_agent_name != colab_agent_name:
        cleaning_folder(colab_main_dir + 'agent/')
        shutil.copy(best_agent_dir, colab_main_dir + 'agent/')
    print('(OK)')

    print(f'Clearning the databook...', end='')
    cleaning_folder(colab_main_dir + 'databook/')
    print('(OK)')

    print(f'Send the communication context...', end='')
    cleaning_folder(colab_main_dir + 'communication_window/')
    commu_context = create_init_communication(
        board_size=board_size, win_seq=win_seq, round_num=round_num, best_agent_name=local_agent_name
    )
    with open(colab_main_dir + 'communication_window/communication_window.json', 'w') as json_file:
        json.dump(commu_context, json_file)
    print('(OK)')

    print(f'Wait for connecting...')
    while True:
        loaded_commu = load_communication_window(colab_main_dir + 'communication_window/')
        if loaded_commu['colab_info']['status']:
            print('(connecting is successful)')
            break
        time.sleep(3)
    write_communication_window(
        colab_main_dir + 'communication_window/',
        board_size = board_size,
        win_seq=win_seq,
        round_num=round_num,
        best_agent_name=local_agent_name,
        status=1
    )




while (now_epoch := get_now_epoch()) < total_epochs:
    if best_agent_dir != get_agent_dir('./model/best_model/'):
        # learning_rate = lr_decay(init_lr=2e-5, lim_lr=6e-6, now_epoch=now_epoch, total_epochs=total_epochs)
        best_agent_dir = get_agent_dir('./model/best_model/')
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


    local_play_num, colab_play_num = 0, 0
    while (local_play_num + colab_play_num) < play_num:
        print(f'\n\n{now_epoch} / {total_epochs}\n\n')
        print(f'TOTAL PLAY: {local_play_num + colab_play_num}', end='\t')
        print(f'(LOCAL PLAY: {local_play_num}, COLAB PLAY: {colab_play_num})')

        play_game.play(
            black=best_agent, white=best_agent,
            databook=databook, diri_TF=True, gui=gui
        )

        local_play_num += 1

        if use_colab_collector:
            commu_data = load_communication_window(colab_main_dir + 'communication_window/')
            colab_status, colab_play_num = get_colab_data(commu_data)

            #3 play_num 남았을 경우, colab collector에 데이터셋 적재 요구하기
            play_num_callsign_limit_TF = ((local_play_num + colab_play_num + 3) >= play_num)   #play_num 3남았을 경우
            now_local_status_TF = (commu_data['local_info']['status'] != 2)   #이전에 callsign 2를 보내지 않았을 경우
            if play_num_callsign_limit_TF and now_local_status_TF:
                write_communication_window(
                    colab_main_dir + 'communication_window/',
                    board_size = board_size,
                    win_seq=win_seq,
                    round_num=round_num,
                    best_agent_name=local_agent_name,
                    status=2
                )

    if use_colab_collector:
        local_agent_name = best_agent_dir.split('/')[-1]

        #communication_window의 colab_info status == False일 경우 업로드 상태
        print(f'Check databook upload status...', end='')
        while True:
            commu_data = load_communication_window(colab_main_dir + 'communication_window/')
            if not commu_data['colab_info']['status']:
                print('(OK)')
                break

        #실제 파일 업로드 확인하기
        print(f'Check for file existence...', end='')
        while True:
            if os.listdir(colab_main_dir + 'databook/'):   #파일 존재 확인
                uploaded_file_name = os.listdir(colab_main_dir + 'databook/')[-1].split('.')[0]

                commu_data = load_communication_window(colab_main_dir + 'communication_window/')
                colab_play_num = str(commu_data['colab_info']['play_num'])
                
                if uploaded_file_name == colab_play_num:
                    print('(OK)')
                    break
        
        #colab databook 불러와 통합하기
        print(f'Combine with colab buffer...', end='')
        colab_databook_dir = f'{colab_main_dir}/databook/{colab_play_num}.pickle'
        with open(colab_databook_dir, 'rb') as pick:
            colab_databook = pickle.load(pick)
        databook.add_data(colab_databook)

        #colab databook 지우기
        os.remove(colab_databook_dir)
        print('(OK)')

        #best agent가 변경되지 않을 경우를 대비하여 학습 및 평가 동안 self-play 요청
        write_communication_window(
            colab_main_dir + 'communication_window/',
            board_size = board_size,
            win_seq=win_seq,
            round_num=round_num,
            best_agent_name=local_agent_name,
            status=3
        )

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