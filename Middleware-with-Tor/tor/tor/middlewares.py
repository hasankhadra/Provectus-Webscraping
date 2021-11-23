import os
from dotenv import load_dotenv
from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from stem.util.log import get_logger

# load environment variables
load_dotenv()

# stop the logging in the terminal to not make it messy
logger = get_logger()
logger.propagate = False


def new_tor_identity():
    with Controller.from_port(port=9051) as controller:
        # authenticate with the tor password
        controller.authenticate(password=os.getenv('TOR_PASSWORD'))

        # Change tor identity
        controller.signal(Signal.NEWNYM)


class ProxyMiddleware(HttpProxyMiddleware):
    """
    Class that inherits from HttpProxyMiddleware and implements its two functions:
    - process_response(self, request, response, spider)
    - process_request(self, request, spider)
    It's responsible for connecting to Tor, adding a proxy for each request and changing
    Tor identity each REQUESTS_PER_SAME_TOR_IDENTITY requests.
    """

    # Number of requests sent during the current tor identity
    def __init__(self, *args, **kwargs):
        super(ProxyMiddleware, self).__init__()
        self.num_sent_requests = 0

    def process_response(self, request, response, spider):
        # get a new identity if the response wasn't successful
        if response.status != 200:
            new_tor_identity()
            return request

        return response

    def process_request(self, request, spider):

        # get a new identity
        if self.num_sent_requests >= spider.settings['REQUESTS_PER_SAME_TOR_IDENTITY']:
            self.num_sent_requests = 0
            new_tor_identity()

        self.num_sent_requests += 1

        # add a proxy for the response
        request.meta['proxy'] = 'http://127.0.0.1:8118'
