import gameBoard

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


board = gameBoard.GameBoard(9)

while game_done := not board.check_game_over():
    print("=" * 100)
    print(board.get_square_board())
    print("Black" if board.now_turn() else "White")

    while True:
        input_x, input_y = check_input("x"), check_input("y")
        success = board.put_stone(input_x, input_y)
        if success: break;

    print("=" * 100, end="\n\n")
    
print(board.check_game_over())
