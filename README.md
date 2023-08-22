### 이 저장소(Repository)는 「Pytorch를 위한 MNIST 데이터셋 구현」에 대한 내용을 다루고 있습니다.

***
작성자: YAGI<br>

최종 수정일: 2023-08-05

+ 2023.08.04: 코드 작성 완료
+ 2023.08.05: README 작성 완료
+ 2023.08.05: 프로젝트 종료
***
<br>

***
+ 프로젝트 기간: 2023-08-04 ~ 2023-08-05
***
<br>

***
+ 해당 프로젝트는 Yann LeCun의 「MNIST handwritten digit database」(2010)를 바탕으로 하고 있습니다.

> LeCun, Y. & Cortes, C. (2010). MNIST handwritten digit database.
***
<br>

## 프로젝트 요약
&nbsp;&nbsp;
파이토치(Pytorch)의 'Dataset' 형식으로 된 MNIST 데이터셋을 제공합니다. 기존 파이토치 Dataset과 마찬가지로 DataLoader를 이용하여 순회 가능한 객체(Iterable)를 구현할 수 있습니다.
<br><br>

## Getting Start

### Get MNIST Dataset
```python
from torch.utils.data import DataLoader
from mnistForPytorch.datasets import MnistDataset

#is_train: True -> 학습 데이터, False -> 검증 데이터
#flatten: True -> 784, False -> 28 × 28
#normalize: True -> 0 ~ 1, False -> 0 ~ 255
#root: 데이터셋 저장 위치
dataset = MnistDataset(
    is_train=True,
    flatten=False,
    normalize=True,
    root='./mnistForPytorch/mnist'
)

#DataLoader
dataLoader = DataLoader(dataset, batch_size=4, shuffle=False)
```
***
<br><br>


## 개발 환경
**Language**

    + Python 3.9.12

    
**Library**

    + pytorch 1.12.0

<br><br>

## License
This project is licensed under the terms of the [MIT license](https://github.com/YAGI0423/mnist_for_pytorch/blob/main/LICENSE).