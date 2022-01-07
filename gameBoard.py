import numpy as np

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        self.__board = [(0, 0), (5, 5), (0, 1), (2, 0), (0, 2), (7, 4), (0, 3), (8, 3)]

    def next_turn(self):
        return self.__board % 2 == 0   #True: 흑, False: 백

    def get_list_board(self):
        return tuple(self.__board)

    def get_square_board(self):
        board = np.zeros((self.board_size, self.board_size))
        for turn, (x, y) in enumerate(self.__board):
            stone_color = -1 if turn % 2 == 0 else 1
            board[y][x] = stone_color
        return board

    def check_location(self, x, y):
        if x >= self.board_size: return False;
        if y >= self.board_size: return False;
        if (x, y) in self.__board: return False;
        return True

    def put_stone(self, x, y):
        if self.check_location(x, y):
            self.__board.append((x, y))
            return True
        return False

    def check_game_over(self):
        last_location = self.__board[-1]





board = GameBoard(9)
print(board.get_square_board(), end="\n\n")

board.put_stone(0, 4)
print(board.get_square_board(), end="\n\n")

board.check_game_over()
