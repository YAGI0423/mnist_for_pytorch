import tkinter as tk

class GUI:
    def __init__(self, board_size, black_info, white_info):
        self.black_info, self.white_info = black_info, white_info
        
        self.window = tk.Tk()
        self.init_window(board_size)

        self.window.bind('<Motion>', self.callback)

    def init_window(self, board_size):
        self.window.title('board window')
        self.window.geometry('700x800+100+100')
        self.window.resizable(False, False)

        self.window.create_rectangle(10, 10, 100, 100)



    # def callback(self, event):
    #     print(f'{event.x}, {event.y}')
        
    def print(self):
        self.window.mainloop()

    # def located(self):
    #     label = tk.Label(self.window, text='하이')
    #     label.pack()


if __name__ == '__main__':
    now_board = ((5, 5), (2, 2), (3, 3))

    
    gui = GUI(board_size=10, black_info=2, white_info=0)

    gui.located()
    gui.print()