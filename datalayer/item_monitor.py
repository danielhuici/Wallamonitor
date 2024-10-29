
class ItemMonitor:
    def __init__(self, search_query, latitude, longitude, max_distance,
                 condition, min_price, max_price, title_exclude,
                 description_exclude, title_must_include, description_must_include,
                 title_first_word_exclude):
        self._search_query = search_query
        self._latitude = latitude
        self._longitude = longitude
        self._max_distance = max_distance
        self._condition = condition
        self._min_price = min_price
        self._max_price = max_price
        self._title_exclude = title_exclude
        self._description_exclude = description_exclude
        self._title_must_include = title_must_include
        self._description_must_include = description_must_include
        self._title_first_word_exclude = title_first_word_exclude
    
    @classmethod
    def load_from_json(cls, json_data):
        return cls(
            json_data['search_query'],
            json_data['latitude'],
            json_data['longitude'],
            json_data['max_distance'],
            json_data['condition'],
            json_data['min_price'],
            json_data['max_price'],
            json_data['title_exclude'],
            json_data['description_exclude'],
            json_data['title_must_include'],
            json_data['description_must_include'],
            json_data['title_first_word_exclude']
        )

    def get_search_query(self):
        return self._search_query

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude

    def get_max_distance(self):
        return self._max_distance

    def get_condition(self):
        return self._condition

    def get_min_price(self):
        return self._min_price

    def get_max_price(self):
        return self._max_price

    def get_title_exclude(self):
        return self._title_exclude

    def get_description_exclude(self):
        return self._description_exclude

    def get_title_must_include(self):
        return self._title_must_include

    def get_description_must_include(self):
        return self._description_must_include

    def get_title_first_word_exclude(self):
        return self._title_first_word_exclude