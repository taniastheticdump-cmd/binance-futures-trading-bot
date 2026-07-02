from bot.orders import place_market_order, place_limit_order, place_stop_limit_order
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price
)


def get_valid_input(prompt, validator):
    """Keep asking until the user gives valid input instead of crashing."""
    while True:
        value = input(prompt)
        try:
            return validator(value)
        except ValueError as e:
            print(f"⚠️  Invalid input: {e}. Please try again.")


def main():
    print("=== Binance Futures Testnet Trading Bot ===")

    symbol = input("Enter symbol (eg. BTCUSDT): ").upper()
    side = get_valid_input("Enter side (BUY/SELL): ", validate_side)
    order_type = get_valid_input(
        "Enter order type (MARKET/LIMIT/STOP_LIMIT): ", validate_order_type
    )
    quantity = get_valid_input("Enter Quantity: ", validate_quantity)

    price = None
    stop_price = None

    if order_type == "LIMIT":
        price = get_valid_input("Enter Limit Price: ", validate_price)
    elif order_type == "STOP_LIMIT":
        stop_price = get_valid_input("Enter Stop (trigger) Price: ", validate_stop_price)
        price = get_valid_input("Enter Limit Price (after trigger): ", validate_price)

    print("\n--- Order Request Summary ---")
    print(f"Symbol:   {symbol}")
    print(f"Side:     {side}")
    print(f"Type:     {order_type}")
    print(f"Quantity: {quantity}")
    if stop_price is not None:
        print(f"Stop Price: {stop_price}")
    if price is not None:
        print(f"Price:    {price}")
    print("------------------------------")

    try:
        if order_type == "MARKET":
            order = place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            order = place_limit_order(symbol, side, quantity, price)
        else:  # STOP_LIMIT
            order = place_stop_limit_order(symbol, side, quantity, stop_price, price)
    except Exception as e:
        print(f"\n❌ Order Placement Failed (unexpected error): {e}")
        return

    if order:
        print("\n--- Order Response ---")
        print(f"Order ID:     {order.get('orderId')}")
        print(f"Symbol:       {order.get('symbol')}")
        print(f"Side:         {order.get('side')}")
        print(f"Type:         {order.get('type')}")
        print(f"Status:       {order.get('status')}")
        print(f"Executed Qty: {order.get('executedQty')}")
        if order.get('avgPrice') is not None:
            print(f"Avg Price:    {order.get('avgPrice')}")
        print("\n✅ Order Placed Successfully!")
    else:
        print("\n❌ Order Placement Failed! (see logs/trading.log for details)")


if __name__ == "__main__":
    main()