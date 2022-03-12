import user
import model
from rule import Rule
from util import Util
from gameBoard import GameBoard

import numpy as np

#해결 필요 문제======

#End=================

board_size = 4
win_seq = 3
player_info = {
    'playerA': model.RandomChoice(board_size),
    'playerB': model.RandomChoice(board_size)
}
playerA_color = bool(np.random.randint(2))   #True: Black, Flase: White

board = GameBoard()
rule = Rule(board_size=board_size, win_seq=5)


now_board = board.get_board()

while rule.game_status(now_board) == 0:
    print("=" * 100)
    print(Util.seq_to_square(now_board, board_size))

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
