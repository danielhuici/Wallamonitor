# Wallamonitor
Periodically checks Wallapop for new articles based on specified parameters and notify through Telegram channel.

### Setup 🔧
```
pip install -U python-dotenv
pip install python-telegram-bot 
```

You will also need to change .env parameters:
```
TELEGRAM_CHANNEL_ID=@Your_Telegram_Channel_ID
TELEGRAM_TOKEN=Your Telegram Token
```

### Usage 🔧

```
$ python -h
usage: alert.py [-h] --name NAME [--latitude LATITUDE] [--longitude LONGITUDE] [--condition CONDITION]
                [--min MIN_PRICE] [--max MAX_PRICE]

Arguments

optional arguments:
  -h, --help              show this help message and exit
  --name NAME             Article name
  --latitude LATITUDE     Latitude
  --longitude LONGITUDE   Longitude
  --condition CONDITION   Item condition: all, new, as_good_as_new, good, fair, has_given_it_all
  --min MIN_PRICE         Min price
  --max MAX_PRICE         Max price
```

Example:
``` 
$ python alert.py --name ps5 --condition new --min 400 --max 600
```
  
  
