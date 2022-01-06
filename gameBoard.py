class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = []

    def check_location(self, x, y):
        if x >= self.board_size: return False;
        if y >= self.board_size: return False;
        if (x, y) in self.board: return False;
        return True

    def put_stone(self, x, y):
        if self.check_location(x, y):
            self.board.append((x, y))
            return True
        return False



board = GameBoard(19)
print(board.board)

board.put_stone(2, 5)
print(board.board)

board.put_stone(2, 20)
print(board.board)

board.put_stone(2, 10)
print(board.board)
