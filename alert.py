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

TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID") 
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SLEEP_TIME=120

def request(product_name, n_articles, latitude, longitude, condition, min_price, max_price):
    url = (f"https://api.wallapop.com/api/v3/general/search?keywords={product_name}"
                f"&order_by=newest&latitude={latitude}"
                f"&longitude={longitude}"
                f"&min_sale_price={min_price}" 
                f"&max_sale_price={max_price}" 
                f"&filters_source=quick_filters&language=es_ES")
                
    if condition != "all":
        url = url + f"&condition={condition}" # new, as_good_as_new, good, fair, has_given_it_all

    response = requests.get(url)
    while response.status_code != 200:
        print(f"Wallapop returned status {response.status_code}. Illegal parameters or Wallapop service is down. Sleep...")
        time.sleep(SLEEP_TIME)
        response = requests.get(url)

    json_data=json.loads(response.text)
    return json_data['search_objects']

 
# We'll insert ignore current items in Wallapop,
# Only alert new articles published from NOW!
def first_run():
    list = []
    articles = request(args.name, 0, args.latitude, args.longitude, args.condition, args.min_price, args.max_price)
    for article in articles: 
        list.insert(0, article['id'])

    return list
    
def main(args):
    bot = telegram.Bot(token = TELEGRAM_TOKEN)
    list = first_run()

    while True:
        articles = request(args.name, 0, args.latitude, args.longitude, args.condition, args.min_price, args.max_price)
        for article in articles:
            if not article['id'] in list:
                bot.send_photo(TELEGRAM_CHANNEL_ID, article['images'][0]['original'])
                try:
                    bot.send_message(TELEGRAM_CHANNEL_ID, f"*Artículo*: {article['title']}\n"
                                                        f"*Descripción*: {article['description']}\n"
                                                        f"*Precio*: {article['price']} {article['currency']}\n"
                                                        f"[Ir al anuncio](https://es.wallapop.com/item/{article['web_slug']})"
                                                    , "MARKDOWN")
                except:
                    bot.send_message(TELEGRAM_CHANNEL_ID, f"*Artículo*: {article['title']}\n"
                                                        f"*Descripción*: Descripción inválida\n"
                                                        f"*Precio*: {article['price']} {article['currency']}\n"
                                                        f"[Ir al anuncio](https://es.wallapop.com/item/{article['web_slug']})"
                                                    , "MARKDOWN")
                list.insert(0, article['id'])
                time.sleep(5) # Avoid Telegram flood restrictions
        time.sleep(SLEEP_TIME) 
    
def argument_handler():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--name', dest='name', type=str, required=True, help='Article name')
    parser.add_argument('--latitude', dest='latitude', type=str, default='40.4165', help='Latitude')
    parser.add_argument('--longitude', dest='longitude', type=str, default='-3.70256', help='Longitude')
    parser.add_argument('--condition', dest='condition', type=str, default='all', help='Item condition: all, new, as_good_as_new, good, fair, has_given_it_all')
    parser.add_argument('--min', dest='min_price', type=str, default=0, help='Min price')
    parser.add_argument('--max', dest='max_price', type=str, default=10000000, help='Max price')

    args = parser.parse_args()
    print(f"Wallapop monitor running. Checking for new items containing: \'{args.name}\' with given parameters periodically")
    return args

args = argument_handler()
main(args)