import numpy as np
import rule

class GameBoard():
    def __init__(self, board_size):
        self.rule = rule.Rule(board_size=board_size)
        self.board_size = board_size
        self.__board = []
        # self.__board = [(0, 0), (1, 2), (1, 0), (1, 3), (2, 0), (6, 7), (3, 0), (5, 6), (4, 0)]

    def get_list_board(self):
        return tuple(self.__board.copy())

    def put_stone(self, x, y):
        self.__board.append((x, y))
