# Binance Futures Testnet Trading Bot

A Python CLI trading bot that places **MARKET**, **LIMIT**, and **STOP_LIMIT** orders on Binance Futures Testnet (USDT-M), with input validation, structured logging, and error handling.

## Project Structure

```
trading_bot/
├── main.py                # CLI entry point
├── bot/
│   ├── client.py           # Binance client wrapper (testnet connection)
│   ├── orders.py            # Order placement logic (MARKET / LIMIT / STOP_LIMIT)
│   └── validators.py        # CLI input validation
├── logging_config.py       # Logging setup (writes to logs/trading.log)
├── logs/
│   └── trading.log          # Log of all order requests, responses & errors
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

- Place **MARKET**, **LIMIT**, and **STOP_LIMIT** orders (bonus: third order type)
- Support both **BUY** and **SELL** sides
- CLI input validation with a **retry loop** — invalid input reprompts the user with a clear message instead of crashing (bonus: enhanced CLI UX)
- Clean order **request summary** printed before submission, and full **response details** (Order ID, status, executed quantity, avg price) printed after
- Structured code: API/client layer (`bot/client.py`, `bot/orders.py`) separated from the CLI layer (`main.py`)
- Logging of every request, response, and error to `logs/trading.log`
- Exception handling split into three categories: invalid input, Binance API errors, and network errors

## Setup

### 1. Get Binance Futures Testnet API credentials
1. Go to https://testnet.binancefuture.com
2. Register / log in and activate a Futures Testnet account.
3. Generate an API Key and Secret from the testnet dashboard.

### 2. Clone this repo and install dependencies
```bash
git clone <your-repo-url>
cd trading_bot
python -m venv venv
venv\Scripts\activate      # On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure your API credentials
Create a `.env` file in the project root:
```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

**Never commit your real `.env` file** — it's excluded via `.gitignore`.

### 4. (Optional) Test your connection
```bash
python test_connection.py
```
This confirms your API keys work and prints your futures testnet account assets.

## How to Run

```bash
python main.py
```

You'll be prompted for:
- **Symbol** (e.g. `BTCUSDT`)
- **Side** (`BUY` or `SELL`)
- **Order type** (`MARKET`, `LIMIT`, or `STOP_LIMIT`)
- **Quantity**
- **Price** — only asked for `LIMIT`
- **Stop Price** and **Limit Price** — only asked for `STOP_LIMIT`

If you enter something invalid (e.g. `side = maybe`), the bot reprompts you with a clear error message instead of exiting.

### Example: Market order
```
=== Binance Futures Testnet Trading Bot ===
Enter symbol (eg. BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter order type (MARKET/LIMIT/STOP_LIMIT): MARKET
Enter Quantity: 0.001

--- Order Request Summary ---
Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.001
------------------------------

--- Order Response ---
Order ID:     18405588285
Symbol:       BTCUSDT
Side:         BUY
Type:         MARKET
Status:       NEW
Executed Qty: 0.0000

✅ Order Placed Successfully!
```

### Example: Limit order
```
=== Binance Futures Testnet Trading Bot ===
Enter symbol (eg. BTCUSDT): BTCUSDT
Enter side (BUY/SELL): SELL
Enter order type (MARKET/LIMIT/STOP_LIMIT): LIMIT
Enter Quantity: 0.01
Enter Limit Price: 60000

--- Order Request Summary ---
Symbol:   BTCUSDT
Side:     SELL
Type:     LIMIT
Quantity: 0.01
Price:    60000.0
------------------------------

--- Order Response ---
Order ID:     18427104642
Symbol:       BTCUSDT
Side:         SELL
Type:         LIMIT
Status:       NEW
Executed Qty: 0.0000

✅ Order Placed Successfully!
```

### Example: Stop-Limit order (bonus)
```
=== Binance Futures Testnet Trading Bot ===
Enter symbol (eg. BTCUSDT): BTCUSDT
Enter side (BUY/SELL): SELL
Enter order type (MARKET/LIMIT/STOP_LIMIT): STOP_LIMIT
Enter Quantity: 0.01
Enter Stop (trigger) Price: 60000
Enter Limit Price (after trigger): 80000

--- Order Request Summary ---
Symbol:   BTCUSDT
Side:     SELL
Type:     STOP_LIMIT
Quantity: 0.01
Stop Price: 60000.0
Price:    80000.0
------------------------------

--- Order Response ---
Order ID:     1000000122006664
Symbol:       BTCUSDT
Side:         SELL
Type:         STOP
Status:       NEW
Executed Qty: 0.0000

✅ Order Placed Successfully!
```
This places a conditional order that triggers a LIMIT SELL at 80000 once the market price crosses 60000.

## Logging

All order requests, responses, and errors are logged to `logs/trading.log` with timestamps, e.g.:
```
2026-07-02 12:35:31,178 | INFO | Request: LIMIT order | symbol=BTCUSDT side=SELL quantity=0.01 price=5000.0
2026-07-02 12:35:31,642 | ERROR | Limit order failed - API error: APIError(code=-4024): Limit price can't be lower than 57207.63.
```
API errors and network errors are logged separately from successful requests, so failures are easy to find without digging through info-level noise.

## Error Handling

- **Invalid input** (bad symbol, invalid side/order type, non-numeric or non-positive quantity/price/stop price) is caught before any API call is made. The CLI reprompts the user with a clear message instead of crashing.
- **API errors** raised by Binance (e.g. invalid price outside allowed band, insufficient balance, bad symbol) are caught via `BinanceAPIException`, logged with the exact reason, and result in a clean failure message.
- **Network errors** (timeouts, connection failures) are caught separately via `BinanceRequestException` / `requests.exceptions` and logged distinctly from API errors.

## Assumptions

- STOP_LIMIT orders use Binance's futures conditional order type (`STOP`), which returns an `algoId`/`algoStatus` response shape rather than the standard `orderId`/`status` shape used by MARKET/LIMIT orders. The response is normalized in code so all three order types print consistently.
- All LIMIT and STOP_LIMIT orders use `timeInForce=GTC`.
- The bot assumes a Futures Testnet USDT-M account with hedging mode off (default one-way position mode).
- Quantity/price precision is not auto-rounded to the symbol's exchange filters — the user is expected to enter values valid for the chosen symbol (e.g. correct decimal precision for BTCUSDT).
- Binance enforces a maximum price deviation band for LIMIT orders relative to the current market price; orders priced too far away will be rejected by the API (this is expected behavior, not a bug — see Error Handling above).