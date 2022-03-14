import numpy as np

class GameBoard():
    def __init__(self):
        self.__board = []
        # self.__board = [
        #     (0, 0), (0, 1), (0, 2), (0, 3),
        #     (1, 1), (1, 0), (1, 3), (1, 2),
        #     (2, 0), (2, 1), (2, 2), (2, 3),
        #     (3, 0), (3, 1), (None, None),
        # ]
        # self.__board = [(0, 0), (None, None)]

    def get_board(self):
        return tuple(self.__board.copy())

    def put_stone(self, x, y):
        self.__board.append((x, y))
