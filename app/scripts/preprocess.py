# scripts/preprocess.py
import argparse, os, pandas as pd

def main(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    df_urls  = pd.read_csv(os.path.join(input_dir, "urls.csv"))
    df_gazes = pd.read_csv(os.path.join(input_dir, "gazes.csv"))
    # → 여기서 실제 전처리 로직 작성
    df = pd.merge(df_urls, df_gazes, left_index=True, right_index=True, how="inner")
    df.to_csv(os.path.join(output_dir, "train_data.csv"), index=False)
    print(f"[preprocess] saved to {output_dir}/train_data.csv")

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir",  required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()
    main(args.input_dir, args.output_dir)
