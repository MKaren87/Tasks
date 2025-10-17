import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 50,
    'page': 1,
    'sparkline': False
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data)

top10_price = df.nlargest(10, 'current_price')[['name', 'current_price']]
print("🔝 Top 10 Cryptos by Price:")
print(top10_price)

gainers = df.nlargest(1, 'price_change_percentage_24h')[['name', 'price_change_percentage_24h']]
losers = df.nsmallest(1, 'price_change_percentage_24h')[['name', 'price_change_percentage_24h']]
print("\n📈 Biggest Gainer (24h):")
print(gainers)
print("\n📉 Biggest Loser (24h):")
print(losers)

avg_market_cap = df['market_cap'].mean()
print(f"\n💰 Average Market Cap of Top 50: ${avg_market_cap:,.2f}")

micro_coins = df[df['current_price'] < 1][['name', 'current_price']]
print("\n🪙 Micro-Coins (Price < $1):")
print(micro_coins)

top20_market_cap = df.nlargest(20, 'market_cap')
top20_market_cap.to_csv('top20_cryptos.csv', index=False)
print("\n✅ Saved top 20 cryptos by market cap to 'top20_cryptos.csv'")