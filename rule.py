import random

class Rule:
    def __init__(self, board_size):
        self.board_size = board_size

    def check_able_location(self, list_board, x, y):
        if x >= self.board_size: return False;
        if y >= self.board_size: return False;
        if (x, y) in list_board: return False;
        return True

    def get_able_location(self, list_board):
        #return able location tuple
        able_loc = set(
            (x, y) \
            for x in range(self.board_size) \
            for y in range(self.board_size)
        )
        able_loc -= set(list_board)
        able_loc = list(able_loc)

        random.shuffle(able_loc)

        able_loc = tuple(
            loc for loc in able_loc \
            if self.check_able_location(list_board, *loc)
        )
        return able_loc
