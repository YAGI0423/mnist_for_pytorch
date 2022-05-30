from tkinter import *
import tkinter.font

class GUI:
    def __init__(self, board_size, black_info, white_info):
        def init_window(root):
            root.title('board window')
            root.geometry(f"{self.wd['width']}x{self.wd['height']}+100+100")
            root.resizable(False, False)

        def init_board(root):
            board = Canvas(root, width=self.wd['width'], height=self.wd['height'])
            board.create_rectangle(
                self.bd['x'], self.bd['y'],
                self.bd['x']+self.board_wh, self.bd['y']+self.board_wh
            )

            step_size = self.board_wh // (self.board_size - 1)

            #draw row, col=============
            for idx in range(step_size, self.board_wh-1, step_size):
                board.create_line(    #row
                    self.bd['x'], self.bd['y']+idx,
                    self.bd['x']+self.board_wh, self.bd['y']+idx
                )
                board.create_line(    #col
                    self.bd['x']+idx, self.bd['y'],
                    self.bd['x']+idx, self.bd['y']+self.board_wh
                )
            #End=======================

            #draw cross dot============
            for idx in range((self.board_size - 2) ** 2):   #board inner range
                x = idx % (self.board_size - 2) + 1
                y = idx // (self.board_size - 2) + 1
                
                board.create_oval(
                    self.bd['x'] - 3 + (x * step_size), self.bd['y'] - 3 + (y * step_size),
                    self.bd['x'] + 3 + (x * step_size), self.bd['y'] + 3 + (y * step_size),
                    fill='gray'
                )
            #End=======================

            board.pack()

        def init_state(root):
            stone_ft = tkinter.font.Font(size=30)

            black_stone_txt = Label(root, text='●', font=stone_ft, relief='solid')
            white_stone_txt = Label(root, text='○', font=stone_ft, relief='solid')
    

            black_stone_txt.place(x=self.bd['x'], y=30)
            white_stone_txt.place(
                x=self.wd['width']-30-30,
                y=30
            )
           

        self.board_size = board_size
        self.black_info, self.white_info = black_info, white_info

        self.wd = {'width': 700, 'height': 800} #wd: `window`의 줌말

        self.bd = {'x': 30}   #bd: `board`의 줌말, 시작 x, y 좌표
        self.board_wh = self.wd['width'] - self.bd['x'] * 2 #board size
        self.bd['y'] = self.wd['height'] - self.board_wh - self.bd['x'] #get bd_y


        self.root = Tk()
        init_window(self.root)
        init_board(self.root)

        init_state(self.root)
        

        # font = tkinter.font.Font(family='Consolas', size=50)
        
        # label = Label(self.root, text="●", font=font)
        # label.place(x=30, y=10)

        # label = Label(self.root, text="○", font=font)
        # label.place(x=700-30-50, y=10)
        
        
        

    def print(self):
        self.root.mainloop()


if __name__ == '__main__':
    now_board = ((5, 5), (2, 2), (3, 3))

    
    gui = GUI(board_size=5, black_info=2, white_info=0)

    # gui.located()
    gui.print()