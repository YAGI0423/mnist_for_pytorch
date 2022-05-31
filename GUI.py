from tkinter import *
import tkinter.font

class GUI:
    def __init__(self, board_size, black_info, white_info):
        def get_step_tuple():
            step_size = self.board_wh // (self.board_size - 1)
            left_pix = self.board_wh % (self.board_size - 1)

            step_list = list()
            temp = step_size
            while temp < self.board_wh:
                if left_pix > 0:
                    temp += 1

                step_list.append(temp)

                temp += step_size
                left_pix -= 1
            return tuple(step_list)

        def init_window(root):
            root.title('board window')
            root.geometry(f"{self.wd['width']}x{self.wd['height']}+100+100")
            root.resizable(False, False)

        def init_board(root, step_tuple):
            board = Canvas(root, width=self.wd['width'], height=self.wd['height'])

            
            board.create_rectangle(
                self.bd['x'], self.bd['y'],
                self.bd['x']+self.board_wh, self.bd['y']+self.board_wh
            )

            #draw row, col=============
            for step in step_tuple:
                board.create_line(    #row
                    self.bd['x'], self.bd['y']+step,
                    self.bd['x']+self.board_wh, self.bd['y']+step
                )
                board.create_line(    #col
                    self.bd['x']+step, self.bd['y'],
                    self.bd['x']+step, self.bd['y']+self.board_wh
                )
            #End=======================

            #draw cross dot============
            for step_y in step_tuple:
                for step_x in step_tuple:
                    board.create_oval(
                        self.bd['x'] - 3 + step_x, self.bd['y'] - 3 + step_y,
                        self.bd['x'] + 3 + step_x, self.bd['y'] + 3 + step_y
                    )
            #End=======================


            board.pack()

        def init_state(root):
            stone_ft = tkinter.font.Font(size=20)

            black_stone_txt = Label(root, text='● User', font=stone_ft)
            white_stone_txt = Label(root, text='AlphaO ○', font=stone_ft)
    

            black_stone_txt.place(x=self.bd['x'], y=10)
            white_stone_txt.place(x=self.wd['width']-self.bd['x'], y=10, anchor='ne')
           

        self.board_size = board_size
        self.black_info, self.white_info = black_info, white_info

        self.wd = {'width': 700, 'height': 800} #wd: `window`의 줌말

        self.bd = {'x': 30}   #bd: `board`의 줌말, 시작 x, y 좌표


        self.step_tuple = get_step_tuple()
        self.stone_size = self.step_tuple[0] // 1.2

        self.space = self.bd['x'] + (self.stone_size // 2)

        self.board_wh = self.wd['width'] - self.bd['x'] * 2 #board size
        self.bd['y'] = self.wd['height'] - self.board_wh - self.bd['x'] #get bd_y
        print(self.stone_size)


        print(self.step_tuple)


        self.root = Tk()
        init_window(self.root)
        init_board(self.root, self.step_tuple)

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

    
    gui = GUI(board_size=10, black_info=2, white_info=0)

    # gui.located()
    gui.print()