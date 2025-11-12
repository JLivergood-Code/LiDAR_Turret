# lcas_dataset.py
import torch
from torch.utils.data import Dataset
import numpy as np
import open3d as o3d
import os
import random

class LCASDataset(Dataset):
    """
    Dataset loader for the L-CAS 3D Point Cloud People Dataset.
    Each .pcd file has an associated .txt annotation file.
    You can use this for classification (pedestrian, group, none, etc.)
    """

    def __init__(self, root_dir, split='train', npoints=2048, transform=None, augment=True):
        super().__init__()
        self.pcd_dir = os.path.join(root_dir, 'LCAS_20160523_1200_1218_pcd')
        self.label_dir = os.path.join(root_dir, 'LCAS_20160523_1200_1218_labels')
        self.files = []
        self.npoints = npoints
        self.transform = transform
        self.augment = augment

        # Only include files that have both a .pcd and a .txt
        for fname in os.listdir(self.pcd_dir):
            if fname.endswith('.pcd'):
                base = fname[:-4]
                txt_path = os.path.join(self.label_dir, base + '.txt')
                if os.path.exists(txt_path):
                    self.files.append(base)


        # Map category string to label index
        self.category_map = {
            'pedestrian': 0,
            'group': 1,
            'none': 2  # optional fallback
        }

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        base = self.files[idx]
        pcd_path = os.path.join(self.pcd_dir, base + '.pcd')
        label_path = os.path.join(self.label_dir, base + '.txt')

        # Load point cloud
        pcd = o3d.io.read_point_cloud(pcd_path)
        points = np.asarray(pcd.points, dtype=np.float32)

        # Randomly sample N points
        if len(points) >= self.npoints:
            choice = np.random.choice(len(points), self.npoints, replace=False)
        else:
            choice = np.random.choice(len(points), self.npoints, replace=True)
        points = points[choice, :]

        # Normalize
        points = points - np.mean(points, axis=0)
        dist = np.max(np.sqrt(np.sum(points ** 2, axis=1)))
        points = points / dist

        # Load first annotation label
        with open(label_path, 'r') as f:
            first_line = f.readline().strip().split()
        category = first_line[0].lower()
        label = self.category_map.get(category, 2)  # default to "none"

        # Data augmentation (random rotation + jitter)
        if self.augment:
            theta = random.uniform(0, 2 * np.pi)
            rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
            points[:, [0, 1]] = points[:, [0, 1]].dot(rot)
            points += np.random.normal(0, 0.02, size=points.shape)

        # To tensor: (3, N)
        points = torch.from_numpy(points.T).float()
        label = torch.tensor(label, dtype=torch.long)

        return points, label
