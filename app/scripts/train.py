# scripts/train.py
import argparse, os
import pandas as pd
import torch, torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self, in_dim, hid=8, out_dim=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hid), nn.ReLU(),
            nn.Linear(hid, out_dim), nn.Sigmoid()
        )
    def forward(self,x): return self.net(x)

def main(data_dir: str, output: str):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    df = pd.read_csv(os.path.join(data_dir, "train_data.csv"))
    X = torch.tensor(df.drop("status",1).values, dtype=torch.float32)
    y = torch.tensor((df.status=="alert").astype(int).values)[:,None].float()

    m = SimpleModel(X.shape[1])
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()
    for ep in range(10):
        opt.zero_grad()
        loss = loss_fn(m(X), y)
        loss.backward(); opt.step()
        print(f"[train] ep{ep+1}/10 loss={loss.item():.4f}")
    torch.save(m.state_dict(), output)
    print(f"[train] saved model to {output}")

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", required=True)
    p.add_argument("--output",   required=True)
    args = p.parse_args()
    main(args.data_dir, args.output)
