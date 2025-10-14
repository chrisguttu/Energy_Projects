
# src/data_loader.py
import pandas as pd
import yfinance as yf
import os
import yaml

def load_config():
    with open("config/paths.yml", "r") as f:
        return yaml.safe_load(f)

def download_yfinance(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Download market data from Yahoo Finance.
    """
    df = yf.download(symbol, start=start, end=end)
    df.reset_index(inplace=True)
    return df

def save_processed(data: pd.DataFrame, name: str):
    """Save processed data to /data/processed."""
    config = load_config()
    path = os.path.join(config['data']['processed'], f"{name}.csv")
    data.to_csv(path, index=False)
    print(f"Processed data saved to {path}")