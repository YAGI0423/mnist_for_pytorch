import numpy as np

from util import Util

class DataBook:
    def __init__(self):
        self.state = []
        self.policy_y = []
        self.value_y = []

    def add_data(self, data_dict):
        check_datas = ('state', 'policy_y', 'value_y')

        for name in check_datas:
            if name in data_dict.keys():
                self.__dict__[name].extend(data_dict[name])

    def get_data(self):
        state = np.asarray(self.state, dtype=np.float64)
        policy_y = np.asarray(self.policy_y, dtype=np.float64).reshape(-1, 10)
        value_y = np.asarray(self.value_y, dtype=np.float64).reshape(-1, 1)

        return {
            'x': state,
            'policy_y': policy_y,
            'value_y': value_y
        }
