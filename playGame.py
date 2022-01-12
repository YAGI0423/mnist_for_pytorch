import gameBoard
import model

import numpy as np


def check_input(message):
    #check user input value
    while True:
        input_data = input(f"{message}: ")
        if (input_data) == "": continue  #빈 값
        try:
            input_data = int(input_data)
            return input_data
        except:
            continue



player1, player2 = True, False   #True: User, False: Model
model = model.AlphaO(9)

player1_stone = bool(np.random.randint(2))   #True: Black, Flase: White


board = gameBoard.GameBoard(9)

while game_done := not board.check_game_over():
    print("=" * 100)
    print(board.get_square_board())

    now_turn = board.now_turn()
    print("Black" if now_turn else "White")

    if player1_stone == now_turn:
        if player1:
            while True:
                input_x, input_y = check_input("x"), check_input("y")
                success = board.put_stone(input_x, input_y)
                if success: break;
        else:
            loc = model.act(board.get_list_board)
            success = board.put_stone(loc)
    else:
        if player2:
            while True:
                input_x, input_y = check_input("x"), check_input("y")
                success = board.put_stone(input_x, input_y)
                if success: break;
        else:
            loc = model.act(board.get_list_board())
            success = board.put_stone(*loc)



    print("=" * 100, end="\n\n")

if win_stone := board.now_turn():   #True: 백 승, False: 흑 승
    print("White Win")
else:
    print("Black Win")
