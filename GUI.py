from tkinter import *
import tkinter.font

class GUI:
    def __init__(self, board_size, black_code, white_code):
        def get_step_tuple(step_size):
            left_pix = self.board_wh % step_size

            step_list = [0]
            temp = step_size
            while temp < self.board_wh:
                if left_pix > 0:
                    temp += 1

                step_list.append(temp)

                temp += step_size
                left_pix -= 1
            step_list.append(temp)
            return tuple(step_list)

        def init_window(root):
            root.title('board window')
            root.geometry(f"{self.wd['width']}x{self.wd['height']}+100+100")
            root.resizable(False, False)

        def init_board(canvas, step_tuple):
            canvas.create_rectangle(
                self.bd['x'], self.bd['y'],
                self.bd['x']+self.board_wh, self.bd['y']+self.board_wh
            )

            #draw row, col=============
            for step in step_tuple[1:-1]:
                canvas.create_line(    #row
                    self.bd['x'], self.bd['y']+step,
                    self.bd['x']+self.board_wh, self.bd['y']+step
                )
                canvas.create_line(    #col
                    self.bd['x']+step, self.bd['y'],
                    self.bd['x']+step, self.bd['y']+self.board_wh
                )
            #End=======================

            #draw cross dot============
            for step_y in step_tuple[1:-1]:
                for step_x in step_tuple[1:-1]:
                    canvas.create_oval(
                        self.bd['x'] - 3 + step_x, self.bd['y'] - 3 + step_y,
                        self.bd['x'] + 3 + step_x, self.bd['y'] + 3 + step_y
                    )
            #End=======================

        def init_state(root, black_code, white_code):
            def get_player_text(palyer_code):
                if palyer_code == 1:
                    return 'RANDOM_CHOICE'
                elif palyer_code == 2:
                    return 'α_O'
                return 'USER'

            black_text = '● ' + get_player_text(black_code)
            white_text = get_player_text(white_code) + ' ○'
            
            
            stone_ft = tkinter.font.Font(size=20)

            black_stone_txt = Label(root, text=black_text, font=stone_ft)
            white_stone_txt = Label(root, text=white_text, font=stone_ft)

            black_stone_txt.place(x=self.interval, y=15)
            white_stone_txt.place(x=self.wd['width']-self.interval, y=15, anchor='ne')


            predict_ft = tkinter.font.Font(size=15)
            black_vnn_txt = Label(root, text='VNN: ', font=predict_ft)
            white_vnn_txt = Label(root, text='VNN: ', font=predict_ft, state='disable')

            black_vnn_txt.place(x=self.interval+20, y=70)
            white_vnn_txt.place(x=self.wd['width']-self.interval-20, y=70, anchor='ne')

        def init_visual_stone():
            return self.board.create_oval( #visual stone 초기 위치
                self.wd['width'], 0, self.wd['width']+self.stone_size, self.stone_size, fill='dimgray'
            )

        def init_loc_text():
            return self.board.create_text(   #stone location text
                self.bd['x']*2, self.wd['height']-self.interval,
                text='stone location: ',
                font=('', 12)
            )

        def wheon_move_mouse(event):   #포석 위치 체크
            def get_is_inner_cross(x, y):
                x_bd_in_TF = x > self.bd['x'] - TOLERANCE and x < self.bd['x'] + self.board_wh + TOLERANCE
                y_bd_in_TF = y > self.bd['y'] - TOLERANCE and y < self.bd['y'] + self.board_wh + TOLERANCE

                if x_bd_in_TF and y_bd_in_TF:
                    x_cr_in_TF = (x - self.bd['x']) % self.board_step_size
                    x_cr_in_TF = x_cr_in_TF > (self.board_step_size - TOLERANCE) or x_cr_in_TF < TOLERANCE

                    y_cr_in_TF = (y - self.bd['y']) % self.board_step_size
                    y_cr_in_TF = y_cr_in_TF > (self.board_step_size - TOLERANCE) or y_cr_in_TF < TOLERANCE

                    return x_cr_in_TF and y_cr_in_TF
                return False

            def get_close_value(value, put_loc_tup):
                for step in put_loc_tup:
                    if abs(step - value) <= TOLERANCE:
                        return step

            def show_visual_stone(x, y):
                if not x:
                    x = self.wd['width']
                    y = 0
                
                self.board.moveto(self.visual_stone, x, y)

            def get_close_value_idx(value, put_loc_tup):
                for idx, step in enumerate(put_loc_tup):
                    if step == value:
                        return idx
                return idx

            TOLERANCE = 20  #포석 인정 허용 범위
            put_loc_tup = tuple([0] + list(self.step_tuple) + [self.step_tuple[-1] + self.board_step_size])
            x, y = event.x, event.y


            if get_is_inner_cross(x, y):
                b_x, b_y = x - self.bd['x'], y - self.bd['y']
                loc_x = get_close_value(b_x, self.step_tuple)
                loc_y = get_close_value(b_y, self.step_tuple)
                
                half_st = self.stone_size // 2
                show_visual_stone(loc_x+self.bd['x']-half_st, loc_y+self.bd['y']-half_st)

                loc_x_idx = get_close_value_idx(loc_x, self.step_tuple)
                loc_y_idx = get_close_value_idx(loc_y, self.step_tuple)
                self.board.itemconfig(self.loc_text, text=f'stone location: ({loc_x_idx}, {loc_y_idx})')
            else:
                show_visual_stone(None, None)


        self.board_size = board_size
        self.black_code, self.white_code = black_code, white_code


        self.interval = 30
        self.wd = {'width': 700, 'height': 800} #wd: `window`의 줌말
        
        self.board_step_size = (self.wd['width'] - self.interval * 2) // (self.board_size + 1)  #하나의 셀 크기
        self.stone_size = self.board_step_size // 1.25
        self.board_wh = self.board_step_size * (self.board_size - 1)  #board size

        self.step_tuple = get_step_tuple(step_size=self.board_step_size)

        self.bd = {'x': 30 + self.board_step_size}   #bd: `board`의 줌말, 시작 x, y 좌표
        self.bd['y'] = self.wd['height'] - self.bd['x'] - self.board_wh

        self.pre_idx_txt_ele = None #최근 stone idx `create_txt` 요소
        self.pnn_text_list = list() #pnn text element의 집합


        self.root = Tk()
        init_window(self.root)

        self.board = Canvas(self.root, width=self.wd['width'], height=self.wd['height'])
        init_board(self.board, self.step_tuple)
        self.board.pack()

        init_state(self.root, self.black_code, self.white_code)

        self.visual_stone = init_visual_stone()
        self.loc_text = init_loc_text()



        self.root.bind("<Motion>", wheon_move_mouse)
        
    def idx_to_pix(self, x, y):
        x = self.bd['x'] + self.step_tuple[x]
        y = self.bd['y'] + self.step_tuple[y]
        return x, y

    def draw_stone(self, x, y, stone_color):
        stone_color_txt = 'white' if stone_color else 'black'
        
        half_st = self.stone_size // 2
        
        x, y= self.idx_to_pix(x, y)
        x -= half_st
        y -= half_st

        stone_ele = self.board.create_oval(
            x, y, x+self.stone_size, y+self.stone_size,
            fill=stone_color_txt
        )
        return stone_ele

    def print_canvas(self):
        self.root.update()

    def update_canvas(
        self, stone_info, vnn_info, pnn_info
    ):
        x, y, stone_idx = stone_info['x'], stone_info['y'], stone_info['idx']
        vnn = vnn_info

        stone_color = 1 if stone_idx % 2 else 0
        self.draw_stone(x, y, stone_color)
        
        pix_x, pix_y = self.idx_to_pix(x, y)

        #stone_idx==============
        if self.pre_idx_txt_ele:    #최근 포석 idx txt color 복구
            stone_idx_txt_color = 'white' if stone_color else 'black'
            self.board.itemconfig(self.pre_idx_txt_ele, fill=stone_idx_txt_color)

        # stone_idx_txt_color = 'black' if stone_color else 'white'
        self.pre_idx_txt_ele = self.board.create_text(pix_x, pix_y, text=f'{stone_idx}', fill='red')  #포석 순서
        #End====================

        #vnn====================
        if stone_color: #white
            self.root.children['!label4'].config(text=f'VNN: {vnn:.3f}')  #white vnn
        else:   #black
            self.root.children['!label3'].config(text=f'VNN: {vnn:.3f}')   #black vnn
        #End====================

        #pnn====================
        # pnn_info = {idx: round(pior, 3) for idx, pior in pnn_info.items()}
        print(pnn_info)

        #remove previous element
        for pnn_ele in self.pnn_text_list:
            print(pnn_ele)
            self.board.delete(pnn_ele)
        #End====================

        def rgb_to_hex(r, g, b):
            return f'#{r:02x}{g:02x}{b:02x}'

        #create text============
        for idx, pior in pnn_info.items():
            if pior < 0.1: continue;
            
            txt_color = rgb_to_hex(0, 0, int(pior * 255))
            pior = round(pior, 3)

            x = idx % self.board_size
            y = idx // self.board_size
            
            pix_x, pix_y = self.idx_to_pix(x, y)

            ele = self.board.create_text(pix_x, pix_y-10, text=pior, fill=txt_color)
            self.pnn_text_list.append(ele)
        #End====================

        
        


