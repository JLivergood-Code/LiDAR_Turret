import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from pointnet_class import PointNetCls

# Example dataset (replace with your real one)
class LidarDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir):
        import os, numpy as np
        self.files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.npy')]

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        import numpy as np
        points = np.load(self.files[idx])  # (N,3)
        label = int(self.files[idx].split('_')[-1].replace('.npy', ''))  # crude example
        points = torch.tensor(points, dtype=torch.float32)
        points = points.transpose(0, 1)  # -> (3, N)
        return points, label


def train_pointnet(data_dir, num_classes=3, epochs=30, batch_size=8, lr=1e-3, device='cuda'):
    dataset = LidarDataset(data_dir)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = PointNetCls(k=num_classes).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        total_loss, correct, total = 0, 0, 0

        for points, labels in loader:
            points, labels = points.to(device), labels.to(device)
            optimizer.zero_grad()

            outputs = model(points)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        print(f"Epoch [{epoch+1}/{epochs}] Loss: {total_loss/len(loader):.4f} | Acc: {100*correct/total:.2f}%")

    torch.save(model.state_dict(), "pointnet_model.pth")
    print("✅ Model saved as pointnet_model.pth")


if __name__ == "__main__":
    data_dir = "./data/train"
    train_pointnet(data_dir)

