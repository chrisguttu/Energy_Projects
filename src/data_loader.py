import requests
import pandas as pd
import yaml
from pathlib import Path

# --- Resolve config path ---
# Find project root by going two levels up from this file (src → project_root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yml"

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

# --- Load config ---
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

API_KEY = config.get("api_key")
if not API_KEY:
    raise ValueError("API key is missing in setting.yml")

MONTHLY_ONLY = set(config.get("commodities", {}).get("monthly_only", []))
if not MONTHLY_ONLY:
    raise ValueError("List of monthly only commoditites are missing in settings.yml")


# --- Functions ---
def get_commodity(commodity: str) -> pd.DataFrame:
    params = {"function": commodity, "apikey": API_KEY}
    if commodity in MONTHLY_ONLY:
        params["interval"] = "monthly"

    url = "https://www.alphavantage.co/query"
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    if "data" not in data:
        raise ValueError(f"No data returned for {commodity}. Response: {data}")

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.set_index("date").sort_index()
    df.rename(columns={"value": commodity}, inplace=True)
    return df


def get_multiple_commodities(commodities: list) -> pd.DataFrame:
    all_data = []
    for c in commodities:
        try:
            df = get_commodity(c)
            all_data.append(df)
            print(f"✅ {c} downloaded ({len(df)} records)")
        except Exception as e:
            print(f"⚠️ Skipped {c}: {e}")

    combined = pd.concat(all_data, axis=1)
    return combined