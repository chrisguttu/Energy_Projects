
import requests
import pandas as pd

# Define which commodities are monthly-only
MONTHLY_ONLY = {"COPPER", "ALUMINUM", "WHEAT", "CORN", "COTTON", "COFFEE", "SUGAR", "ALL_COMMODITIES"}

def get_commodity(commodity: str, api_key: str) -> pd.DataFrame:
    """
    Download a single Alpha Vantage commodity as a pandas DataFrame.
    Handles daily vs monthly intervals automatically.
    """
    params = {"function": commodity, "apikey": api_key}
    
    if commodity in MONTHLY_ONLY:
        params["interval"] = "monthly"  # required for these commodities

    url = "https://www.alphavantage.co/query"
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    
    if "data" not in data:
        raise ValueError(f"No data returned for {commodity}. Response: {data}")

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors='coerce') # handle non-numeric values as alpha vantage use "." for missing data
    df = df.set_index("date").sort_index()
    df.rename(columns={"value": commodity}, inplace=True)
    return df



def get_multiple_commodities(commodities: list, api_key: str) -> pd.DataFrame:
    """
    Download multiple commodities and combine into one DataFrame.
    Each column corresponds to a commodity name.
    """
    all_data = []
    for c in commodities:
        try:
            df = get_commodity(c, api_key)
            all_data.append(df)
            print(f"✅ {c} downloaded ({len(df)} records)")
        except Exception as e:
            print(f"⚠️ Skipped {c}: {e}")

    # Combine all on date index
    combined = pd.concat(all_data, axis=1)
    return combined






    