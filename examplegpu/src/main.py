import torch
from dataloader.mnist_dataloader import MNISTDataLoader
from model_test import model_test
from model_train import model_train
from models.cnn import CNN, CNNConfig
from torch import nn, optim


def main() -> None:
    """Main function to load data, train and test the model."""
    # Set up the configuration
    import os

    print(os.getcwd())
    raise ValueError
    batch_size: int = 64
    num_epochs: int = 5
    learning_rate: float = 0.001
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device {device}")

    model_config = CNNConfig()

    # Initialize the MNIST DataLoader for training and testing
    train_loader = MNISTDataLoader(batch_size=batch_size, train=True)
    test_loader = MNISTDataLoader(batch_size=batch_size, train=False)

    # Set up the model, loss function, and optimizer
    model = CNN(model_config)

    # If more than one GPU is available, use DataParallel
    if torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs!")
        model = nn.DataParallel(model)

    model = model.to(device)  # Move model to GPU

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    model_train(
        model=model,
        data_loader=train_loader,
        criterion=criterion,
        optimizer=optimizer,
        device=device,
        num_epochs=num_epochs,
    )

    # Test the model
    model_test(model, test_loader, device)


if __name__ == "__main__":
    main()
