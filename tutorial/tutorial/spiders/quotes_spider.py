from pathlib import Path
import scrapy

class QuoteSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ["https://quotes.toscrape.com/"]
    # def start_requests(self):
    #     urls = [
    #         "https://quotes.toscrape.com/page/1/",
    #         "https://quotes.toscrape.com/page/2/",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tags a.tag::text").getall()
        #     }
        quotes = response.css("div.quote").get()
        for quote in quotes:
            relative_url = quote.css("small.author::attr(href)").get()
            author_url = "https://quotes.toscrape.com/" + relative_url
            yield response.follow(author_url, callback=self.parse_author)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)

    def parse_quote(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {"quote": extract_with_css("span.text::text").get(),
               "tags": extract_with_css("div.tags a.tag::text").getall()}

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        pass
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
