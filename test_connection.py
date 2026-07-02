from bot.client import get_client

try:
    client = get_client()

    account = client.futures_account()

    print("Connected to Binance Futures Testnet!")
    print("Account Assets:")
    print(account["assets"])

except Exception as e:
    print("Connection Failed")
    print(e)