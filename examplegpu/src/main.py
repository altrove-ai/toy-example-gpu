import os
import time
import nvidia.dali as dali
import torch
from dataloader.mnist_dataloader import MNISTDataLoader
from dotenv import load_dotenv
from logger import LocalLogger, WandbLogger
from model_test import model_test
from model_train import model_train
from models.cnn import CNN, CNNConfig
from nvidia.dali import types
from torch import nn, optim

load_dotenv()


def load_data_with_dali(batch_size=32, num_threads=4, device_id=0, data_dir="random_dataset"):
    # Define the DALI Pipeline
    pipeline = dali.pipeline.Pipeline(
        batch_size=batch_size, num_threads=num_threads, device_id=device_id
    )

    with pipeline:
        # List all the .pt files in the directory (where your random arrays are saved)
        file_list = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".pt")]

        # Use ExternalSource to load the data from the .pt files
        data = dali.ops.ExternalSource(source=file_list, num_outputs=1, skip_warmup=True)
        data = dali.ops.Cast(device="gpu", dtype=types.FLOAT)(data)  # Now properly applied after data is loaded
        data = dali.ops.Reshape(device="gpu", shape=[-1, 100, 100])(data) 

        # Set pipeline outputs
        pipeline.set_outputs(data)

    pipeline.build()
    for _ in range(10):
        data = pipeline.run()
        print(data[0].shape)
    return data


def main() -> None:
    """Main function to load data, train and test the model."""
    # Set up the configuration
    batch_size: int = 64
    num_epochs: int = 5
    learning_rate: float = 0.001
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    t_start = time.time()
    useless_data = load_data_with_dali()
    print(f"Loading useless data time: {time.time() - t_start:.2f}")

    wandb_config = {
        "learning_rate": learning_rate,
        "optimizer": "adam",
    }
    run_name = f"run_{os.getenv('SLURM_JOB_ID', '0')}_{os.getenv('SLURM_PROCID', '0')}"
    logger = LocalLogger(f"_logs/{run_name}.log")
    # logger = WandbLogger(project_name="test_run_horace", run_name=run_name, config=wandb_config)

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
    with logger:
        model_train(
            model=model,
            data_loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            logger=logger,
            num_epochs=num_epochs,
        )

    # Test the model
    model_test(model, test_loader, device)


if __name__ == "__main__":
    main()
