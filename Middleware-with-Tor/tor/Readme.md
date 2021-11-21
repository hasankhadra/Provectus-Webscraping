# Task 3 - Scraping - Scrapy with Tor

## Table of contents
1. [ Description ](#desc)
2. [ Structure of the code ](#struct)
3. [ Installation and Running ](#install)

<a name="desc"></a>
### 1. Description
In this task, we are scraping [https://www.regard.ru/](https://www.regard.ru/) and [https://www.onlinetrade.ru/](https://www.onlinetrade.ru/) to retrieve 
information about the available GPUs while using Tor and Proxy. We're using Scrapy with XPath Selectors for scraping the website. First, we get the available information 
in the navigation page that has a short description of each product (`gpu_name, store_name, gpu_price, url`). Then, we scrape the page of each product 
individually in order to get other detailed info such as the model of the GPU (`gpu_model`) and the `in_stock` attribute. 

For each 
`REQUESTS_PER_SAME_TOR_IDENTITY` requests (Can be modified. Defined in `settings.py`) the `downloader_middleware` changes Tor identity and provide
a proxy for each outgoing request through Tor network. Also, if the response was unsuccessful, the middleware changes Tor identity and resends the request.

After retrieving the data we 
store it in `output.csv`. The csv file has the following columns:
```
store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url
```

<a name="struct"></a>
### 2. Structure of the code
The code is structured using `Scrapy` library, and the logic of the main code can be found in 
[`scrapyfetch-tor.py`](https://github.com/hasankhadra/Provectus-Webscraping/blob/dev_part3/Middleware-with-Tor/tor/tor/spiders/scrapyfetch-tor.py). 
In `middlewares.py`, we implement our custom `downloader_middleware` to the purpose explained above. In `items.py` we define the attributes of a gpu 
product (which are the same as the columns of `output.csv`). We also set some settings in `settings.py` 
to specify the `downloader_middleware` we will use and some describe extra settings.

<a name="install"></a>
### 3. Installation and Running
Clone this repo to your local machine. `cd` to `Provectus-Webscraping/Middleware-with-Tor/tor` and install all the requirements with the command:
```
pip install -r requirements.txt
```
In the same command line run the command `cd tor`. Note the `.env.example` file which contain some sensitive and private data. 
To run the code successfully, you need to rename this file to `.env` and then create your own `tor-password` and insert it in the 
correct place inside `.env`.

After you've configured your `.env` file, in the same command line run the following commands:
```
cd spiders
scrapy crawl extract_gpus_tor -o output.csv -t csv
```
After running the script, the file `output.csv` will be overwritten (or created in case it wasn't created before) with the new information from 
the website. The file will be created in the same directory you are currently in.
