import numpy as np

class DataBook:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size

        self.state = []
        self.policy_y = []
        self.value_y = []

    def add_data(self, data_dict):
        check_datas = ('state', 'policy_y', 'value_y')

        for name in check_datas:
            if name in data_dict.keys():
                self.__dict__[name].extend(data_dict[name])

    def get_data(self, shuffle=False):
        dataset_len = len(self.state)

        state = np.asarray(self.state, dtype=np.float64)
        policy_y = np.asarray(self.policy_y, dtype=np.float64).reshape(dataset_len, -1)
        value_y = np.asarray(self.value_y, dtype=np.float64).reshape(-1, 1)

        if shuffle:
            idx = np.array(range(dataset_len))
            np.random.shuffle(idx)

            state = state[idx]
            policy_y = policy_y[idx]
            value_y = value_y[idx]

        return {
            'x': state,
            'policy_y': policy_y,
            'value_y': value_y
        }
