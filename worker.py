import time
import requests
import json
import telegram
import argparse
from dotenv import load_dotenv
import os
load_dotenv()
import threading


TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID") 
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SLEEP_TIME=30

class Worker:

    def request(self, product_name, n_articles, latitude='40.4165', longitude='-3.70256', distance='0', condition='all', min_price=0, max_price=10000000):
        url = (f"http://api.wallapop.com/api/v3/general/search?keywords={product_name}"
                    f"&order_by=newest&latitude={latitude}"
                    f"&longitude={longitude}"
                    f"&distance={distance}"
                    f"&min_sale_price={min_price}" 
                    f"&max_sale_price={max_price}" 
                    f"&filters_source=quick_filters&language=es_ES")
                    
        if condition != "all":
            url = url + f"&condition={condition}" # new, as_good_as_new, good, fair, has_given_it_all

        while True:
            response = requests.get(url)
            try:
                if response.status_code == 200:
                    break
                else:
                    print(f"\'{product_name}\' -> Wallapop returned status {response.get_status_code() }. Illegal parameters or Wallapop service is down. Retrying...")
            except Exception as e:
                print("Exception: "+e)
                time.sleep(3)

        json_data=response.json()
        return json_data['search_objects']

    def first_run(self, args):
        list = []
        articles = self.request(args['product_name'], 0, args['latitude'], args['longitude'], args['condition'], args['min_price'], args['max_price'])
        for article in articles: 
            list.insert(0, article['id'])
        
        return list

    def work(self, args, list):
        exec_times = []
        bot = telegram.Bot(token = TELEGRAM_TOKEN)
        
        while True:
            start_time = time.time()
            articles = self.request(args['product_name'], 0, args['latitude'], args['longitude'], args['distance'], args['condition'], args['min_price'], args['max_price'])
            for article in articles:
                if not article['id'] in list:
                    try:
                        if not self.has_excluded_words(article['title'].lower(), article['description'].lower(), args['exclude']) and not self.is_title_key_word_excluded(article['title'].lower(), args['title_keyword_exclude']):
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
                            time.sleep(1) # Avoid Telegram flood restriction
                        list.insert(0, article['id'])   
                    except Exception as e:
                        print("---------- EXCEPTION -----------")
                        f = open("error_log.txt", "a")
                        f.write(f"{args['product_name']} worker crashed. {e}")
                        f.write(f"{args['product_name']}: Trying to parse {article['id']}: {article['title']} .")
                        f.close()


            time.sleep(5)
            exec_times.append(time.time() - start_time)
            print(f"\'{args['product_name']}\' node-> last: {exec_times[-1]} max: {self.get_max_time(exec_times)} avg: {self.get_average_time(exec_times)}")

    def has_excluded_words(self, title, description, excluded_words):
        for word in excluded_words:
            print("EXCLUDER: Checking '" + word + "' for title: '" + title)
            if word in title or word in description:
                print("EXCLUDE!")
                return True
        return False
    
    def is_title_key_word_excluded(self, title, excluded_words):
        for word in excluded_words:
            print("Checking '" + word + "' for title: '" + title)
            if word in title.split()[0]:
                return True
        return False

    def get_average_time(self, exec_times):
        sum = 0
        for i in exec_times:
            sum = sum + i
        
        return sum / len(exec_times)

    def get_max_time(self, exec_times):
        largest = 0
        for i in exec_times:
            if i > largest:
                largest = i
        return largest
        

    def run(args):
        worker = Worker()
        list = worker.first_run(args)
        while True:
            #try:
            print(f"Wallapop monitor worker started. Checking for new items containing: \'{args['product_name']}\' with given parameters periodically")
            worker.work(args, list)
            #except Exception as e:
            #    print(f"Exception: {e}")
            #    print(f"{args['product_name']} worker crashed. Restarting worker...")
            #    time.sleep(10)

