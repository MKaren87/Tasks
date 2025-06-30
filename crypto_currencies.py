try:
    import argparse
except ImportError:
    print("Module 'argparse' is not installed. Install it with: pip install argparse")
    exit(1)

try:
    import requests
except ImportError:
    print("Module 'requests' is not installed. Install it with: pip install requests")
    exit(1)

try:
    from tabulate import tabulate
except ImportError:
    print("Module 'tabulate' is not installed. Install it with: pip install tabulate")
    exit(1)

import time

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'price_change_percentage': '24h'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  
    return response.json()

def display_data(data, name_filter=None, min_price=None):
    table = []
    for coin in data:
        name = coin['name']
        symbol = coin['symbol'].upper()
        price = coin['current_price']
        market_cap = coin['market_cap']
        volume = coin['total_volume']
        price_change = coin.get('price_change_percentage_24h', 0)

        if name_filter and name_filter.lower() not in name.lower():
            continue
        if min_price and price < min_price:
            continue

        table.append([
            name,
            symbol,
            f"{price:.2f}",
            f"{market_cap:,}",
            f"{volume:,}",
            f"{price_change:.2f}"
        ])
    print(tabulate(table, headers=["Name", "Symbol", "Price ($)", "Market Cap ($)", "Volume ($)", "24h Change (%)"]))

def parse_arguments():
    parser = argparse.ArgumentParser(description="Cryptocurrency Stats Viewer")
    parser.add_argument('--name', type=str, help='Filter by coin name (partial match)')
    parser.add_argument('--min_price', type=float, help='Show coins with price greater than this value')
    return parser.parse_args()

def main():
    args = parse_arguments()
    while True:
        try:
            data = fetch_crypto_data()
            display_data(data, name_filter=args.name, min_price=args.min_price)
        except Exception as e:
            print(f"Error fetching data: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()

