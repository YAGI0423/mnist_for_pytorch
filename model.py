import rule
from tree import Node

import numpy as np
import tensorflow as tf
from tensorflow import keras as K


class RandomChoice(rule.Rule):
    def __init__(self, board_size):
        super().__init__(board_size)
        self.board_size = board_size

    def act(self, board):
        able_loc_tup = super().get_able_location(board)
        rand_idx = np.random.choice(len(able_loc_tup))
        return able_loc_tup[rand_idx]


class AlphaO():
    def __init__(self, board_size):
        self.rule = rule.Rule(9)
        self.board_size = board_size
        self.model = self.__get_model()

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

    def predict_stone(self, list_board):
        #MCTS tree search

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

        def xy_to_idx(list_board):
            #convert x, y location to idx
            loc2idx = tuple(   #able loc -> idx
                x + y * self.board_size for x, y in list_board
            )
            return loc2idx

        def get_idx_to_loc(branch_idx):
            #convert branch idx, to x, y location
            x = branch_idx % self.board_size
            y = branch_idx // self.board_size
            return x, y

        def select_branch(node):
            #Evaluate Branch and Select
            #return branch idx
            total_n = node.total_visit

            def score_branch(branch_idx):
                #Calculate Branch Value
                q = node.get_expected_value(branch_idx)
                p = node.get_prior(branch_idx)
                n = node.get_visit(branch_idx)
                return q + self.c * p * np.sqrt(total_n) / (n + 1)
            return max(node.get_branches_keys(), key=score_branch)

        def model_predict(list_board):
            #get policy, value
            def get_input_data(list_board):
                #list_board ==> moel input tensor
                square_board = get_square_board(list_board)
                black_board = filt_board(square_board, -1)
                white_board = filt_board(square_board, 1)

                turn_board = np.zeros((self.board_size, self.board_size))
                if len(list_board) % 2 == 1:   #백 차례일 때, 1
                    turn_board[:] = 1.

                input_tensor = np.array((black_board, white_board, turn_board))
                input_tensor = input_tensor.reshape(1, self.board_size, self.board_size, 3)
                return input_tensor

            input_board = get_input_data(list_board)
            policy_pred, value_pred = self.model(input_board)
            policy_pred = np.array(policy_pred[0])
            value_pred = np.array(value_pred[0][0])
            return policy_pred, value_pred

        def create_node(list_board, parent):
            policy_pred, value_pred = model_predict(list_board)

            #get node's branches
            able_loc = self.rule.get_able_location(list_board)   #oly able loc
            idx_board = xy_to_idx(able_loc)
            branches = {idx: policy_pred[idx] for idx in idx_board}

            node = Node(
                state=list_board,
                value=value_pred,
                parent=parent,
                branches=branches
            )
            return node


        root = create_node(list_board, None)
        print(root.state)
        print(root.branches)
        exit()

        #Select Branch
        #가지 선택 과제 수행 필요
        for round in range(1):
            node = root
            branch_idx = select_branch(node)

            while node.has_child(branch_idx):
                #has child: follow root, no child: stop
                pass   #일단 child가 없어서 넘어가진다.


            #선택된 가지(branch_idx)를 바탕으로
            #state 만들기
            #tree class에 branch_idx를 입력하면
            #state 반환하도록 하기

            #idx를 x, y좌표로 변환
            loc = get_idx_to_loc(branch_idx)

            #현재 board의 좌표에 돌 놓기
            branch_board = list(node.state)
            branch_board.append(loc)
            branch_board = tuple(branch_board)

            child = create_node(branch_board, parent=node)
            exit()


        print(root)
        print(root.state)
        exit()


    def act(self, list_board):
        self.predict_stone(list_board)
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
