# scripts/convert_to_onnx.py
import argparse, os, torch
from train import SimpleModel

def main(input_path: str, output: str):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    m = SimpleModel(in_dim=4)          # input_dim은 전처리 컬럼 개수로 조정
    m.load_state_dict(torch.load(input_path))
    m.eval()
    dummy = torch.randn(1, m.net[0].in_features)
    torch.onnx.export(
        m, dummy, output,
        input_names=["input"], output_names=["output"],
        dynamic_axes={"input":{0:"batch"}, "output":{0:"batch"}}
    )
    print(f"[onnx] exported to {output}")

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input",  required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    main(args.input, args.output)
