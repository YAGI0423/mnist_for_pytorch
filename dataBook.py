import numpy as np
import random

from gym import data_augment

class DataBook:
    def __init__(self):
        self.state = []
        self.policy_y = []
        self.value_y = []

    def update_databook(self, buffer_size):
        state_policy_TF = len(self.state) == len(self.policy_y)
        policy_value_TF = len(self.policy_y) == len(self.value_y)

        if state_policy_TF and policy_value_TF:   #must dataset size is same
            over_num = len(self.state) - buffer_size

            if over_num > 0:
                del_idx = np.random.choice(
                    range(len(self.state)), replace=False, size=over_num
                )
                
                del_idx.sort()
                
                for idx in del_idx[::-1]:
                    del self.state[idx]
                    del self.policy_y[idx]
                    del self.value_y[idx]
        else:
            raise

    def add_data(self, data_dict):
        check_datas = ('state', 'policy_y', 'value_y')

        for name in check_datas:
            if name in data_dict.keys():
                if name == 'policy_y':
                    self.__dict__[name].append(data_dict[name])
                else:
                    self.__dict__[name].extend(data_dict[name])

    def get_data(self, shuffle=False, augment_rate=None):
        def data_augment(x, policy_y, value_y, rate=0.3):
            data_len = len(value_y)
            augment_num = int(data_len * rate)

            aug_idx_list = random.choices(range(data_len), k=augment_num)

            aug_x = x[aug_idx_list].copy()
            aug_policy_y = policy_y[aug_idx_list].copy()
            aug_value_y = value_y[aug_idx_list].copy()

            aug_x = np.rot90(aug_x, k=random.randint(1, 4), axes=(1, 2))
            if random.randint(0, 2):
                aug_x = np.flip(aug_x, axis=2)
            
            x = np.concatenate((x, aug_x), axis=0)
            policy_y = np.concatenate((policy_y, aug_policy_y))
            value_y = np.concatenate((value_y, aug_value_y))

            return x, policy_y, value_y


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

        if augment_rate:
            state, policy_y, value_y = data_augment(state, policy_y, value_y, augment_rate)

        return {
            'x': state,
            'policy_y': policy_y,
            'value_y': value_y
        }
