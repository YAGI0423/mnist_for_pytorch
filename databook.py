import json
import numpy as np

class Databook:
    def __init__(self):
        self.state = list()
        self.policy_y = list()
        self.value_y = list()

    def add_data(self, dataset):
        def check_dataset_validation(dataset):
            '''
            * 데이터셋 유효성 검사
            * (1) 데이터셋 요소(`state`, `policy_y`, `value_y`) 존재 확인
            * (2) 데이터셋 요소 간, 데이터 수 일치 확인
            '''
            for key in ('state', 'policy_y', 'value_y'):    #입력 dataset 유효성 검증
                if not key in dataset.keys():
                    raise Exception(f'[dataset] must have `state`, `policy_y`, `value_y`')
        
            check_data_size = len(dataset['state']) #각 데이터 사이즈 검사
            for key in ('policy_y', 'value_y'):
                if not len(dataset[key]) == check_data_size:
                    raise Exception(
                        f'[dataset] size must be same between `state`, `policy_y`, `value_y`'
                    )

        check_dataset_validation(dataset=dataset)

        for key in ('state', 'policy_y', 'value_y'):
            self.__dict__[key].extend(dataset[key])

    def size(self):
        dataset_size = len(self.state)

        for data in (self.policy_y, self.value_y):
            if not len(data) == dataset_size:
                raise Exception(
                    f'[dataset] size must be same between `state`, `policy_y`, `value_y`'
                )
        return dataset_size

    def print_dataset_shape(self):
        print('\n' + 'DATASET SHAPE'.center(50, '='))
        for key in ('state', 'policy_y', 'value_y'):
            shape = np.shape(self.__dict__[key])
            print(f'{key:>10} shape: {shape}')
        print('=' * 50, end='\n\n\n')

    def save_databook(self, file_type: str='txt'):
        if file_type == 'json':
            databook = {
                'state': self.state,
                'policy_y': self.policy_y,
                'value_y': self.value_y,
            }
            with open('./databook/databook.json', 'w') as json_file:
                json.dump(databook, json_file)
        if file_type == 'txt':
            pass