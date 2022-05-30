from tkinter import *

class GUI:
    def __init__(self, board_size, black_info, white_info):
        self.board_size = board_size
        self.black_info, self.white_info = black_info, white_info

        self.wd = {'width': 700, 'height': 800} #wd: `window`의 줌말

        self.bd = {'x': 30}   #bd: `board`의 줌말, 시작 x, y 좌표
        self.board_wh = self.wd['width'] - self.bd['x'] * 2 #board size
        self.bd['y'] = self.wd['height'] - self.board_wh - self.bd['x'] #get bd_y


        self.root = Tk()
        self.window = Canvas(self.root, width=self.wd['width'], height=self.wd['height'])
        
        self.init_window()



    def init_window(self):
        self.root.title('board window')
        self.root.geometry(f"{self.wd['width']}x{self.wd['height']}+100+100")
        self.root.resizable(False, False)
        self.window.pack()

        self.window.create_rectangle(
            self.bd['x'], self.bd['y'],
            self.bd['x']+self.board_wh, self.bd['y']+self.board_wh
        )

        step_size = self.board_wh // (self.board_size - 1)

        #draw row, col=============
        for idx in range(step_size, self.board_wh-1, step_size):
            self.window.create_line(    #row
                self.bd['x'], self.bd['y']+idx,
                self.bd['x']+self.board_wh, self.bd['y']+idx
            )
            self.window.create_line(    #col
                self.bd['x']+idx, self.bd['y'],
                self.bd['x']+idx, self.bd['y']+self.board_wh
            )
        #End=======================

        #draw cross dot============
        for idx in range((self.board_size - 2) ** 2):   #board inner range
            x = idx % (self.board_size - 2) + 1
            y = idx // (self.board_size - 2) + 1
            
            self.window.create_oval(
                self.bd['x'] - 3 + (x * step_size), self.bd['y'] - 3 + (y * step_size),
                self.bd['x'] + 3 + (x * step_size), self.bd['y'] + 3 + (y * step_size),
                fill='gray'
            )
        #End=======================


        # exit()
    # def callback(self, event):
    #     print(f'{event.x}, {event.y}')
        
    def print(self):
        self.root.mainloop()


if __name__ == '__main__':
    now_board = ((5, 5), (2, 2), (3, 3))

    
    gui = GUI(board_size=5, black_info=2, white_info=0)

    # gui.located()
    gui.print()