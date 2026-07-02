VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["LIMIT", "MARKET","STOP_LIMIT"]

def validate_side(side):
    side= side.upper()

    if side not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL")
    
    return side

def validate_order_type(order_type):
    order_type=order_type.upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError("Order type must be MARKET OR LIMIT")
   
    return order_type

def validate_quantity(quantity):
    try:
        quantity = float(quantity)
    except (TypeError , ValueError):
        raise ValueError("Quantity must be a valid number")
    if quantity <=0:
        raise ValueError("Quantity must be greater than 0")
    return quantity

def validate_price(price):
    try:
        price = float(price)
    except (TypeError ,ValueError):
        raise ValueError("Price must be a valid number")
    if price <=0:
        raise ValueError("Price must be greater than 0")
    return price

def validate_stop_price(stop_price):
    try:
        stop_price = float(stop_price)
    except (TypeError, ValueError):
        raise ValueError("Stop price must be a valid number")
    if stop_price <=0:
        raise ValueError("Stop price must be greater than 0")
    return stop_price

                        
