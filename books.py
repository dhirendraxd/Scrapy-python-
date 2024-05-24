import scrapy


class BooksSpider(scrapy.Spider):
    name = "paisa"
    allowed_domains = ["hathighoda.com"]
    start_urls = ["https://hathighoda.com/"]

    def parse(self, response):
        pass
