import json
import threading
import logging
from item_monitor import ItemMonitor
from worker import Worker

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('main_log.txt'), logging.StreamHandler()])

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
