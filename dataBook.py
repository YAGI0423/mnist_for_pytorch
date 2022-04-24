import numpy as np

class DataBook:
    def __init__(self):
        self.state = []
        self.policy_y = []
        self.value_y = []

    def update_databook(self, buffer_size):
        state_policy_TF = len(self.state) == len(self.policy_y)
        policy_value_TF = len(self.policy_y) == len(self.value_y[0])

        print(self.policy_y)
        print(self.value_y)

        if state_policy_TF and policy_value_TF:   #must dataset size is same
            print(self.policy_y)

            over_num = len(self.state) - buffer_size

            if over_num > 0:
                del_idx = np.random.choice(
                    range(len(self.state)), replace=False, size=over_num
                )
                
                for idx in del_idx:
                    del self.state[idx]
                    del self.policy_y[idx]
                    del self.value_y[0][idx]
        else:
            raise

    
        print(self.policy_y)
        print(self.value_y)
        
        exit()

    def add_data(self, data_dict):
        check_datas = ('state', 'policy_y', 'value_y')

        for name in check_datas:
            if name in data_dict.keys():
                self.__dict__[name].append(data_dict[name])

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
