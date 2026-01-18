
  # Wallamonitor 📲 
  **Automate your Wallapop searches and get notified on Telegram when new items are listed!**  
  This bot periodically searches Wallapop for new items based on your specific parameters and sends real-time notifications to your designated Telegram channel.

  ## Table of Contents
  - [Setup](#setup-)
  - [Configuration](#configuration-)
  - [Usage](#usage-)

  ## Setup 🔧

  1. Install required packages:
     ```bash
     pip3 install -r requirements.txt
     ```

  2. Configure your Telegram details in `config.yaml`:
     ```yaml
     TELEGRAM_CHANNEL_ID: "@Your_Telegram_Channel_ID"
     TELEGRAM_TOKEN: "Your Telegram Token"
     ```

  ## Configuration 🛠️

  Create an `args.json` file with your search parameters. This file tells Wallamonitor what items you’re looking for, such as price range, condition, and other criteria. You can set multiple search configurations within this file.
  

  ### Parameters:
  | Parameter                  | Description                                                                                               | Example                  | Mandatory         |
  |----------------------------|-----------------------------------------------------------------------------------------------------------|--------------------------|-------------------|
  | `search_query`             | Main search term. Only items containing this phrase in their title will be found.                         | `"laptop"`               | **Yes**          |
  | `min_price`                | Minimum item price.                                                                                       | `"100"`                  | **Yes**          |
  | `max_price`                | Maximum item price.                                                                                       | `"500"`                  | **Yes**          |
  | `latitude`                 | Latitude of your location for distance-based filtering.                                                   | `"40.4165"`              | No               |
  | `longitude`                | Longitude of your location for distance-based filtering.                                                  | `"-3.70256"`             | No               |
  | `max_distance`             | Search range (in kilometers) from the specified latitude/longitude. Use `"0"` for no limit.               | `"10"`                   | No               |
  | `condition`                | Item condition to filter by. Options: `all`, `new`, `as_good_as_new`, `good`, `fair`, `has_given_it_all`. | `"good"`                 | No               |
  | `title_exclude`            | List of words that, if present in the title, will exclude an item.                                        | `["broken", "parts"]`    | No               |
  | `description_exclude`      | List of words that, if present in the description, will exclude an item.                                  | `["damaged"]`            | No               |
  | `title_must_include`       | List of required words in the title. If none of these words appear, the item will be excluded.            | `["Intel", "i5"]`        | No               |
  | `description_must_include` | List of required words in the description. If none of these words appear, the item will be excluded.      | `["working"]`            | No               |
  | `title_first_word_include` | Notify only if the first word of the title matches the specified word.                                    | `"New"`                  | No               |

Check out [args.json](./args.json) for an example

  ## Usage 🚀

  1. Ensure your `args.json` file is filled out with the parameters you’d like Wallamonitor to use for its searches.
  2. Run Wallamonitor:

     ```bash
     python3 wallamonitor.py
     ```

  The bot will monitor Wallapop periodically (default 15s) and send notifications to your specified Telegram channel whenever new items match your criteria.

  ---

  Feel free to reach out if you have any issues with Wallamonitor or have suggestions to improve it. Happy shopping! 🛒📲
