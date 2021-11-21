import scrapy

class IfconfigSpider(scrapy.Spider):
    name = 'extract_gpus'
    allowed_domains = ['ifconfig.me']
    start_urls = ['http://ifconfig.me/']
    def start_requests(self):
        for i in range(10):
            yield scrapy.Request(url="https://check.torproject.org/", callback=self.parse, dont_filter=True)

    def parse(self, response):
        yield {"proxy": response.xpath("//div[@class='content']//p[1]/strong/text()").extract()}
        print("AAAAAAAAAA", response.xpath("//div[@class='content']//p[1]/strong/text()").extract())
