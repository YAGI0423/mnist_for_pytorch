import matplotlib.pyplot as plt

from torch.utils.data import DataLoader
from mnistForPytorch.datasets import MnistDataset


if __name__ == '__main__':
    dataLoader = DataLoader(
        MnistDataset(
            is_train=True,
            flatten=False,
            normalize=True,
            root='./mnist'
        ),
        batch_size=4,
        shuffle=False,
    )


    plt.figure(figsize=(9, 3))
    plt.suptitle('Samples', fontsize=12, fontweight='bold')

    batch_sample = next(iter(dataLoader))

    for idx, (x, y) in enumerate(zip(*batch_sample), 1):
        plt.subplot(1, 4, idx)
        plt.axis('off')
        
        plt.title(f'label: {int(y)}')
        plt.imshow(x, cmap='gray')

    plt.show()
        