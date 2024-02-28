

class Article:
    def __init__(self, id, title, description, price, currency, location, allows_shipping, url):
        self._id = id
        self._title = title
        self._description = description
        self._price = price
        self._currency = currency
        self._location = location
        self._allows_shipping = allows_shipping
        self._url = url

    @classmethod
    def load_from_json(cls, json_data):
        return cls(
            json_data['id'],
            json_data['title'],
            json_data['description'],
            json_data['price'],
            json_data['currency'],
            json_data['location']['city'],
            json_data['shipping']['user_allows_shipping'],
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

    def get_location(self):
        return self._location

    def get_allows_shipping(self):
        return self._allows_shipping

    def get_url(self):
        return self._url

    def __eq__(self, article2):
        return self.get_id() == article2.get_id()

    def __str__(self):
        return f"Article(id={self._id}, title='{self._title}', description='{self._description}', " \
               f"price={self._price} {self._currency}, url='{self._url}')"