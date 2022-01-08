import numpy as np

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size

        # self.__board = [(5, 2), (7, 5), (5, 3), (2, 0), (5, 5), (7, 4), (5, 6), (8, 3)]   #세로
        # self.__board = [(2, 5), (7, 5), (3, 5), (2, 0), (5, 5), (7, 4), (6, 5), (8, 3)]   #가로
        self.__board = [(1, 7), (7, 2), (2, 6), (2, 0), (4, 4), (7, 3), (5, 3), (8, 3)]   #좌측 대각

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
        #1. 보드를 정방행렬로 자르기
        #2. 대각성분 추출하기
        #3. 보드를 대칭변환 flip 하기

        last_x, last_y = self.__board[-1]
        last_turn = not self.next_turn()
        stone_color = -1 if last_turn else 1

        def cut_board(board, stone_location, cut_size):
            #board를 stone_locate 기준으로 cut_size만큼 크롭하여 반환
            x, y = stone_location

            a = np.zeros((cut_size*2+1, cut_size*2+1))

            print(x, y)
            print(a)


        cut_board(self.get_square_board(), (last_x, last_y), 4)




        # row = self.get_square_board()[last_y] == stone_color
        #
        # left_side = row[:last_x][::-1]   #마지막 돌 기준 좌측
        # right_side = row[last_x+1:]   #마지막 돌 기준 우측
        #
        # def count_squential_stone(list):
        #     #연결된 돌의 개수를 반환
        #     for num, stone in enumerate(list):
        #         if not stone: break;
        #     return num
        #
        # seq_num = count_squential_stone(left_side)
        # seq_num += count_squential_stone(right_side)
        # print(seq_num)



board = GameBoard(9)
print(board.get_square_board(), end="\n\n")

board.put_stone(3, 5)
print(board.get_square_board(), end="\n\n")

board.check_game_over()
