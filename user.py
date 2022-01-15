import rule

class User(rule.Rule):
    def __init__(self, board_size):
        super().__init__(board_size)
        self.board_size = board_size

    def act(self, board):
        def check_input(message):
            #check user input value
            while True:
                input_data = input(f"{message}: ")
                if (input_data) == "": continue  #빈 값
                if input_data == "None": return None;   #None값
                try:
                    input_data = int(input_data)   #정수값
                    return input_data
                except:
                    continue

        able_loc_tup = super().get_able_location(board)
        while True:
            input_x, input_y = check_input("x"), check_input("y")
            if (input_x, input_y) in able_loc_tup: break;
            if (input_x, input_y) == (None, None): break;   #기권
        return (input_x, input_y)
