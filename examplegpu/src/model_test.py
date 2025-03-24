import torch
from torch import nn, optim
from torch.utils.data import DataLoader


def model_test(
    model: nn.Module,
    data_loader: DataLoader,
    device: torch.device,
) -> None:
    """Test the model on the test data."""
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in data_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"Accuracy on test set: {100 * correct / total:.2f}%")