if __name__ == '__main__':
    now_board = ((2, 1), (2, 2), (0, 0), (1, 2), (1, 0))
    vnn_list = (10, 2, 3, 4, 2)
    pnn_list = (
        {3: 0.037, 7: 0.05, 8: 0.109, 6: 0.05, 2: 0.897, 4: 0.06, 1: 0.024, 5: 0.243, 0: 0.13},
        {3: 0.037, 7: 0.03, 8: 0.109, 6: 0.05, 2: 0.297, 4: 0.06, 1: 0.024, 5: 0.243, 0: 0.13},
        {3: 0.037, 7: 0.06, 8: 0.109, 6: 0.05, 2: 0.297, 4: 0.06, 1: 0.024, 5: 0.243, 0: 0.13},
        {3: 0.037, 7: 0.02, 8: 0.109, 6: 0.05, 2: 0.297, 4: 0.06, 1: 0.024, 5: 0.243, 0: 0.13},
        {3: 0.037, 7: 0.07, 8: 0.109, 6: 0.05, 2: 0.297, 4: 0.06, 1: 0.024, 5: 0.243, 0: 0.13}
    )
    
    import time

    gui = GUI(board_size=3, black_code=2, white_code=0)

    
    # gui.root.mainloop()
    gui.print_canvas()

    for t in range(len(now_board)):

        x, y = now_board[t]
        vnn = vnn_list[t]
        pnn = pnn_list[t]

        stone_color = 1 if t % 2 else 0

        gui.update_canvas(
            stone_info={'x': x, 'y': y, 'idx': t},
            vnn_info=vnn, pnn_info=pnn
        )

        gui.print_canvas()
        time.sleep(2)

