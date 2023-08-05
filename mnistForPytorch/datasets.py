from torchvision.datasets import MNIST
from torch.utils.data import Dataset

from torch import Tensor


class MnistDataset(Dataset):
    def __init__(self, is_train: bool=True,
                 flatten: bool=False, normalize: bool=False, root: str='./mnistForPytorch/mnist') -> None:
        
        self.x, self.y = self.__getMnist(root=root, is_train=is_train)
        
        if flatten:
            self.x = self.__flatten(self.x)
        if normalize:
            self.x = self.__minMax_normalize(self.x)

    def __len__(self) -> int:
        return self.x.__len__()

    def __getitem__(self, index) -> tuple[Tensor, Tensor]:
        return self.x[index], self.y[index]
    
    def __getMnist(self, root: str, is_train: bool) -> tuple[Tensor, Tensor]:
        mnist = MNIST(root, train=is_train, download=True)
        return mnist.data, mnist.targets
    
    def __flatten(self, x) -> Tensor:
        batch, height, weight = x.shape
        return x.reshape(batch, height * weight)

    def __minMax_normalize(self, x) -> Tensor:
        return x / x.max()