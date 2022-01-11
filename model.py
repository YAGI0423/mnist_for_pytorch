import numpy as np

class AlphaO:
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

        able_loc = get_able_location(board)
        rand_idx = np.random.choice(len(able_loc))
        return able_loc[rand_idx]


board = [(0, 0), (1, 2), (1, 0), (1, 3), (2, 0), (6, 7), (3, 0), (5, 6), (4, 0)]

model = AlphaO(9)
print(model.act(board))
