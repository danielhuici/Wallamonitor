# Wallamonitor 
# 10/02/2021

import time
import requests
import json
import telegram
import argparse
from dotenv import load_dotenv
import os
load_dotenv()
import threading

from worker import Worker

def parse_json_file():
    f = open("args.json")
    return json.load(f)

    
def main():
    args = parse_json_file()

    for argument in args:
        p = threading.Thread(target=Worker.run, args=(argument, ))
        p.start()

main()