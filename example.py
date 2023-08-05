import matplotlib.pyplot as plt

from torch.utils.data import DataLoader
from mnistForPytorch.datasets import MnistDataset


def sample_show(batch_sample) -> None:
    iters = zip(*batch_sample)

    plt.figure(figsize=(9, 3))
    plt.suptitle('Samples', fontsize=12, fontweight='bold')

    for idx, (x, y) in enumerate(iters, 1):
        plt.subplot(1, 4, idx)
        plt.axis('off')
        
        plt.title(f'label: {int(y)}')
        plt.imshow(x, cmap='gray')

    plt.show()


if __name__ == '__main__':
    dataLoader = DataLoader(
        MnistDataset(
            is_train=True,
            flatten=False,
            normalize=True,
            root='./mnistForPytorch/mnist'
        ),
        batch_size=4,
        shuffle=True,
    )

    batch_sample = next(iter(dataLoader))
    sample_show(batch_sample)
        