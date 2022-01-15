import user
import model
import gameBoard

import numpy as np

#해결 필요 문제======

#End=================

board_size = 9
player_info = {
    'playerA': user.User(board_size),
    'playerB': model.AlphaO(board_size)
}
playerA_color = bool(np.random.randint(2))   #True: Black, Flase: White
board = gameBoard.GameBoard(board_size)


while (game_done := board.game_status()) == 0:
    print("=" * 100)
    print(board.get_square_board())

    #Put Stone=======================
    now_turn = board.now_turn()
    print("Black" if now_turn else "White")

    now_player_key = "playerA" if playerA_color == now_turn else "playerB"

    stone_location = player_info[now_player_key].act(board.get_list_board())
    if stone_location == (None, None): break;   #기권

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

print(board.get_square_board())
print(stone_location)
