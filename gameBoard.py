class GameBoard:
    def __init__(self, board_size):
        self.board = []

    def put_stone(self, x, y):
        self.board.append((x, y))
