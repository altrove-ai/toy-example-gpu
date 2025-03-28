import torch
from logger import Logger
from torch import nn, optim
from torch.utils.data import DataLoader


def model_train(
    model: nn.Module,
    data_loader: DataLoader,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    device: torch.device,
    logger: Logger,
    num_epochs: int = 5,
) -> None:
    """Train the model on the training data."""
    model.train()
    for epoch in range(num_epochs):
        print(f"Starting epoch {epoch}")
        running_loss = 0.0
        correct = 0
        total = 0

        images: torch.Tensor
        labels: torch.Tensor
        for images, labels in data_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        actual_loss = running_loss / len(data_loader)
        accuracy = 100 * correct / total
        print(
            f"Epoch [{epoch + 1}/{num_epochs}], Loss: {actual_loss:.4f}, Accuracy: {accuracy:.2f}%"
        )
        logger.log(
            {
                "epoch": epoch,
                "loss": actual_loss,
                "accuracy": accuracy,
            }
        )
