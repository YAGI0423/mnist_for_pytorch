class User:
    def __init__(self, board_size):
        self.board_size = board_size

    def act(self, board):
        def get_able_location(board):
            #return able location
            able_loc = set(
                (x, y) \
                for x in range(self.board_size) \
                for y in range(self.board_size)
            )
            able_loc -= set(board)
            return tuple(able_loc)

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

        able_loc = get_able_location(board)
        while True:
            input_x, input_y = check_input("x"), check_input("y")
            if (input_x, input_y) in able_loc: break;
        return (input_x, input_y)
