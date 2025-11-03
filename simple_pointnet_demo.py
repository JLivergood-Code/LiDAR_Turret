"""
simple_pointnet_demo_colored.py
Demonstrates a tiny PointNet-style classifier on synthetic 3D point clouds.
Shows colored visualizations of 'human-like' vs 'background' shapes.
"""

import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ---------- Synthetic data ----------
def gen_human_like(num_points=1024):
    theta = np.random.rand(num_points) * 2*np.pi
    z = np.random.rand(num_points) * 1.6          # 1.6 m tall
    r = 0.18 + 0.07*np.random.randn(num_points)   # cylinder radius
    x = r*np.cos(theta); y = r*np.sin(theta)
    pts = np.vstack([x, y, z]).T
    pts[z > 1.45] += 0.12*np.random.randn((z > 1.45).sum(), 3)  # head cluster
    pts += 0.02*np.random.randn(*pts.shape)
    return pts.astype(np.float32)

def gen_background(num_points=1024, spread=4.0):
    pts = (np.random.rand(num_points,3)-0.5)*spread
    pts[:,2] = np.random.exponential(scale=0.5,size=num_points) # ground-ish
    return pts.astype(np.float32)

def make_dataset(n_samples=400, points_per_sample=1024):
    X, y = [], []
    for i in range(n_samples):
        if i < n_samples//2:
            pts = gen_human_like(points_per_sample)
            trans = np.array([np.random.uniform(-1.5,1.5),
                              np.random.uniform(-1.5,1.5), 0.0])
            pts += trans
            label = 1
        else:
            pts = gen_background(points_per_sample)
            label = 0
        X.append(pts - pts.mean(0, keepdims=True))
        y.append(label)
    return np.stack(X), np.array(y)

# ---------- Dataset ----------
class PointCloudDataset(Dataset):
    def __init__(self,X,y): self.X=X; self.y=y
    def __len__(self): return len(self.X)
    def __getitem__(self,idx):
        return torch.from_numpy(self.X[idx]), torch.tensor(self.y[idx])

# ---------- Tiny PointNet ----------
class TinyPointNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(3,64), nn.ReLU(),
            nn.Linear(64,128), nn.ReLU(),
            nn.Linear(128,256), nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(256,128), nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128,2)
        )
    def forward(self,x):
        x = self.mlp(x)
        x = x.max(dim=1)[0]  # symmetric pooling
        return self.fc(x)

# ---------- Visualization helpers ----------
def show_examples(human_pts, bg_pts, preds=None):
    fig = plt.figure(figsize=(8,4))
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")
    ax1.scatter(human_pts[:,0], human_pts[:,1], human_pts[:,2],
                s=2, c="orange")
    ax2.scatter(bg_pts[:,0], bg_pts[:,1], bg_pts[:,2],
                s=2, c="skyblue")
    ax1.set_title(f"Human-like shape{' ✓' if preds and preds[0]==1 else ''}")
    ax2.set_title(f"Background{' ✓' if preds and preds[1]==0 else ''}")
    for a in (ax1,ax2):
        a.set_xlim(-2,2); a.set_ylim(-2,2); a.set_zlim(0,2)
        a.set_axis_off()
    plt.tight_layout(); plt.show()

# ---------- Main ----------
def main():
    X, y = make_dataset(300)
    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=0.2,stratify=y,random_state=0)
    train_loader = DataLoader(PointCloudDataset(Xtr,ytr),batch_size=16,shuffle=True)
    test_loader  = DataLoader(PointCloudDataset(Xte,yte),batch_size=32)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = TinyPointNet().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    for ep in range(1,16):
        model.train(); tot,acc=0,0
        for pts,lab in train_loader:
            pts,lab = pts.to(device), lab.to(device)
            opt.zero_grad(); out=model(pts)
            loss = F.cross_entropy(out,lab)
            loss.backward(); opt.step()
            tot+=loss.item()*pts.size(0)
            acc+=(out.argmax(1)==lab).sum().item()
        if ep%5==0: print(f"Epoch {ep}: loss={tot/len(Xtr):.3f}, acc={acc/len(Xtr):.3f}")

    # quick evaluation
    model.eval(); correct=0
    with torch.no_grad():
        for pts,lab in test_loader:
            pts,lab = pts.to(device),lab.to(device)
            out=model(pts)
            correct += (out.argmax(1)==lab).sum().item()
    print(f"Test accuracy ≈ {correct/len(Xte):.3f}")

    # show one human & one background example with predicted labels
    h_pts, b_pts = gen_human_like(), gen_background()
    with torch.no_grad():
        pred_h = model(torch.from_numpy(h_pts[None,:,:]).to(device)).argmax(1).item()
        pred_b = model(torch.from_numpy(b_pts[None,:,:]).to(device)).argmax(1).item()
    show_examples(h_pts,b_pts,preds=[pred_h,pred_b])

if __name__ == "__main__":
    main()
