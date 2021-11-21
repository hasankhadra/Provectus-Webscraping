
BOT_NAME = 'tor'

SPIDER_MODULES = ['tor.spiders']
NEWSPIDER_MODULE = 'tor.spiders'

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'tor.middlewares.ProxyMiddleware': 543
}

REQUESTS_PER_SAME_TOR_IDENTITY = 3
ROTATING_PROXY_NUM = 0