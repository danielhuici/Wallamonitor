

class Article:
    def __init__(self, id, title, description, price, currency, url):
        self._id = id
        self._title = title
        self._description = description
        self._price = price
        self._currency = currency
        self._url = url

    @classmethod
    def load_from_json(cls, json_data):
        return cls(
            json_data['id'],
            json_data['title'],
            json_data['description'],
            json_data['price'],
            json_data['currency'],
            json_data['web_slug']
        )

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_price(self):
        return self._price

    def get_currency(self):
        return self._currency

    def get_url(self):
        return self._url

    def __eq__(self, article2):
        return self.get_id() == article2.get_id()