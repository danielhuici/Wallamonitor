# Wallamonitor
Periodically checks Wallapop for new articles based on specified parameters and notify through Telegram channel.

### Setup 🔧
```
pip3 install -U python-dotenv
pip3 install python-telegram-bot 
```

You will also need to change .env parameters:
```
TELEGRAM_CHANNEL_ID=@Your_Telegram_Channel_ID
TELEGRAM_TOKEN=Your Telegram Token
```

### Usage
1. Create a `args.json` file and fill it with following parameters (JSON):

```
[
  {
    "product_name": "name", # Find products containing name
    "distance": "0", # Distance search range (Meters). Use 0 for no limits
    "latitude": "", # Latitude origin for distance search
    "longitude": "", # Longitude origin for distance search
    "condition": "all", # Can be: all, new, as_good_as_new, good, fair, has_given_it_all
    "min_price": "40", # Minimum price
    "max_price": "80", # Maximum price
	  "title_keyword_exclude" : ["word1", "word2"], # Exclude an item if it contains one of this words
	  "exclude": ["word1", "word2"] # Exclude an item if title or description contains one of this words
  },
  
  ...
]

```

Check the file `args.json` of this repo for an example.


2. Run:
``` 
$ python3 alert.py
```  


