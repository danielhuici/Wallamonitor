import json
import logging
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor

from datalayer.item_monitor import ItemMonitor
from worker import Worker
from managers.telegram_manager import TelegramManager

def configure_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    file_handler = RotatingFileHandler('monitor.log', maxBytes=10e6)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configure the root logger with both handlers
    logging.basicConfig(level=logging.NOTSET,
                        handlers=[console_handler, file_handler])

def parse_items_to_monitor():
    with open("args.json") as f:
        args = json.load(f)
        items = [ItemMonitor.load_from_json(item) for item in args]
    return items

if __name__ == "__main__":
    configure_logger()
    items = parse_items_to_monitor()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for item in items:
            worker = Worker(item)
            executor.submit(worker.run)

