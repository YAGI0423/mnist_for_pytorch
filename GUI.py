from tkinter import *

class GUI:
    def __init__(self, board_size, black_info, white_info):
        self.board_size = board_size
        self.black_info, self.white_info = black_info, white_info

        self.board_wh = 640
        
        self.root = Tk()
        self.window = Canvas(self.root, width=700, height=800)
        
        self.init_window()

        


    def init_window(self):
        self.root.title('board window')
        self.root.geometry('700x800+100+100')
        self.root.resizable(False, False)
        self.window.pack()

        self.window.create_rectangle(30, 130, 30+self.board_wh, 130+self.board_wh)


        for idx in range(self.board_size):
            step_size = self.board_wh // self.board_size
            
            self.window.create_line(30, 130+(), 30+self.board_wh, 130+self.board_wh)
            break

    # def callback(self, event):
    #     print(f'{event.x}, {event.y}')
        
    def print(self):
        self.root.mainloop()


if __name__ == '__main__':
    now_board = ((5, 5), (2, 2), (3, 3))

    
    gui = GUI(board_size=3, black_info=2, white_info=0)

    # gui.located()
    gui.print()