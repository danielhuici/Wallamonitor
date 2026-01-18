import time
import requests
import logging
from datalayer.wallapop_article import WallapopArticle
from managers.telegram_manager import TelegramManager
import traceback

REQUEST_SLEEP_TIME = 15
REQUEST_RETRY_TIME = 3
ERROR_SLEEP_TIME = 30
NOTIFIED_ARTICLES_LIMIT = 300
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'

class Worker:
    def __init__(self, item_to_monitor):
        self.logger = logging.getLogger(__name__)
        self._item_monitoring = item_to_monitor
        self._notified_articles = self._request_articles()
        self.telegram_manager = TelegramManager()

    def _create_url(self):
        url = (
            f"http://api.wallapop.com/api/v3/search"
            f"?source=search_box"
            f"&keywords={self._item_monitoring._search_query}"
            f"&order_by=newest"
            f"&latitude={self._item_monitoring._latitude}"
            f"&longitude={self._item_monitoring._longitude}"
            f"&min_sale_price={self._item_monitoring._min_price}" 
            f"&max_sale_price={self._item_monitoring._max_price}" 
            f"&language=es_ES"
        )

        if self._item_monitoring._max_distance != "0":
            url += f"&distance_in_km={self._item_monitoring._max_distance}"

        if self._item_monitoring.get_condition() != "all":
            url += f"&condition={self._item_monitoring.get_condition()}"  # new, as_good_as_new, good, fair, has_given_it_all

        return url

    def _request_articles(self):
        url = self._create_url()

        while True:
            try:
                headers = {
                    'X-DeviceOS': '0',
                    'User-Agent': USER_AGENT
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as err:
                self.logger.error(f"Request Exception: {err}")
            time.sleep(REQUEST_RETRY_TIME)

        json_response = response.json()
        json_items = json_response['data']['section']['payload']['items']
        articles = self._parse_json_response(json_items)
        return articles

    def _parse_json_response(self, json_response):
        articles = []
        for json_article in json_response:
            articles.append(WallapopArticle.load_from_json(json_article))
        return articles

    def _has_words(self, text, word_list):
        return any(word in text for word in word_list)

    def _title_has_excluded_words(self, article_title):
        return self._has_words(article_title, self._item_monitoring.get_title_exclude())

    def _description_has_excluded_words(self, article_description):
        return self._has_words(article_description, self._item_monitoring.get_description_exclude())

    def _title_has_required_words(self, article_title):
        return not self._item_monitoring.get_title_must_include() \
                or self._has_words(article_title, self._item_monitoring.get_title_must_include())

    def _description_has_required_words(self, article_description):
        return not self._item_monitoring.get_description_must_include() \
                or self._has_words(article_description, self._item_monitoring.get_description_must_include())

    def _title_first_word_is_excluded(self, article_title):
        first_word = article_title.split()[0]
        for excluded_word in self._item_monitoring.get_title_first_word_exclude():
            if first_word == excluded_word:
                return True
        return False

    def _meets_item_conditions(self, article):
        if article in self._notified_articles:
            return False

        article_title = article.get_title().lower()
        article_description = article.get_description().lower()
        if (
            self._title_has_required_words(article_title) and
            self._description_has_required_words(article_description) and
            not self._title_has_excluded_words(article_title) and
            not self._description_has_excluded_words(article_description) and
            not self._title_first_word_is_excluded(article_title)
        ):
            return True
        else:
            self.logger.info(f"Excluded article: {article}")
            return False

    def work(self):
        exec_times = []
        
        while True:
            start_time = time.time()
            articles = self._request_articles()
            new_articles = 0
            for article in articles:
                if self._meets_item_conditions(article):
                    try:
                        self.telegram_manager.send_telegram_article(article)
                        new_articles += 1
                    except Exception as e:
                        self.logger.error(f"{self._item_monitoring.get_search_query()} worker crashed: {e}")
                self._notified_articles.insert(0, article)
                self._notified_articles = self._notified_articles[:NOTIFIED_ARTICLES_LIMIT]
            time.sleep(REQUEST_SLEEP_TIME)
            exec_times.append(time.time() - start_time)
            self.logger.info(
                f"Worker '{self._item_monitoring.get_search_query()}': {new_articles} new articles found. "
                f"Execution time stats - Last: {exec_times[-1]:.2f}s, Max: {max(exec_times):.2f}s, "
                f"Average: {sum(exec_times) / len(exec_times):.2f}s."
            )
    
    def run(self):
        while True:
            try:
                self.logger.info(f"Wallapop monitor worker started -  {self._item_monitoring.get_search_query()}")
                self.work()
            except Exception as e:
                self.logger.error(f"{''.join(traceback.format_exception(None, e, e.__traceback__))}")
                self.logger.error(f"{self._item_monitoring.get_search_query()} worker crashed. Restarting worker...")
                time.sleep(ERROR_SLEEP_TIME)
