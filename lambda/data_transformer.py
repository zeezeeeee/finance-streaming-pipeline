import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--target", "/tmp"])
sys.path.append('/tmp')

import requests
import json
import boto3
import time
import os

kinesis = boto3.client('kinesis', 'us-east-2')

STREAM_NAME = "Datacollector-stream"
API_KEY = os.environ.get("API_KEY")

TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "JPM", "V", "WMT",
    "JNJ", "PG", "MA", "HD", "BAC", "XOM", "CVX", "ABBV", "MRK", "LLY",
    "PEP", "KO", "AVGO", "COST", "TMO", "MCD", "ACN", "DHR", "NEE", "UNH",
    "NFLX", "ADBE", "CRM", "TXN", "PM", "LIN", "QCOM", "ORCL", "AMD", "INTC",
    "IBM", "GE", "CAT", "BA", "RTX", "HON", "UPS", "SBUX", "GS", "MS",
    "SCHW", "BLK", "AXP", "SPGI", "CB", "PLD", "AMT", "DUK", "SO", "D",
    "MMM", "CVS", "GILD", "VRTX", "REGN", "AMGN"
]

def lambda_handler(event, context):
    count = 0
    for ticker in TICKERS:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})

        for date_str, values in time_series.items():
            open_price = float(values["1. open"])
            close_price = float(values["4. close"])
            difference = round(open_price - close_price, 2)

            record = {
                "name": ticker,
                "ts": date_str,
                "open_stock": open_price,
                "close_stock": close_price,
                "difference": difference
            }

            payload = json.dumps(record) + "\n"
            print(payload)

            kinesis.put_record(
                StreamName=STREAM_NAME,
                Data=payload,
                PartitionKey=ticker
            )

            count += 1
            time.sleep(0.05)

    print(count)
    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully streamed to Kinesis!')
    }
