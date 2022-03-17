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
                self.__dict__[name].append(data_dict[name])
