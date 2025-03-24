from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class MNISTDataLoader(DataLoader):
    """Custom DataLoader class for MNIST dataset."""

    def __init__(
        self, batch_size: int = 64, train: bool = True, root: str = "./_data", **kwargs
    ) -> None:
        # Choose between training and test dataset
        self.train = train
        self.transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
        )

        # Initialize the dataset
        if self.train:
            dataset = datasets.MNIST(root=root, train=True, download=True, transform=self.transform)
        else:
            dataset = datasets.MNIST(
                root=root, train=False, download=True, transform=self.transform
            )

        # Initialize the DataLoader with the provided arguments
        super(MNISTDataLoader, self).__init__(
            dataset, batch_size=batch_size, shuffle=True, **kwargs
        )
