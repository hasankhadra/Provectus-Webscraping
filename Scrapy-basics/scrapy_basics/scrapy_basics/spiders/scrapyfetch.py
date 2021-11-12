# importing the scrapy module
import scrapy
import time
from scrapy_basics.items import GpuItem


class RegardFetch(scrapy.Spider):

    name = "extract_gpus"
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36 '

    def start_requests(self):
        """
        Starts the first request of the main page
        """

        urls = ['https://www.regard.ru/catalog/group4000.htm', ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)

    def parse_pages(self, response):
        """
        Extracts the links of the pages to scrape and scrape them
        """

        pages = response.xpath("//div[@class='pagination']/a/@href").extract()

        for page in pages:
            next_page = response.urljoin(page)
            yield scrapy.Request(url=next_page, callback=self.parse_page)

    def parse_misc(self, response):
        """
        :param response: the response of object of the request
        Scrape the contents of the product's page inside response and extract:
        gpu_model, in_stock
        """

        gpu_name = response.meta.get('gpu_name')
        url = response.meta.get('url')
        gpu_price = response.meta.get('gpu_price')
        fetch_ts = response.meta.get('fetch_ts')
        store_name = response.meta.get('store_name')

        in_stock = response.xpath("//div[@class='goodCard_inStock_button inStock_available']/text()").extract_first() == 'в наличии'
        gpu_model = response.xpath("//div[@id='tabs-1']/table/tr[6]/td[2]/text()").extract_first()

        yield GpuItem(gpu_name=gpu_name, gpu_price=gpu_price, url=url, fetch_ts=fetch_ts, store_name=store_name,
                      in_stock=in_stock, gpu_model=gpu_model)

    def parse_page(self, response):
        """
        :param response: the response of object of the request
        Scrape the contents of the page inside response and extract:
        gpu_name, url, store_name, fetch_ts, price
        """

        # Get gpu names
        titles = response.xpath("//div[@class='block']/div[@class='bcontent']//a[@class='header']/text()").extract()

        # Get the url for each gpu
        links = response.xpath("//div[@class='block']/div[@class='bcontent']//a[@class='header']/@href").extract()

        # Get gpu prices
        prices = response.xpath("//div[@class='block']/div[@class='bcontent']/div[@class='price']/span[2]/text()").extract()

        # Get the store name
        store_name = response.xpath("//div[@id='logo']/a/img/@alt").extract_first()

        # Get the fetch time in seconds
        fetch_ts = time.time()

        for link, title, price in zip(links, titles, prices):
            full_link = "https://www.regard.ru" + link

            item_info = {
                'gpu_name': title,
                'url': full_link,
                'gpu_price': price,
                'fetch_ts': fetch_ts,
                'store_name': store_name
            }

            yield scrapy.Request(url=full_link, callback=self.parse_misc, meta=item_info)


