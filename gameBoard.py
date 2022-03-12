import numpy as np

class GameBoard():
    def __init__(self):
        # self.__board = []
        self.__board = [(0, 0), (0, 2), (1, 2), (2, 3), (2, 1)]

    def get_board(self):
        return tuple(self.__board.copy())

    def put_stone(self, x, y):
        self.__board.append((x, y))
