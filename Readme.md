# Task 1 - Scraping - Naive approach

## Table of contents
1. [ Description ](#desc)
2. [ Structure of the code ](#struct)
3. [ Installation and Running ](#install)

<a name="desc"></a>
### 1. Description
In this task, we are scraping [https://www.regard.ru/](https://www.regard.ru/) to retrieve information about the available GPUs. We use `beautifulsoup4` with CSS Selectors for scraping the website. First, we get the available information in the navigation page that has a short description of each product. Then, we scrap the page of each product individually in order to get other detailed info such as the model of the GPU. After retrieving the data we store it in a csv file using `csv` python built-in library. The csv file has the following columns:
```
store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url
```

<a name="struct"></a>
### 2. Structure of the code
The code is split into two files `scrape.py` which contains the functionality of scraping the website and retrieving the required information and `to_csv.py` which is responsible of handling the storing of the data in the csv file. 

<a name="install"></a>
### 3. Installation and Running
Clone this repo to your local machine. `cd` to the directory of the repo and install all the requirements with the command:
```
pip install -r requirements.txt
```
Now, in the same command line run:
```
python3 scrape.py
```
After running the script, the file `output.csv` will be overwritten (or created in case it wasn't created before) with the new information from the website.
