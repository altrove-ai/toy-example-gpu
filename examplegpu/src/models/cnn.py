import torch
import torch.nn.functional as F
from pydantic import BaseModel
from torch import nn


class CNNConfig(BaseModel):
    """Configuration class to hold hyperparameters and model configuration."""

    in_channels: int = 1
    out_channels: int = 10
    hidden_units: int = 128


class CNN(nn.Module):
    """A simple CNN model for MNIST."""

    def __init__(self, config: CNNConfig):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(config.in_channels, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, config.hidden_units)
        self.fc2 = nn.Linear(config.hidden_units, config.out_channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
