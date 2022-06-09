from tree import Node
from util import Util

import time
import numpy as np
from tensorflow import keras as K

class User:
    def __init__(self, board_size, rule):
        self.board_size = board_size
        self.rule = rule

    def act(self, seq_xy_board, diri_TF):
        def check_input(message):
            #check user input value
            while True:
                input_data = input(f"{message}: ")
                if (input_data) == "": continue  #빈 값
                if input_data == "None": return None;   #None값
                try:
                    input_data = int(input_data)   #정수값
                    return input_data
                except:
                    continue

        while True:
            input_x, input_y = check_input("x"), check_input("y")
            able_loc = self.rule.get_able_loc(seq_xy_board)
            if (input_x, input_y) in able_loc: break;   #aleady put stone
        return {'xy_loc':(input_x, input_y)}


class RandomChoice:
    def __init__(self, board_size, rule):
        self.board_size = board_size
        self.rule = rule

    def act(self, seq_xy_board, diri_TF):
        able_loc = list(self.rule.get_able_loc(seq_xy_board))
        able_loc.remove((None, None))   #surrender
        rand_idx = np.random.choice(len(able_loc))
        return {'xy_loc': able_loc[rand_idx]}


class AlphaO:
    def __init__(self, board_size, rule, model_dir=None, lr=0.00002, round_num=1600):   
        self.board_size = board_size
        self.rule = rule

        self.lr = lr

        self.c = np.sqrt(2)
        self.diri_param = 0.03
        self.round_num = round_num

        self.model_dir = model_dir
        if self.model_dir is None:
            self.model = self.create_model()

            self.model.compile(
                optimizer=K.optimizers.SGD(learning_rate=self.lr, momentum=0.9),
                loss=['categorical_crossentropy', 'mse']
            )
            print(f'\n\ncreate new model...\n\n')
        else:
            self.model = K.models.load_model(model_dir, custom_objects={'LeakyReLU':K.layers.LeakyReLU()})
            
            self.model.compile(
                optimizer=K.optimizers.SGD(learning_rate=self.lr, momentum=0.9),
                loss=['categorical_crossentropy', 'mse']
            )

            print(f'\n\nload model from: {model_dir}\n\n')

    def create_model(self):
        input = K.layers.Input(shape=(self.board_size, self.board_size, 3))
        conv1 = K.layers.Conv2D(kernel_size=2, filters=64, activation='relu', padding="same")(input)
        conv2 = K.layers.Conv2D(kernel_size=2, filters=128, activation='relu', padding="same")(conv1)
        
        conv3 = K.layers.Conv2D(kernel_size=2, filters=256, activation='relu', padding="same")(conv2)
        conv3_batch = K.layers.BatchNormalization()(conv3)

        add_conv1 = K.layers.Conv2D(kernel_size=1, filters=256, activation='relu')(input)
        add1 = K.layers.Add()([conv3_batch, add_conv1])
        add_dense = K.layers.Dense(256, activation='relu')(add1)

        policy_conv = K.layers.Conv2D(kernel_size=2, filters=512, padding="same")(add_dense)
        policy_batch = K.layers.BatchNormalization()(policy_conv)
        policy_activ = K.layers.ReLU()(policy_batch)
        policy_flat = K.layers.GlobalAveragePooling2D()(policy_activ)

        policy_dense = K.layers.Dense(128, activation='relu')(policy_flat)
        policy_output = K.layers.Dense(self.board_size ** 2, activation="softmax", name="PNN")(policy_dense)


        value_conv = K.layers.Conv2D(kernel_size=2, filters=512, padding="same")(add_dense)
        value_batch = K.layers.BatchNormalization()(value_conv)
        value_activ = K.layers.ReLU()(value_batch)
        value_flat = K.layers.GlobalAveragePooling2D()(value_activ)
        
        value_dense = K.layers.Dense(128, activation='relu')(value_flat)
        value_dense2 = K.layers.Dense(128, activation='relu')(value_dense)
        value_output = K.layers.Dense(1, activation="tanh", name="VNN")(value_dense2)

        model = K.models.Model(inputs=input, outputs=[policy_output, value_output])
        return model

    def get_model_input(self, seq_xy_board):
        #list_board ==> moel input tensor

        def filt_board(square_board, stone_color):
            #filt squre board stone
            board = (square_board == stone_color)
            board = board.astype(np.float64)
            return board

        square_board = Util.seq_to_square(seq_xy_board, self.board_size)

        black_board = filt_board(square_board, -1)
        white_board = filt_board(square_board, 1)

        turn_board = np.zeros((self.board_size, self.board_size))
        if len(seq_xy_board) % 2 == 1:   #흑: 0, 백: 1
            turn_board[:] = 1.

        input_tensor = np.array((black_board, white_board, turn_board))
        input_tensor = np.transpose(input_tensor, (1, 2, 0))
        return input_tensor.reshape(1, self.board_size, self.board_size, 3)

    def predict_stone(self, seq_xy_board, diri_TF):
        #MCTS tree search

        #function====================================
        def seq_xy_to_idx(seq_xy_board):
            #convert x, y location to idx
            loc2idx = tuple(   #able loc -> idx
                x + y * self.board_size for x, y in seq_xy_board
            )
            return loc2idx

        def element_idx_to_xy(idx_loc):
            #convert branch idx, to x, y location
            x = idx_loc % self.board_size
            y = idx_loc // self.board_size
            return x, y

        def model_predict(seq_xy_board):
            #get policy, value
            input_board = self.get_model_input(seq_xy_board)
            policy_pred, value_pred = self.model(input_board)
            policy_pred = np.array(policy_pred[0])
            value_pred = np.array(value_pred[0][0])
            return policy_pred, value_pred

        def create_node(seq_xy_board, idx, parent, diri_TF=False):
            policy_pred, value_pred = model_predict(seq_xy_board)

            if diri_TF:
                diri_prob = np.random.dirichlet([self.diri_param] * (self.board_size ** 2))
                
                #previous_diri
                # policy_pred = (policy_pred * diri_prob) / np.sum(diri_prob)
                
                #new_diri
                policy_pred = (policy_pred + diri_prob) / 2.

            #get node's branches
            able_loc = self.rule.get_able_loc(seq_xy_board)

            #surrender is another algorithm
            able_loc = list(able_loc)
            able_loc.remove((None, None))
            able_loc = tuple(able_loc)

            seq_idx_board = seq_xy_to_idx(able_loc)

            policy_pred_len = len(policy_pred)
            branches = {idx: policy_pred[idx] for idx in seq_idx_board if idx < policy_pred_len}

            node = Node(
                state=seq_xy_board,
                value=value_pred,
                idx=idx,
                parent=parent,
                branches=branches
            )

            #add child to parent
            if parent is not None:
                parent.childrens[idx] = node
            return node

        def select_branch(node):
            #Evaluate Branch and Select
            #return branch idx
            total_n = node.total_visit

            def score_branch(branch_idx):
                #Calculate Branch Value
                q = node.get_expected_value(branch_idx)   #total value / visit
                p = node.get_prior(branch_idx)
                n = node.get_visit(branch_idx)
                return q + self.c * p * np.sqrt(total_n) / (n + 1)
            return max(node.get_branches_keys(), key=score_branch)
        #End=========================================


        root = create_node(seq_xy_board, idx=None, parent=None, diri_TF=diri_TF)

        for round in range(self.round_num):
            node = root
            branch_idx = select_branch(node)

            #explore tree
            while node.has_child(branch_idx):
                #has child: follow root, no child: stop
                node = node.childrens[branch_idx]
                branch_idx = select_branch(node)

            #create new state
            xy_loc = element_idx_to_xy(branch_idx)

            branch_board = list(node.state)
            branch_board.append(xy_loc)
            branch_board = tuple(branch_board)

            #create child node
            game_status = self.rule.game_status(branch_board)
            if game_status['during']:   #during
                child_node = create_node(branch_board, idx=branch_idx, parent=node)
                value = -1. * child_node.value
            else:   #done | is terminal node
                #draw: 0, win: -1
                value = 0. if game_status['win'] == 2 else 1.

            child_idx = branch_idx

            #record visit
            while node is not None:
                node.record_visit(child_idx, value)

                value = -1. * value
                child_idx = node.idx
                node = node.parent

        result_idx = max(root.branches.keys(), key=root.get_visit)
        return root, element_idx_to_xy(result_idx)

    def act(self, seq_xy_board, diri_TF):

        def get_policy_y(branches):
            policy_y = [0] * (self.board_size ** 2)

            for idx, value in branches.items():
                policy_y[idx] = value['visit']

            _sum = sum(policy_y)

            policy_y = tuple(value/_sum for value in policy_y)
            return policy_y

        root, xy_loc = self.predict_stone(seq_xy_board, diri_TF)
        print(f'value: {root.value:.3f}')

        return {
            'state': self.get_model_input(root.state),
            'policy_y': get_policy_y(root.branches),
            'xy_loc': xy_loc,
            'pnn': {idx: value['pior'] for idx, value in root.branches.items()},
            'vnn': root.value
        }

    def train_model(self, dataset, batch_size=1):
        history = self.model.fit(
            dataset['x'],
            [dataset['policy_y'], dataset['value_y']],
            batch_size = batch_size,
            shuffle=True,
            validation_split=0.2
        )
        return history

    def save_model(self, root_dir, idx, start_round, end_round):
         # #file name rule
        # #IDX_START EPOCH_END EPOCH_TIME.h5

        now = time.localtime()
        now = f'{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}'

        info_dir = f'{idx}_{start_round}_{end_round}_'

        self.model.save(root_dir + info_dir + now + '.h5')
