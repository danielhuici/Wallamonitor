import time
import requests
import logging
from article import Article
from telegram_handler import TelegramHandler
import traceback
import asyncio

REQUEST_SLEEP_TIME = 5
REQUEST_RETRY_TIME = 3
ERROR_SLEEP_TIME = 10

worker_logger = logging.getLogger(__name__)
worker_logger.setLevel(logging.INFO)  # Set the level as needed
worker_logger.addHandler(logging.StreamHandler())

class Worker:
    def __init__(self, item_to_monitor):
        self.logger = logging.getLogger(__name__)
        self._item_monitoring = item_to_monitor
        self._notified_articles = self._request_articles()
        self._telegram_handler = TelegramHandler()

    def _request_articles(self):
        url = (
            f"http://api.wallapop.com/api/v3/general/search?keywords={self._item_monitoring.get_search_query()}"
            f"&order_by=newest&latitude={self._item_monitoring.get_latitude()}"
            f"&longitude={self._item_monitoring.get_longitude()}"
            f"&distance={self._item_monitoring.get_max_distance()}"
            f"&min_sale_price={self._item_monitoring.get_min_price()}" 
            f"&max_sale_price={self._item_monitoring.get_max_price()}" 
            f"&filters_source=quick_filters&language=es_ES"
        )

        if self._item_monitoring.get_condition() != "all":
            url += f"&condition={self._item_monitoring.get_condition()}"  # new, as_good_as_new, good, fair, has_given_it_all

        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as err:
                self.logger.error(f"Request Exception: {err}")
            time.sleep(REQUEST_RETRY_TIME)

        json_response = response.json()
        articles = self._parse_json_response(json_response['search_objects'])
        return articles

    def _parse_json_response(self, json_response):
        articles = []
        for json_article in json_response:
            articles.append(Article.load_from_json(json_article))
        return articles

    def _has_words(self, text, word_list):
        return any(word in text for word in word_list)

    def _title_has_excluded_words(self, article):
        return self._has_words(article.get_title(), 
                               self._item_monitoring.get_title_exclude())

    def _description_has_excluded_words(self, article):
        return self._has_words(article.get_description(), 
                               self._item_monitoring.get_description_exclude())

    def _title_has_required_words(self, article):
        return not self._item_monitoring.get_title_must_include() \
                or self._has_words(article.get_title(),
                                   self._item_monitoring.get_title_must_include())

    def _description_has_required_words(self, article):
        return not self._item_monitoring.get_description_must_include() \
                or self._has_words(article.get_description(), 
                                   self._item_monitoring.get_description_must_include())

    def _meets_item_conditions(self, article):
        return (
            self._title_has_required_words(article) and
            self._description_has_required_words(article) and
            not self._title_has_excluded_words(article) and
            not self._description_has_excluded_words(article) and
            article not in self._notified_articles
        )

    def work(self):
        exec_times = []
        
        while True:
            start_time = time.time()
            articles = self._request_articles()
            for article in articles[0:1]:
                if self._meets_item_conditions(article):
                    try:
                        self._telegram_handler.send_telegram_article(article)
                        self._notified_articles.insert(0, article)
                    except Exception as e:
                        self.logger.error(f"{self._item_monitoring.get_search_query()} worker crashed: {e}")
            time.sleep(REQUEST_SLEEP_TIME)
            exec_times.append(time.time() - start_time)
            self.logger.info(f"\'{self._item_monitoring.get_search_query()}\' node-> last: {exec_times[-1]}"
                             f" max: {max(exec_times)} avg: {sum(exec_times) / len(exec_times)}")
    
    def run(self):
        while True:
            try:
                self.logger.info(f"Wallapop monitor worker started. Checking for "
                                 f"new items containing '{self._item_monitoring.get_search_query()}' "
                                 f"with given parameters periodically")
                self.work()
            except Exception as e:
                self.logger.error(f"{''.join(traceback.format_exception(None, e, e.__traceback__))}")
                self.logger.error(f"{self._item_monitoring.get_search_query()} worker crashed. Restarting worker...")
                time.sleep(ERROR_SLEEP_TIME)
