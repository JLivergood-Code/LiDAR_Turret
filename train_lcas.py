# train_lcas.py
from __future__ import print_function
import argparse
import os
import random
import torch
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
import torch.nn.functional as F
from tqdm import tqdm
import numpy as np
import open3d as o3d

from pointnet.model import PointNetDenseCls, feature_transform_regularizer

# -------------------------
# Dataset definition
# -------------------------
from torch.utils.data import Dataset

class LCASDataset(Dataset):
    def __init__(self, pointcloud_dir, label_dir, npoints=2500, classification=False):
        self.pc_files = sorted([os.path.join(pointcloud_dir, f) for f in os.listdir(pointcloud_dir) if f.endswith('.pcd')])
        self.label_files = sorted([os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith('.label')])
        assert len(self.pc_files) == len(self.label_files), "Mismatch between PCDs and label files"
        self.npoints = npoints
        self.classification = classification

        # Determine number of segmentation classes
        all_labels = []
        for f in self.label_files:
            all_labels.append(np.loadtxt(f, dtype=np.int64))
        self.num_seg_classes = int(max([labels.max() for labels in all_labels])) + 1  # assuming labels start at 0

    def __len__(self):
        return len(self.pc_files)

    def __getitem__(self, idx):
        # Load point cloud
        pcd = o3d.io.read_point_cloud(self.pc_files[idx])
        points = np.asarray(pcd.points, dtype=np.float32)

        # Load labels
        labels = np.loadtxt(self.label_files[idx], dtype=np.int64)

        # Resample points
        if len(points) >= self.npoints:
            choice = np.random.choice(len(points), self.npoints, replace=False)
        else:
            choice = np.random.choice(len(points), self.npoints, replace=True)

        points = points[choice, :]
        labels = labels[choice]

        # Normalize points (center + scale)
        points = points - np.mean(points, axis=0)
        dist = np.max(np.sqrt(np.sum(points ** 2, axis=1)))
        points = points / dist

        points = torch.from_numpy(points).float()
        labels = torch.from_numpy(labels).long()

        if self.classification:
            label = labels[0]
            return points, label
        else:
            return points, labels

# -------------------------
# Argument parsing
# -------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--batchSize', type=int, default=16, help='input batch size')
parser.add_argument('--workers', type=int, default=4, help='number of data loading workers')
parser.add_argument('--nepoch', type=int, default=25, help='number of epochs to train for')
parser.add_argument('--outf', type=str, default='seg', help='output folder')
parser.add_argument('--model', type=str, default='', help='model path')
parser.add_argument('--pointcloud_dir', type=str, required=True, help='folder with PCD files')
parser.add_argument('--label_dir', type=str, required=True, help='folder with label files')
parser.add_argument('--feature_transform', action='store_true', help="use feature transform")

opt = parser.parse_args()
print(opt)

# -------------------------
# Random seed
# -------------------------
opt.manualSeed = random.randint(1, 10000)
print("Random Seed: ", opt.manualSeed)
random.seed(opt.manualSeed)
torch.manual_seed(opt.manualSeed)

# -------------------------
# Dataset and dataloader
# -------------------------
dataset = LCASDataset(pointcloud_dir=opt.pointcloud_dir, label_dir=opt.label_dir, classification=False)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batchSize, shuffle=True, num_workers=int(opt.workers))

# Using same dataset for testing here (you can split later)
testdataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batchSize, shuffle=True, num_workers=int(opt.workers))

print("Dataset size:", len(dataset))
num_classes = dataset.num_seg_classes
print('Number of segmentation classes:', num_classes)

try:
    os.makedirs(opt.outf)
except OSError:
    pass

# -------------------------
# Model setup
# -------------------------
blue = lambda x: '\033[94m' + x + '\033[0m'

classifier = PointNetDenseCls(k=num_classes, feature_transform=opt.feature_transform)

if opt.model != '':
    classifier.load_state_dict(torch.load(opt.model))

optimizer = optim.Adam(classifier.parameters(), lr=0.001, betas=(0.9, 0.999))
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)
classifier.cuda()

num_batch = len(dataset) / opt.batchSize

# -------------------------
# Training loop
# -------------------------
for epoch in range(opt.nepoch):
    scheduler.step()
    for i, data in enumerate(dataloader, 0):
        points, target = data
        points = points.transpose(2, 1)
        points, target = points.cuda(), target.cuda()
        optimizer.zero_grad()
        classifier = classifier.train()
        pred, trans, trans_feat = classifier(points)
        pred = pred.view(-1, num_classes)
        target = target.view(-1, 1)[:, 0]
        loss = F.nll_loss(pred, target)
        if opt.feature_transform:
            loss += feature_transform_regularizer(trans_feat) * 0.001
        loss.backward()
        optimizer.step()

        pred_choice = pred.data.max(1)[1]
        correct = pred_choice.eq(target.data).cpu().sum()
        print('[%d: %d/%d] train loss: %f accuracy: %f' % (
            epoch, i, num_batch, loss.item(), correct.item()/float(opt.batchSize * dataset.npoints)))

        if i % 10 == 0:
            j, data = next(enumerate(testdataloader, 0))
            points, target = data
            points = points.transpose(2, 1)
            points, target = points.cuda(), target.cuda()
            classifier = classifier.eval()
            pred, _, _ = classifier(points)
            pred = pred.view(-1, num_classes)
            target = target.view(-1, 1)[:, 0]
            loss = F.nll_loss(pred, target)
            pred_choice = pred.data.max(1)[1]
            correct = pred_choice.eq(target.data).cpu().sum()
            print('[%d: %d/%d] %s loss: %f accuracy: %f' % (
                epoch, i, num_batch, blue('test'), loss.item(), correct.item()/float(opt.batchSize * dataset.npoints)))

    torch.save(classifier.state_dict(), '%s/lcas_seg_model_%d.pth' % (opt.outf, epoch))

# -------------------------
# Benchmark mIOU
# -------------------------
shape_ious = []
for i, data in tqdm(enumerate(testdataloader, 0)):
    points, target = data
    points = points.transpose(2, 1)
    points, target = points.cuda(), target.cuda()
    classifier = classifier.eval()
    pred, _, _ = classifier(points)
    pred_choice = pred.data.max(2)[1]

    pred_np = pred_choice.cpu().data.numpy()
    target_np = target.cpu().data.numpy()

    for shape_idx in range(target_np.shape[0]):
        parts = range(num_classes)
        part_ious = []
        for part in parts:
            I = np.sum(np.logical_and(pred_np[shape_idx] == part, target_np[shape_idx] == part))
            U = np.sum(np.logical_or(pred_np[shape_idx] == part, target_np[shape_idx] == part))
            iou = 1 if U == 0 else I / float(U)
            part_ious.append(iou)
        shape_ious.append(np.mean(part_ious))

print("mIOU for dataset: {}".format(np.mean(shape_ious)))
