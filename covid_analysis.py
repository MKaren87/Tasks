import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
from typing import List

def fetch_data(url: str, timeout: int = 15) -> list:
    """
    Fetch JSON data from URL, raise for bad status and save raw file.
    """
    print(f"Fetching URL: {url}")
    response = requests.get(url, timeout=timeout)
    print("HTTP status:", response.status_code)
    response.raise_for_status()
    data = response.json()
    out_raw = 'raw_covid_data.json'
    with open(out_raw, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved raw data -> {out_raw} (entries: {len(data) if isinstance(data, list) else 'unknown'})")
    return data

def normalize_data(data: list) -> pd.DataFrame:
    records = []
    for entry in data:
        country = entry.get('country') or entry.get('province') or entry.get('countryRegion') or entry.get('country_region') or "Unknown"
        timeline = entry.get('timeline') or {}
        cases = {}
        if isinstance(timeline, dict):
            cases = timeline.get('cases') or timeline.get('Cases') or {}
        if not cases:
            cases = entry.get('cases') or entry.get('Cases') or {}
        if not isinstance(cases, dict):
            continue
        for date_str, count in cases.items():
            try:
                cnt = int(count) if count is not None else 0
            except Exception:
                try:
                    cnt = int(float(count))
                except Exception:
                    cnt = 0
            records.append({'country': country, 'date': date_str, 'cases': cnt})
    if not records:
        return pd.DataFrame(columns=['country', 'date', 'cases'])
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=False)
    df = df.dropna(subset=['date'])
    df['date'] = df['date'].dt.normalize()  
    df.sort_values(['country', 'date'], inplace=True)
    return df

def pivot_cases(df: pd.DataFrame) -> pd.DataFrame:
    pivot_df = df.pivot_table(index='date', columns='country', values='cases', fill_value=0)
    pivot_df.to_csv('pivoted_covid.csv')
    return pivot_df

def plot_case_trends(pivot_df: pd.DataFrame, countries: List[str]):
    available = [c for c in countries if c in pivot_df.columns]
    if not available:
        if pivot_df.empty:
            print("No data available to plot.")
            return
        latest = pivot_df.iloc[-1].sort_values(ascending=False)
        available = latest.head(5).index.tolist()
        print("Requested countries not found. Using top available:", available)
    pivot_df[available].plot(figsize=(12, 6), title='COVID-19 Cases Trend (Last 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.legend(title='Country')
    plt.tight_layout()
    out1 = 'cases_trend.png'
    plt.savefig(out1)
    print(f"Saved trend plot: {out1}")
    plt.close()

def compute_daily_change(pivot_df: pd.DataFrame) -> pd.DataFrame:
    long_df = pivot_df.reset_index().melt(id_vars='date', var_name='country', value_name='cases')
    long_df = long_df.sort_values(['country', 'date'])
    long_df['daily_change'] = long_df.groupby('country')['cases'].diff().fillna(0)
    long_df['daily_change'] = pd.to_numeric(long_df['daily_change'], errors='coerce').fillna(0)
    return long_df

def plot_top5_daily_change(long_df: pd.DataFrame):
    if long_df.empty:
        print("No data to plot for top5.")
        return
    last_date = long_df['date'].max()
    last_week = long_df[long_df['date'] >= (last_date - pd.Timedelta(days=7))]
    if last_week.empty:
        print("No data for the last week.")
        return
    weekly_increase = last_week.groupby('country')['daily_change'].sum().sort_values(ascending=False)
    if weekly_increase.empty:
        print("No weekly increase data.")
        return
    top5 = weekly_increase.head(5).index.tolist()

    plt.figure(figsize=(12, 6))
    for country in top5:
        subset = last_week[last_week['country'] == country]
        if subset.empty:
            continue
        plt.plot(subset['date'], subset['daily_change'], label=country)

    plt.title('Top 5 Countries by Weekly Case Increase')
    plt.xlabel('Date')
    plt.ylabel('Daily Change in Cases')
    plt.legend()
    plt.tight_layout()
    out2 = 'daily_change_top5.png'
    plt.savefig(out2)
    print(f"Saved top5 plot: {out2}")
    plt.close()

def main():
    print("Starting covid_analysis.main()")
    url = "https://disease.sh/v3/covid-19/historical?lastdays=30"
    try:
        data = fetch_data(url)
    except Exception as e:
        print("Failed to fetch data:", repr(e))
        return
    df = normalize_data(data)
    print("Normalized rows:", len(df))
    if df.empty:
        print("No valid data after normalization.")
        return
    pivot_df = pivot_cases(df)
    print("Pivot table shape:", pivot_df.shape)

    selected_countries = ['USA', 'India', 'Brazil', 'Russia', 'France']
    plot_case_trends(pivot_df, selected_countries)

    long_df = compute_daily_change(pivot_df)
    plot_top5_daily_change(long_df)

if __name__ == "__main__":
    main()