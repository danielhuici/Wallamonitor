import json
import threading
import logging
from logging.handlers import RotatingFileHandler
from item_monitor import ItemMonitor
from worker import Worker

# Configure the console logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Configure the file logger
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
    logger = logging.getLogger(__name__)
    items = parse_items_to_monitor()

    for item in items:
        worker = Worker(item)
        thread = threading.Thread(target=worker.run)
        thread.start()
