import pickle
import random
import numpy as np

class DataBook:
    def __init__(self, buffer_size=1024, window_size=128, load_dir=None):
        self.buffer_size = buffer_size
        self.window_size = window_size

        self.state = []
        self.policy_y = []
        self.value_y = []

        if load_dir:
            self.load_databook(load_dir)

    def add_data(self, data_dict):
        check_datas = ('state', 'policy_y', 'value_y')

        for name in check_datas:    
            if name in data_dict.keys():
                if name == 'policy_y':
                    self.__dict__[name].append(data_dict[name])
                else:
                    self.__dict__[name].extend(data_dict[name])

    def get_data(self, shuffle=False, augment_rate=None):
        def update_databook():
            state_policy_TF = len(self.state) == len(self.policy_y)
            policy_value_TF = len(self.policy_y) == len(self.value_y)

            if state_policy_TF and policy_value_TF:   #must dataset size is same
                over_num = len(self.state) - self.buffer_size

                if over_num > 0:
                    self.state = self.state[over_num:]
                    self.policy_y = self.policy_y[over_num:]
                    self.value_y = self.value_y[over_num:]
            else:
                raise

        def data_rot(x, policy_y, value_y, augment_num):
            split_num = augment_num // 4
            board_size = x[0].shape[:-1]

            aug_idx_list = np.random.choice(range(data_len), size=augment_num, replace=False)

            policy_y = policy_y.reshape(-1, *board_size)


            for idx in range(5):
                splited_idx = aug_idx_list[split_num*idx: split_num*(idx+1)].tolist()
                
                if splited_idx:
                    aug_x = x[splited_idx]
                    aug_policy_y = policy_y[splited_idx]

                    rot_rate = random.randint(1, 3)
                    aug_x = np.rot90(aug_x, k=rot_rate, axes=(1, 2))
                    aug_policy_y = np.rot90(aug_policy_y, k=rot_rate, axes=(1, 2))

                    if random.randint(0, 2):
                        aug_x = np.flip(aug_x, axis=2)
                        aug_policy_y = np.flip(aug_policy_y, axis=2)

                    #add augment data
                    x = np.concatenate((x, aug_x), axis=0)
                    policy_y = np.concatenate((policy_y, aug_policy_y))
            
            policy_y = policy_y.reshape(-1, board_size[0] ** 2)
            value_y = np.concatenate((value_y, value_y[aug_idx_list]))
            return x, policy_y, value_y

        def colour_transpose(x, policy_y, value_y, augment_num):
            aug_idx_list = np.random.choice(range(data_len), size=augment_num, replace=False)
            aug_x = x[aug_idx_list]

            black, white = aug_x[:, :, :, 0].copy(), aug_x[:, :, :, 1].copy()
            aug_x[:, :, :, 0] = white
            aug_x[:, :, :, 1] = black
            
            aug_x[:, :, :, 2] *= -1.
            aug_x[:, :, :, 2] += 1.

            x = np.concatenate((x, aug_x))
            policy_y = np.concatenate((policy_y, policy_y[aug_idx_list]))
            value_y = np.concatenate((value_y, value_y[aug_idx_list]))
            
            return x, policy_y, value_y

        update_databook()
        dataset_len = len(self.state)

        state = np.asarray(self.state, dtype=np.float64)
        policy_y = np.asarray(self.policy_y, dtype=np.float64).reshape(dataset_len, -1)
        value_y = np.asarray(self.value_y, dtype=np.float64).reshape(-1, 1)

        if dataset_len > self.window_size:
            return_idx = np.random.choice(range(dataset_len), size=self.window_size, replace=False).tolist()
            state = state[return_idx]
            policy_y = policy_y[return_idx]
            value_y = value_y[return_idx]

        if augment_rate:
            data_len = len(value_y)
            augment_num = int(data_len * augment_rate / 2)

            state, policy_y, value_y = data_rot(state, policy_y, value_y, augment_num=augment_num)
            state, policy_y, value_y = colour_transpose(state, policy_y, value_y, augment_num=augment_num)

        return {
            'x': state,
            'policy_y': policy_y,
            'value_y': value_y
        }

    def save_databook(self, save_dir):
        with open(save_dir, 'wb') as pick:
            save_databook = {
                'state': self.state,
                'policy_y': self.policy_y,
                'value_y': self.value_y
            }
            pickle.dump(save_databook, pick)

    def load_databook(self, load_dir):
        with open(load_dir, 'rb') as pick:
            data = pickle.load(pick)
    
        self.state = data['state']
        self.policy_y = data['policy_y']
        self.value_y = data['value_y']


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    databook = DataBook(buffer_size=65536, load_dir='./dataset/buffer_dataset.pickle')

    train_data = databook.get_data(shuffle=False, augment_rate=1.)
    
    train_x = train_data['x']
    policy_y = train_data['policy_y']
    value_y = train_data['value_y']

    print(len(databook.state))

    for idx in range(16):
        plt.subplot(16, 2, (idx+1)*2-1)
        plt.imshow(train_x[idx])

        plt.subplot(16, 2, (idx+1)*2)
        plt.imshow(policy_y[idx].reshape(3,3))
    plt.show()

