import scrapy
from pathlib import Path

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]
    
    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/classics_6/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
                    
    def parse(self, response):
        page = response.url.split("/")[-2] 
        filename = f"books-{page}.html"
        bookdetail = {}
        
        #Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        card  = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)
            rating = card.css("")
            image = card.css(".image_container img::attr(src)")
            print(image.attrib["src"])
            
     

        