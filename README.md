# Wallamonitor
Periodically checks Wallapop for new articles based on specified parameters and notify them through Telegram channel.

### Setup 🔧
```
pip3 install pyyaml python-telegram-bot 
```

You will also need to set your Telegram config at `config.yaml`:
```
TELEGRAM_CHANNEL_ID=@Your_Telegram_Channel_ID
TELEGRAM_TOKEN=Your Telegram Token
```

### Usage
1. Create a `args.json` file and fill it with following parameters (JSON):

```
[
  {
    "search_query": "search query", # Find products containing...
    "latitude": "40.4165", # Latitude origin for distance search
    "longitude": "-3.70256", # Longitude origin for distance search
    "max_distance":"0", # Distance search range (in meters). Use 0 for unlimited distance
    "condition": "all", # Can be: all, new, as_good_as_new, good, fair, has_given_it_all
    "min_price": "20", # Minimum price
    "max_price": "80", # Maximum price
    "title_exclude" : [], # Exclude an item if title contains one of this words
    "description_exclude": [], # Exclude an item if description contains one of this words
    "title_must_include" : [], # Exclude an item if title does not contains one of this words
    "description_must_include" : [] # Exclude an item if description does not contains one of this words
  },

  
  ...
]

```

Check the file `args.json` of this repo for an example.


2. Run:
``` 
$ python3 main.py
```  


