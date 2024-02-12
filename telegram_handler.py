from article import Article
import asyncio
import threading
import yaml
import telegram

ITEM_TEXT = "*Artículo*: {}\n" \
            "*Descripción*: {}\n" \
            "*Precio*: {} {}\n" \
            "[Ir al anuncio](https://es.wallapop.com/item/{})"

class TelegramHandler:
    def __init__(self):
        token, channel = self.get_config()
        self._channel = channel
        self._bot = telegram.Bot(token=token)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def get_config(self):
        config_file = 'config.yaml'
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            print(config)
            token = config['telegram_token']
            telegram_channel = config['telegram_channel']
        return token, telegram_channel

    def send_telegram_article(self, article):
        self._loop.run_until_complete(self.send_telegram_article_async(article))

    async def send_telegram_article_async(self, article):
        message = ITEM_TEXT.format(article.get_title(), article.get_description(),
                                   article.get_price(), article.get_currency(),
                                   article.get_url())
        await self._bot.send_message(self._channel, text=message, parse_mode="MARKDOWN")