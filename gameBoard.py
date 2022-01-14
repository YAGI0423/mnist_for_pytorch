import numpy as np

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        self.sequence_num = 5
        self.__board = []
        # self.__board = [(0, 0), (1, 2), (1, 0), (1, 3), (2, 0), (6, 7), (3, 0), (5, 6), (4, 0)]

    def now_turn(self):
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

    def game_status(self):
        #0: during, 1: win, 2: draw

        #함수 선언================================
        def crop_board(board, stone_location, cut_size):
            #board를 stone_locate 기준으로 cut_size만큼 크롭하여 반환

            def get_crop_index(location, cut_size, board_size):
                #크롭을 위한 위치(Index)를 반환
                #board cut idx: cut_min_idx, cut_max_idx
                #board shift idx: shift_min_idx, shift_max_idx
                cut_min_idx = np.clip(location - cut_size, 0, None)
                cut_max_idx = np.clip(location + cut_size, 0, board_size - 1) + 1

                shift_min_idx = cut_size - location + cut_min_idx
                shift_max_idx = shift_min_idx + cut_max_idx - cut_min_idx
                return (cut_min_idx, cut_max_idx), (shift_min_idx, shift_max_idx)

            x, y = stone_location
            tensor_board = np.zeros((cut_size*2+1, cut_size*2+1))

            cut_x, shift_x = get_crop_index(x, cut_size, self.board_size)
            cut_y, shift_y = get_crop_index(y, cut_size, self.board_size)

            cropped_board = board[   #cropping board
                cut_y[0]:cut_y[1],
                cut_x[0]:cut_x[1]
            ]

            tensor_board[   #마지막 착수를 중심으로 정방 행렬 생성
                shift_y[0]:shift_y[1],
                shift_x[0]:shift_x[1]
            ] = cropped_board

            return tensor_board

        def count_seq_stone(seq_list):
            #Count sequence Stone Num
            try: seq_num = seq_list.index(False);
            except: return len(seq_list);
            return seq_num
        #End======================================

        #이전까지는 승패 결정 불가
        if len(self.__board) < self.sequence_num * 2 - 1: return 0;   #during

        #변수 선언================================
        last_x, last_y = self.__board[-1]
        cut_size = self.sequence_num - 1

        last_turn = not self.now_turn()
        stone_color = -1 if last_turn else 1
        #End======================================

        cropped_board = crop_board(self.get_square_board(), (last_x, last_y), cut_size)

        for angle in range(2):   #90도
            row = (cropped_board[cut_size] == stone_color)   #수평축
            for hor in range(2):   #수평, 대각
                row = row.tolist()

                left_side = row[:cut_size][::-1]
                right_side = row[cut_size+1:]

                seq_num = count_seq_stone(left_side)
                seq_num += count_seq_stone(right_side)

                row = np.diag(cropped_board) == stone_color   #대각축

                if seq_num >= cut_size: return 1;   #win

            cropped_board = np.rot90(cropped_board)   #90도 회전

        if len(self.__board) == self.board_size ** 2:
            return 2   #draw
        return 0   #during


if __name__ == "__main__":
    board = GameBoard(3)
    print(board.get_square_board())
    print(board.game_status())
