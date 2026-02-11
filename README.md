
  # Wallamonitor 📲 
  **Automate your Wallapop searches and get notified on Telegram when new items are listed!**  
  This bot periodically searches Wallapop for new items based on your specific parameters and sends real-time notifications to your designated Telegram channel.

  ## Table of Contents
  - [Setup](#setup-)
  - [Configuration](#configuration-)
  - [Usage](#usage-)
  - [Docker Setup](#docker-setup-)

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

  ## Docker Setup 🐳

  Wallamonitor can be easily deployed using Docker, which provides an isolated environment and simplifies dependency management.

  ### Prerequisites

  - Docker installed on your system ([Download Docker](https://www.docker.com/get-started))
  - Docker Compose (usually included with Docker Desktop)

  ### Environment Setup

  1. Create a `.env` file in the project root with your Telegram credentials:
     ```env
     TELEGRAM_CHANNEL=@Your_Telegram_Channel_ID
     TELEGRAM_TOKEN=Your_Telegram_Bot_Token
     ```

  2. Create your search configuration file in the `searches/` directory (e.g., `searches/example.json`):
     ```json
     [
       {
         "search_query": "iphone",
         "latitude": "40.4165",
         "longitude": "-3.70256",
         "max_distance": "0",
         "condition": "all",
         "min_price": "0",
         "max_price": "200",
         "title_exclude": [],
         "description_exclude": [],
         "title_must_include": [],
         "title_first_word_exclude": "",
         "description_must_include": []
       }
     ]
     ```

  ### Running with Docker Compose

  The `docker-compose.yml` includes a template service that you can customize:

  1. **Start the default example service:**
     ```bash
     docker-compose up -d wallamonitor-example
     ```

  2. **Add your own monitoring service:**
     
     Edit `docker-compose.yml` and add a new service (uncomment and modify the laptops example):
     ```yaml
     wallamonitor-laptops:
       <<: *wallamonitor-base
       container_name: wallamonitor-laptops
       volumes:
         - ./searches/laptops.json:/app/args.json:ro
     ```

  3. **Run multiple monitors simultaneously:**
     ```bash
     docker-compose up -d
     ```
     
     This will start all configured services at once, each monitoring different search criteria.

  4. **View logs:**
     ```bash
     docker-compose logs -f wallamonitor-example
     ```

  5. **Stop the services:**
     ```bash
     docker-compose down
     ```


  ---

  Feel free to reach out if you have any issues with Wallamonitor or have suggestions to improve it. Happy shopping! 🛒📲
