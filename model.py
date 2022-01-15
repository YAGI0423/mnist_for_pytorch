import numpy as np
import tensorflow as tf
from tensorflow import keras as K


class RandomChoice:
    def __init__(self, board_size):
        self.board_size = board_size

    def act(self, board):
        def get_able_location(board):
            #return able location
            able_loc = set(
                (x, y) \
                for x in range(self.board_size) \
                for y in range(self.board_size)
            )
            able_loc -= set(board)
            return tuple(able_loc)

        able_loc = get_able_location(board)
        rand_idx = np.random.choice(len(able_loc))
        return able_loc[rand_idx]


class AlphaO:
    def __init__(self, board_size):
        self.board_size = board_size
        self.model = self.__get_model()

    def __get_model(self):
        input = K.layers.Input(shape=(self.board_size, self.board_size, 1))
        conv1 = K.layers.Conv2D(kernel_size=3, filters=64, activation="relu", padding="same")(input)

        flat = K.layers.Flatten()(conv1)
        dense1 = K.layers.Dense(256, activation="relu")(flat)

        policy_dense = K.layers.Dense(128, activation="relu")(dense1)
        policy_output = K.layers.Dense(self.board_size ** 2 + 1, activation="softmax", name="PNN")(policy_dense)

        value_dense = tf.keras.layers.Dense(128, activation="relu")(dense1)
        value_output = tf.keras.layers.Dense(1, activation="tanh", name="VNN")(value_dense)

        model = K.models.Model(inputs=input, outputs=[policy_output, value_output])
        return model

    def act(self):
        pass


if __name__ == "__main__":
        model = AlphaO(9)

        test_input = np.zeros((1, 9, 9))
        print(model.model(test_input))
