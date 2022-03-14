from tree import Node
from util import Util

import numpy as np
import tensorflow as tf
from tensorflow import keras as K

class User:
    def __init__(self, board_size, rule):
        self.board_size = board_size
        self.rule = rule

    def act(self, seq_xy_board):
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
            if (input_x, input_y) == (None, None): break;   #기권
        return (input_x, input_y)


class RandomChoice:
    def __init__(self, board_size, rule):
        self.board_size = board_size
        self.rule = rule

    def act(self, seq_xy_board):
        able_loc = self.rule.get_able_loc(seq_xy_board)
        rand_idx = np.random.choice(len(able_loc))
        return able_loc[rand_idx]


class AlphaO:
    def __init__(self, board_size, rule):
        self.board_size = board_size
        self.model = self.__get_model()
        self.rule = rule

        self.c = np.sqrt(2)

    def __get_model(self):
        input = K.layers.Input(shape=(self.board_size, self.board_size, 3))
        conv1 = K.layers.Conv2D(kernel_size=3, filters=64, activation="relu", padding="same")(input)

        flat = K.layers.Flatten()(conv1)
        dense1 = K.layers.Dense(256, activation="relu")(flat)

        policy_dense = K.layers.Dense(128, activation="relu")(dense1)
        policy_output = K.layers.Dense(self.board_size ** 2 + 1, activation="softmax", name="PNN")(policy_dense)

        value_dense = tf.keras.layers.Dense(128, activation="relu")(dense1)
        value_output = tf.keras.layers.Dense(1, activation="tanh", name="VNN")(value_dense)

        model = K.models.Model(inputs=input, outputs=[policy_output, value_output])
        return model

    def predict_stone(self, seq_xy_board):
        #MCTS tree search
        def filt_board(square_board, stone_color):
            #filt squre board stone
            board = (square_board == stone_color)
            board = board.astype(np.float64)
            return board

        def seq_xy_to_idx(seq_xy_board):
            #convert x, y location to idx
            loc2idx = tuple(   #able loc -> idx
                y * self.board_size + x for x, y in seq_xy_board
            )
            return loc2idx

        def element_idx_to_xy(idx_loc):
            #convert branch idx, to x, y location
            x = idx_loc % self.board_size
            y = idx_loc // self.board_size
            return x, y

        def model_predict(seq_xy_board):
            #get policy, value
            def get_input_data(seq_xy_board):
                #list_board ==> moel input tensor
                square_board = Util.seq_to_square(seq_xy_board, self.board_size)
                black_board = filt_board(square_board, -1)
                white_board = filt_board(square_board, 1)

                turn_board = np.zeros((self.board_size, self.board_size))
                if len(seq_xy_board) % 2 == 1:   #흑: 0, 백: 1
                    turn_board[:] = 1.

                input_tensor = np.array((black_board, white_board, turn_board))
                input_tensor = input_tensor.reshape(1, self.board_size, self.board_size, 3)
                return input_tensor

            input_board = get_input_data(seq_xy_board)
            policy_pred, value_pred = self.model(input_board)
            policy_pred = np.array(policy_pred[0])
            value_pred = np.array(value_pred[0][0])
            return policy_pred, value_pred

        def create_node(seq_xy_board, idx, parent):
            policy_pred, value_pred = model_predict(seq_xy_board)

            #get node's branches
            able_loc = self.rule.get_able_loc(seq_xy_board)
            seq_idx_board = seq_xy_to_idx(able_loc)
            branches = {idx: policy_pred[idx] for idx in seq_idx_board}

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


        root = create_node(seq_xy_board, idx=None, parent=None)

        #Select Branch
        for round in range(2000):
            node = root
            branch_idx = select_branch(node)

            while node.has_child(branch_idx):
                #has child: follow root, no child: stop
                node = node.childrens[branch_idx]
                branch_idx = select_branch(node)

            #선택된 가지(branch_idx)를 바탕으로
            #state 만들기
            #tree class에 branch_idx를 입력하면
            #state 반환하도록 하기

            #idx를 x, y좌표로 변환
            xy_loc = element_idx_to_xy(branch_idx)

            #현재 board의 좌표에 돌 놓기
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
                value = 0. if game_status['win'] == 2 else -1.

            child_idx = branch_idx

            #parent를 따라 방문 기록하기
            while node is not None:
                #node의 branch_idx를 기록하기
                node.record_visit(child_idx, value)

                value = -1. * value
                child_idx = node.idx
                node = node.parent

        print(root)
        for idx, value in root.branches.items():
            print(f'{idx}: {value}')

        exit()


    def act(self, seq_xy_board):
        self.predict_stone(seq_xy_board)
        exit()

        def get_square_board(list_board):
            square_board = np.zeros((self.board_size, self.board_size))
            for turn, (x, y) in enumerate(list_board):
                stone_color = -1 if turn % 2 == 0 else 1
                square_board[y][x] = stone_color
            return square_board

        def filt_board(square_board, stone_color):
            #filt squre board stone
            board = (square_board == stone_color)
            board = board.astype(np.float64)
            return board

        #모델 입력 데이터(=특징 평면)================
        square_board = get_square_board(list_board)
        black_board = filt_board(square_board, -1)
        white_board = filt_board(square_board, 1)

        turn_board = np.zeros((self.board_size, self.board_size))
        if len(list_board) % 2 == 1:   #백 차례일 때, 1
            turn_board[:] = 1.

        input_board = np.array((black_board, white_board, turn_board))
        input_board = input_board.reshape(1, self.board_size, self.board_size, 3)
        #End========================================

        policy_pred, value_pred = self.model(input_board)
        print(policy_pred, value_pred)
        exit()
        policy_pred = np.array(policy_pred[0], dtype=np.float32)

        #확률분포 조건(sum = 1)
        over = 1 - np.sum(policy_pred)
        policy_pred[-1] += over

        idx = np.random.choice(
            range(self.board_size ** 2 + 1),
            p=policy_pred
        )
        if idx == self.board_size: return (-1, -1)   #surrender
        return (idx % self.board_size, idx // self.board_size)


if __name__ == "__main__":
        model = AlphaO(9)

        list_board = [(0, 0), (5, 3)]
        print(model.act(list_board))
