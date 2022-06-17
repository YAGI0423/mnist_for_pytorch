from util import Util

from dataBook import DataBook
from gameBoard import GameBoard

class PlayGame:
    def __init__(self, board_size, rule):
        self.board_size = board_size
        self.discount_factor = 1.
        self.rule = rule
        
    def play(self, black, white, databook, diri_TF=False, gui=None):
        def get_value_y(seq_xy_board, win_code, discount_factor):
            turn_count = len(seq_xy_board)
            value_y = [0.] * turn_count

            if win_code < 2:
                for idx in range(turn_count):
                    value_y[idx] = float(win_code == (idx % 2)) * 2 - 1

                #discount factor
                gamma = 1.
                for idx in range(turn_count):
                    value_y[idx] *= gamma

                    if idx % 2:
                        gamma *= discount_factor
            return tuple(value_y)

        board = GameBoard()
        now_board = board.get_board()

        
        # gui.print_canvas()

        while self.rule.game_status(now_board)['during']:
            print("=" * 100)
            print(Util.seq_to_square(now_board, self.board_size))

            now_turn = Util.now_turn(now_board)
            now_player = black if now_turn else white

            print('\nnow turn: ', end='')
            print('Black') if now_turn else print('White')

            act = now_player.act(now_board, diri_TF)
            act_loc = act['xy_loc']

            board.put_stone(*act_loc)

            databook.add_data(act)

            print(f'\nact loc: {act_loc}\n\n')
            now_board = board.get_board()

            #when repeat pass stone
            if now_board[-4:].count((0, self.board_size)) >= 4:
                loc = list(self.rule.get_able_loc(now_board))
                loc.remove((None, None))
                loc.remove((0, self.board_size))

                board.put_stone(*loc[0])
                now_board = board.get_board()

            #gui====================
            if gui:
                policy_predict = act['pnn']
                value_predict = act['vnn']

                gui.update_canvas(
                    stone_info={'x': act_loc[0], 'y': act_loc[1], 'idx': len(now_board)-1},
                    vnn_info=value_predict, pnn_info=policy_predict
                )
                gui.print_canvas()
            #End====================
        if gui:
            gui.clear_canvas()


        win_code = self.rule.game_status(now_board)['win']

        print('winner:', win_code, end='\n\n')

        value_y = get_value_y(now_board, win_code, discount_factor=self.discount_factor)
        databook.add_data({'value_y': value_y})

        return win_code


if __name__ == '__main__':
    import model
    from rule import Rule

    import os

    def win_seq_checker(win_seq, board_size):
        win_seq_check_TF = win_seq > 7 or win_seq < 3    #seq
        win_seq_check_TF = win_seq_check_TF or win_seq > board_size
        return win_seq_check_TF

    def get_agent(agent_code, board_size, rule):
        def get_main_agent_dir():
            main_root = './model/main_model/'
            model_list = os.listdir(main_root)
            if model_list:   #Exist
                return main_root + model_list[0]
            return None   #Empty

        if agent_code == 0:   #user
            return model.User(board_size=board_size, rule=rule)
        elif agent_code == 1:   #random
            return model.RandomChoice(board_size=board_size, rule=rule)
        return model.AlphaO(
            board_size=board_size, rule=rule,
            model_dir=get_main_agent_dir()
        )   #alphaO


    board_size = 0
    win_seq = 0
    
    black = None
    white = None

    black, white = -1, -1
    
    while board_size > 19 or board_size < 3:
        board_size = input('Board size(3 ~ 19): ')
        board_size = int(board_size)


    while win_seq_checker(win_seq, board_size):
        win_seq = input(f'win seq(3 ~ 7 and small then board_size({board_size}): ')
        win_seq = int(win_seq)

    while not black in (0, 1, 2):
        black = input('black stone(0: user, 1: random, 2: alphaO): ')
        black = int(black)

    while not white in (0, 1, 2):
        white = input('white stone(0: user, 1: random, 2: alphaO): ')
        white = int(white)


    rule = Rule(board_size=board_size, win_seq=win_seq)
    play_game = PlayGame(board_size=board_size, rule=rule)
    databook = DataBook()

    black = get_agent(black, board_size, rule)
    white = get_agent(white, board_size, rule)

    play_game.play(black=black, white=white, databook=databook)
    
