import os

import torch


def generate_random_data(n, shape=(100, 100), dtype=torch.float32):
    """
    Generate a dataset of random arrays of shape (n, 100, 100).
    """
    return torch.rand(n, *shape, dtype=dtype)


def save_to_pytorch_tensor(data, filename):
    """
    Save the data as a PyTorch tensor in a specified file.
    """
    torch.save(data, filename)
    print(f"Saved {filename}")


def split_data_and_save(data, output_dir, batch_size=10000):
    """
    Split the dataset into smaller files, each containing batch_size examples.
    """
    os.makedirs(output_dir, exist_ok=True)

    total_samples = data.shape[0]
    num_batches = (total_samples + batch_size - 1) // batch_size  # Calculate number of batches

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_samples)
        batch_data = data[start_idx:end_idx]

        filename = os.path.join(output_dir, f"data_batch_{i + 1}.pt")
        save_to_pytorch_tensor(batch_data, filename)


def main():
    n = 100000  # Total number of random arrays
    shape = (100, 100)  # Shape of each array
    output_dir = "random_dataset"  # Directory to store the split files

    # Generate random data
    data = generate_random_data(n, shape)

    # Split data into smaller files and save them
    split_data_and_save(data, output_dir)


if __name__ == "__main__":
    main()
