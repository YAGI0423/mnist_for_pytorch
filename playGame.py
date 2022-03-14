import model
from user import User
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np

#해결 필요 문제======

#End=================

board_size = 4
win_seq = 3
player_info = {
    'black': User(board_size),
    'white': User(board_size)
}

board = GameBoard()
rule = Rule(board_size=board_size, win_seq=win_seq)


now_board = board.get_board()

print(rule.game_status(now_board)['during'])

while rule.game_status(now_board)['during']:
    now_turn = Util.now_turn(now_board)
    now_player = player_info['black'] if now_turn else player_info['white']

    status = {
        'seq_xy_board': now_board,
        'able_loc': rule.get_able_loc(now_board)
    }

    act_loc = now_player.act(status)
    board.put_stone(*act_loc)


    #print================
    print("=" * 100)
    print('square board', '-' * 30)
    print(Util.seq_to_square(now_board, board_size))
    print('-' * 43)

    print('\nnow turn: ', end='')
    print('Black') if now_turn else print('White')

    print(f'\nact loc: {act_loc}')
    #End==================


    now_board = board.get_board()

    print(now_board)
    print(Util.seq_to_square(now_board, board_size))
    print(rule.game_status(now_board))
    exit()
exit()


while (game_done := _rule.game_status(board.get_list_board())) == 0:
    print("=" * 100)
    print(Util.get_square_board(board.get_list_board(), board_size))
    exit()

    #Put Stone=======================
    now_turn = board.now_turn()
    print("Black" if now_turn else "White")

    now_player_key = "playerA" if playerA_color == now_turn else "playerB"

    stone_location = player_info[now_player_key].act(board.get_list_board())
    if stone_location == (None, None):
        print("surrender!")
        break;   #기권

    board.put_stone(*stone_location)
    #End=============================

    print("=" * 100, end="\n\n")

if game_done == 2:
    print("Draw")
else:
    if board.now_turn():   #True: 흑 승, False: 백 승
        print("White Win")
    else:
        print("Black Win")

print(util.get_square_board(board.get_list_board()))
print(stone_location)
