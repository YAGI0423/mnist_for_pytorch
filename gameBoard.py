import numpy as np

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size

        # self.__board = [(5, 2), (7, 5), (5, 3), (2, 0), (5, 5), (7, 4), (5, 6), (8, 3)]   #세로
        self.__board = [(2, 5), (7, 5), (3, 5), (2, 0), (5, 5), (7, 4), (6, 5), (8, 3)]   #가로

    def next_turn(self):
        return len(self.__board) % 2 == 0   #True: 흑, False: 백

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
        last_x, last_y = self.__board[-1]
        last_turn = not self.next_turn()
        stone_color = -1 if last_turn else 1

        row = self.get_square_board()[last_y] == stone_color

        left_side = row[:last_x][::-1]
        right_side = row[last_x+1:]

        def count_squential_stone(list):
            #연결된 돌의 개수를 반환
            for num, stone in enumerate(list):
                if not stone: break;
            return num

        print(count_squential_stone(left_side))
        print(count_squential_stone(right_side))



board = GameBoard(9)
print(board.get_square_board(), end="\n\n")

board.put_stone(4, 5)
print(board.get_square_board(), end="\n\n")

board.check_game_over()
