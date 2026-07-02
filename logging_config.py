import logging
import os 

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    
    logging.basicConfig(
        filename="logs/trading.log",
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(message)s"
    )
    # return logger properly
    return logging.getLogger("trading_bot")