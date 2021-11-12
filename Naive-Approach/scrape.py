from bs4 import BeautifulSoup
import requests
import time
from to_csv import ToCsv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
BASE_URL = "https://www.regard.ru"


class Scrape:
    """
    Class that scrapes a website and retrieves information about all GPUs listed
    in that websiste.
    """

    def __init__(self, headers: dict, base_url: str):
        self.headers = headers
        self.base_url = base_url
        self.fetched_products = 0
        self.to_csv_instance = ToCsv('output.csv')

        self.to_csv_instance.empty_file()
        self.to_csv_instance.add_header(['url', 'gpu_name', 'store_name', 'fetch_ts', 'gpu_price', 'in_stock',
                                         'gpu_model'])

    def get_num_of_pages(self):
        """
        function that retrieves the number of pages to scrape in the website
        :return: the number of the pages to scrape
        """

        page = requests.get(self.base_url + "/catalog/group4000/page1.htm", headers=self.headers)
        soup = BeautifulSoup(page.text, "html.parser")
        return len(soup.select("div#hits div.pagination > a"))

    def extract_misc_info(self, product_url: str):
        """
        function that retrieves the following properties about the GPU: in_stock, gpu_model
        :param product_url: the url of the product (GPU) to scrape
        :return: a dictionary of the format:
        {
            'in_stock': whether the product is in stock or not (boolean),
            'gpu_model': The model of the GPU (string)
        }
        """

        product_page = requests.get(product_url, headers=self.headers)
        soup = BeautifulSoup(product_page.text, "html.parser")

        in_stock_content = soup.select("div.goodCard_inStock_button.inStock_available")[0].get_text()
        gpu_model_content = soup.select("div#tabs-1 table")

        try:
            gpu_model_tag = list(list(gpu_model_content[0].children)[7].children)
            gpu_model = gpu_model_tag[1].get_text()
        except:
            gpu_model = "No information"

        item_info = {"in_stock": True if in_stock_content == "в наличии" else False, "gpu_model": gpu_model}
        return item_info

    def extract_page(self, page_number: int):
        """
        Extracts all the info about the GPUs in the given page number
        :param page_number: the page number in the website
        """

        # connect to website
        page_url = f"https://www.regard.ru/catalog/group4000/page{page_number}.htm"
        page = requests.get(page_url, headers=self.headers)
        soup = BeautifulSoup(page.text, "html.parser")

        base_selector = "div#hits div.content div.block div.bcontent"  # base selector for
        url_name_content = soup.select(base_selector + " div.aheader a")  # filter the name and url tags
        id_content = soup.select(base_selector + " div.block_img div.code")  # filter the id tag
        price_content = soup.select(base_selector + " div.price ")  # filter the price tag
        store_name_content = soup.select("div#logo > a > img")  # filter the store name
        items_info = {}

        for i in range(len(id_content)):  # iterate over the products in this page
            element = url_name_content[i]

            gpu_id = id_content[i].get_text().split(" ")[1]
            gpu_name = element.get_text()
            store_name = store_name_content[0]['alt']
            url = element['href']
            fetch_ts = time.time()
            gpu_price = list(price_content[i].children)[3].get_text() + list(price_content[i].children)[-1][:4]

            items_info[gpu_id] = {"url": self.base_url + url, "gpu_name": gpu_name, "store_name": store_name,
                                  "fetch_ts": fetch_ts, 'gpu_price': gpu_price}

            items_info[gpu_id].update(self.extract_misc_info(items_info[gpu_id]['url']))

        self.fetched_products += len(id_content)
        print(f"Fetched {self.fetched_products} products.")
        self.to_csv_instance.put_data(items_info)  # put the info we collected in the csv file

    def extract_pages(self):
        """
        Extracts the information about the GPUs in all the pages of the website.
        Saves the information retrieved in a csv file.
        :return:
        """

        for page in range(1, self.get_num_of_pages() + 1):
            self.extract_page(page_number=page)

        print(f"The information about all GPUs available on website {BASE_URL} "
              f"are saved in output.csv in the same directory of scrape.py")


if __name__ == "__main__":

    scrape_instance = Scrape(HEADERS, BASE_URL)

    scrape_instance.extract_pages()

