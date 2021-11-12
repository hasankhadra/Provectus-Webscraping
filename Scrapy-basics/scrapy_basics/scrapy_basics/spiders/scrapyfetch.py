import scrapy
import time
from scrapy_basics.items import GpuItem


class GPUInfoFetch(scrapy.Spider):
    """
    The class inherits from scrapy.Spider to use all Spider functionality for scraping.
    This class fetches gpu information :(store_name,gpu_model,gpu_name,fetch_ts,gpu_price,in_stock,url)
    from any given websites.
    The output of the scraping is stored in output.csv in the directory Scrapy-basics/scrapy_basics
    """
    # the name of the spider
    name = "extract_gpus"

    # the user agent string helps the destination server identify which browser, type of
    # device, and operating system is being used to avoid being restricted from scraping
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3'

    def start_requests(self):
        """
        Starts the first request of the main page of each website defined in the list urls
        """

        # websites to be scraped
        urls = ['https://www.regard.ru/catalog/group4000.htm',
                "https://www.onlinetrade.ru/catalogue/videokarty-c338/?page=0"]

        # we specify the xpath selector for each attribute beforehand and we pass it through the workflow
        # so the solution can work for any website by only passing the correct selectors.
        xpath_selectors = [
            {
                'pages_selector': "//div[@class='pagination']/a/@href",
                'in_stock_selector': "//div[@class='goodCard_inStock_button inStock_available']/text()",
                'gpu_model_selector': "//div[@id='tabs-1']/table/tr[6]/td[2]/text()",
                "gpu_name_selector": "//div[@class='block']/div[@class='bcontent']//a[@class='header']/text()",
                'url_selector': "//div[@class='block']/div[@class='bcontent']//a[@class='header']/@href",
                'gpu_price_selector': "//div[@class='block']/div[@class='bcontent']/div[@class='price']/span[2]/text()",
                'store_name_selector': "//div[@id='logo']/a/img/@alt",
                'page_selector_function': self.parse_all_pages,  # function that works on websites
                # with no "Next Page" button

                'in_stock_type': "text"  # in case the information was just a string indicating
                # the in_stock attribute: "in stock"
            },

            {
                'pages_selector': "//div[@class='paginator__links']/a[normalize-space(@title)='Следующие 15"
                                  " товаров']/@href",
                'in_stock_selector': "//span[@class='catalog__displayedItem__availabilityCount']/label/text()",
                'gpu_model_selector': "//div[@class='productPage__shortProperties']/ul[normalize-space(@class)"
                                      "='featureList columned']/"
                                      "li[@class='featureList__item'][1]/text()",
                "gpu_name_selector": "//a[normalize-space(@class)='indexGoods__item__name indexGoods__item__"
                                     "name__3lines']/text()",
                'url_selector': "//a[normalize-space(@class)='indexGoods__item__name "
                                     "indexGoods__item__name__3lines']/@href",
                'gpu_price_selector': "//span[normalize-space(@class)='price regular js__actualPrice' or "
                                      "contains(@class, 'price js__actualPrice')]/text()",
                'store_name_selector': "//img[@id='logo']/@alt",
                'page_selector_function': self.parse_by_next_page,  # function that works on websites that
                # have "Next Page" button

                'scrape_first_page': True,  # in case of iterating by pressing the "Next Page" button,
                # we need to manually scrape
                # the first page before moving to the next page

                "in_stock_type": "number"  # in case the information contained the number of items available:
                # "in stock > 10 products" or "10 products remaining"
            }
        ]

        for url, xpath_selector in zip(urls, xpath_selectors):

            if xpath_selector.get("scrape_first_page"):
                yield scrapy.Request(url=url, callback=self.parse_page, dont_filter=True, meta=xpath_selector)

            yield scrapy.Request(url=url, callback=xpath_selector['page_selector_function'], dont_filter=True,
                                 meta=xpath_selector)

    def parse_all_pages(self, response):
        """
        Extracts the links of all pages to scrape at once, and scrape them
        :param response: the response of object of the request
        """

        pages = response.xpath(response.meta.get('pages_selector')).extract()

        for page in pages:
            next_page = response.urljoin(page)  # concat the sub-link to the main link to form a correct full link
            yield scrapy.Request(url=next_page, callback=self.parse_page, meta=response.meta)

    def parse_by_next_page(self, response):
        """
        Extracts the links of the pages to scrape by imitating the process of pressing "Next Page"
        in the website, and scrape them
        :param response: the response of object of the request

        """

        next_page = response.xpath(response.meta.get('pages_selector')).extract_first()  # extract next page link

        if next_page:  # if this is the last page the recursive call will stop
            next_page = response.urljoin(next_page)

            # scrape the next page and its information to the csv file
            yield scrapy.Request(url=next_page, callback=self.parse_page, meta=response.meta, dont_filter=True)

            # recursively go to the next page to iterate more pages
            yield scrapy.Request(url=next_page, callback=self.parse_by_next_page, meta=response.meta)

    def parse_misc(self, response):
        """
        :param response: the response of object of the request
        Scrape the contents of the product's page inside response and extract:
        gpu_model, in_stock
        """

        # read the already fetched info from the meta data in the response object
        gpu_name = response.meta.get('gpu_name')
        url = response.meta.get('url')
        gpu_price = response.meta.get('gpu_price')
        fetch_ts = response.meta.get('fetch_ts')
        store_name = response.meta.get('store_name')

        in_stock = response.xpath(response.meta.get("in_stock_selector")).extract_first()

        # the case of having the number of remaining items
        if response.meta.get("in_stock_type") == "number":
            if not in_stock:  # if no information was specified the item is considered out of stock
                in_stock = False
            else:
                in_stock_text = in_stock.split(" ")
                in_stock = False
                for element in in_stock_text:
                    try:
                        if int(element) > 0:
                            in_stock = True
                            break
                    except:
                        continue
        else:
            in_stock = in_stock == "в наличии"

        gpu_model = response.xpath(response.meta.get("gpu_model_selector")).extract_first()

        if gpu_model:
            # extract special html characters
            gpu_model = gpu_model.replace('\xa0', '')

        gpuitem = GpuItem(gpu_name=gpu_name, gpu_price=gpu_price, url=url, fetch_ts=fetch_ts, store_name=store_name,
                      in_stock=in_stock, gpu_model=gpu_model)

        yield gpuitem

    def parse_page(self, response):
        """
        :param response: the response of object of the request
        Scrape the contents of the page inside response and extract:
        gpu_name, url, store_name, fetch_ts, price
        """

        # Get gpu names
        titles = response.xpath(response.meta.get("gpu_name_selector")).extract()

        # Get the url for each gpu
        links = response.xpath(response.meta.get("url_selector")).extract()

        # Get gpu prices
        prices = response.xpath(response.meta.get("gpu_price_selector")).extract()

        # Get the store name
        store_name = response.xpath(response.meta.get("store_name_selector")).extract_first()

        # Get the fetch time in seconds
        fetch_ts = time.time()

        for link, title, price in zip(links, titles, prices):

            full_link = response.urljoin(link)

            # extract special html characters
            title = title.replace('\xa0', ' ')

            # the meta data to be passed to the next callback function
            item_info = {
                'gpu_name': title,
                'url': full_link,
                'gpu_price': price,
                'fetch_ts': fetch_ts,
                'store_name': store_name
            }

            item_info.update(response.meta)
            yield scrapy.Request(url=full_link, callback=self.parse_misc, meta=item_info)
