import user
import model
import gameBoard

import numpy as np


board_size = 9
player_info = {
    'playerA': model.RandomChoice(board_size),
    'playerB': model.RandomChoice(board_size)
}
playerA_color = bool(np.random.randint(2))   #True: Black, Flase: White
board = gameBoard.GameBoard(board_size)


while game_done := not board.check_game_over():
    print("=" * 100)
    print(board.get_square_board())

    #Put Stone=======================
    now_turn = board.now_turn()
    print("Black" if now_turn else "White")

    now_player_key = "playerA" if playerA_color == now_turn else "playerB"
    stone_location = player_info[now_player_key].act(board.get_list_board())
    success = board.put_stone(*stone_location)
    #End=============================

    print("=" * 100, end="\n\n")

if not now_turn:   #True: 백 승, False: 흑 승
    print("White Win")
else:
    print("Black Win")
print(board.get_square_board())
print(stone_location)
#오목이 완성 되지 않아도 게임이 종료되는 이슈
