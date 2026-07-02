from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException
from requests.exceptions import ConnectionError, Timeout
from bot.client import get_client
from logging_config import setup_logging

logger = setup_logging()

client = get_client()


def place_market_order(symbol, side, quantity):
    """
    Place a MARKET order.
    """
    logger.info(f"Request: MARKET order | symbol={symbol} side={side} quantity={quantity}")
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        logger.info(f"Response: Market order placed successfully | {order}")
        return order
    except BinanceAPIException as e:
        logger.error(f"Market order failed - API error: {e}")
        return None
    except (BinanceRequestException, ConnectionError, Timeout) as e:
        logger.error(f"Market order failed - network error: {e}")
        return None
    except Exception as e:
        logger.error(f"Market order failed - unexpected error: {e}")
        return None


def place_limit_order(symbol, side, quantity, price):
    """
    Place a LIMIT order.
    """
    logger.info(f"Request: LIMIT order | symbol={symbol} side={side} quantity={quantity} price={price}")
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=price
        )
        logger.info(f"Response: Limit order placed successfully | {order}")
        return order
    except BinanceAPIException as e:
        logger.error(f"Limit order failed - API error: {e}")
        return None
    except (BinanceRequestException, ConnectionError, Timeout) as e:
        logger.error(f"Limit order failed - network error: {e}")
        return None
    except Exception as e:
        logger.error(f"Limit order failed - unexpected error: {e}")
        return None


def place_stop_limit_order(symbol, side, quantity, stop_price, price):
    """
    Place a STOP-LIMIT order.
    Triggers a LIMIT order once the market price crosses stop_price.
    """
    logger.info(
        f"Request: STOP_LIMIT order | symbol={symbol} side={side} "
        f"quantity={quantity} stop_price={stop_price} price={price}"
    )
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_STOP,
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            timeInForce=TIME_IN_FORCE_GTC
        )
        logger.info(f"Response: Stop-Limit order placed successfully | {order}")
        # Normalize algo-order response to match regular order response shape
        order["orderId"] = order.get("algoId")
        order["status"] = order.get("algoStatus")
        order["type"] = order.get("orderType")
        order["executedQty"] = "0.0000"  # not filled until triggered
        return order
    except BinanceAPIException as e:
        logger.error(f"Stop-Limit order failed - API error: {e}")
        return None
    except (BinanceRequestException, ConnectionError, Timeout) as e:
        logger.error(f"Stop-Limit order failed - network error: {e}")
        return None
    except Exception as e:
        logger.error(f"Stop-Limit order failed - unexpected error: {e}")
        return None