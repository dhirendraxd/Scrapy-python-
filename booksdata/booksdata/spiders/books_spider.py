import scrapy
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from scrapy_rotating_proxies.middlewares import RotatingProxyMiddleware, BanDetectionMiddleware

class BooksSpider(scrapy.Spider):
    name = "paisa"
    allowed_domains = ["hathighoda.com"]
    start_urls = [
        "https://hathighoda.com/",
        "https://hathighoda.com/collections/accessories",
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            'scrapy_rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'scrapy_rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],
        'HTTPERROR_ALLOWED_CODES': [403],
        'ROTATING_PROXY_LIST': [
            # Add a list of proxies here
            'proxy1.com:8000',
            'proxy2.com:8031',
            # ...
        ],
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        if response.status == 403:
            self.log(f"Access denied to {response.url}")
            return

        page = response.url.split("/")[-2]
        filename = f"paisa-{page}.html"
        
        self.log(f"Saved file {filename}")

        # Correct the CSS selectors to match the actual structure of the target website
        cards = response.css('.product-grid.count-18 .product-item')
        for card in cards:
            title = card.css(".product-card-title a::text").get()
            rating = card.css(".star-rating::attr(class)").re_first('star-rating ([A-Za-z]+)')
            image_url = card.css(".product-card-image img::attr(src)").get()

            if image_url and not image_url.startswith("http"):
                image_url = response.urljoin(image_url)

            self.log(f"Title: {title}, Rating: {rating}, Image URL: {image_url}")

            # Collect the data into a dictionary
            book_detail = {
                'title': title,
                'rating': rating,
                'image_url': image_url
            }

            # Print or save the book details
            print(book_detail)
            # Here you can also yield the book_detail dictionary to send it to a pipeline
            # yield book_detail
