import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, min, max

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder.appName("CryptoStatsAndVisualization").getOrCreate()

cryptos = ["bitcoin", "ethereum", "tether"]
prices_dict = {}

for coin in cryptos:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": "180"}
    response = requests.get(url, params=params)
    data = response.json()

    prices = [{"timestamp": ts, "price": p} for ts, p in data["prices"]]

    df = spark.createDataFrame(prices)

    stats = df.select(
        avg(col("price")).alias("avg_price"),
        min(col("price")).alias("min_price"),
        max(col("price")).alias("max_price")
    )
    print(f"\n{coin.upper()} статистика за последние полгода:")
    stats.show()

    df = df.withColumn("date", (col("timestamp")/1000).cast("timestamp"))
    daily = df.groupBy(col("date").cast("date")).agg(avg("price").alias("avg_price"))

    prices_dict[coin] = daily.toPandas().sort_values("date")

plt.figure(figsize=(12, 6))
for coin, df in prices_dict.items():
    plt.plot(df["date"], df["avg_price"], label=coin.capitalize())

plt.title("Курс криптовалют (Bitcoin, Ethereum, Tether) за последние полгода")
plt.xlabel("Дата")
plt.ylabel("Средняя цена (USD)")
plt.legend()
plt.grid(True)
plt.savefig('crypto_chart.png')

spark.stop()
