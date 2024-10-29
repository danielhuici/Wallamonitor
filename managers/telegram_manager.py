import asyncio
import yaml
import telegram
import re

ITEM_TEXT = "- *Artículo*: {}\n" \
            "- *Descripción*: {}\n" \
            "- *Localidad*: {}\n" \
            "- *Precio*: {} {}\n" \
            "- *Acepta envíos*: {}\n" \
            "[Ir al anuncio](https://es.wallapop.com/item/{})"


class TelegramManager:
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
            token = config['telegram_token']
            telegram_channel = config['telegram_channel']
        return token, telegram_channel

    
    def escape_markdown(self, text):
        special_chars = r'_[\]()~`>#\+\-=|{}.!]'
        escaped_text = re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)
        return escaped_text

    def send_telegram_article(self, article):
        self._loop.run_until_complete(self.send_telegram_article_async(article))

    async def send_telegram_article_async(self, article):
        message = ITEM_TEXT.format(article.get_title(), self.escape_markdown(article.get_description()),
                                   self.escape_markdown(article.get_location()), article.get_price(), 
                                   article.get_currency(), article.get_allows_shipping(),
                                   article.get_url())
        escaped_message = self.escape_markdown(message)
        await self._bot.send_message(self._channel, text=escaped_message, parse_mode="MarkdownV2")