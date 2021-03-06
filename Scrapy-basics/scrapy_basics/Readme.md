# Task 2 - Scraping - Scrapy with XPath

## Table of contents
1. [ Description ](#desc)
2. [ Structure of the code ](#struct)
3. [ Installation and Running ](#install)

<a name="desc"></a>
### 1. Description
In this task, we are scraping [https://www.regard.ru/](https://www.regard.ru/) and [https://www.onlinetrade.ru/](https://www.onlinetrade.ru/) to retrieve information about the available GPUs. We're using Scrapy with XPath Selectors for scraping the website. First, we get the available information in the navigation page that has a short description of each product (`gpu_name, store_name, gpu_price, url`). Then, we scrape the page of each product individually in order to get other detailed info such as the model of the GPU (`gpu_model`) and the `in_stock` attribute. After retrieving the data we store it in `output.csv`. The csv file has the following columns:
```
store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url
```

<a name="struct"></a>
### 2. Structure of the code
The code is structured using `Scrapy` library, and the logic of the main code can be found in [`Scrapy-basics/scrapy_basics/scrapy_basics/spiders/scrapyfetch.py`](https://github.com/hasankhadra/Provectus-Webscraping/blob/dev_part2/Scrapy-basics/scrapy_basics/scrapy_basics/spiders/scrapyfetch.py). In `items.py` we define the attributes of a gpu product (which are the same as the columns of `output.csv`). We also specify some extra settings in `settings.py` to fix some bugs that might happen during scraping. 

<a name="install"></a>
### 3. Installation and Running
Clone this repo to your local machine. `cd` to `/Provectus-Webscraping/Scrapy-basics/scrapy_basics` and install all the requirements with the command:
```
pip install -r requirements.txt
```
Now, in the same command line run:
```
scrapy crawl extract_gpus -o output.csv -t csv
```
After running the script, the file `output.csv` will be overwritten (or created in case it wasn't created before) with the new information from the website. The file will be created in the same directory you are currently in.
