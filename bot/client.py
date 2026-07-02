from binance.client import Client
from dotenv import load_dotenv
import os

#Load environment variables
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

def get_client():
    client = Client(
        API_KEY,
        API_SECRET,
        testnet=True
    )
    # Automatically sync with Binance server time
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    client.timestamp_offset = (
    client.futures_time()["serverTime"] - int(__import__("time").time() *1000)
    )
    return client

