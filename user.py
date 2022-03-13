class User():
    def __init__(self, board_size):
        self.board_size = board_size

    def act(self, status):
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

        able_loc = status['able_loc']
        while True:
            input_x, input_y = check_input("x"), check_input("y")
            if (input_x, input_y) in able_loc: break;
            if (input_x, input_y) == (None, None): break;   #기권
        return (input_x, input_y)
