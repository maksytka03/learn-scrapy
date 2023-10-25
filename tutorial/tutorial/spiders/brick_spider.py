import scrapy
import asyncio
from ..items import BrickItem
import random


class BrickSpider(scrapy.Spider):
    name = "brick"
    allowed_domains = ["brickset.com"]
    start_urls = ["https://brickset.com/sets/year-2023"]

    async def parse(self, response):
        sets = response.css("article.set")
        for brick_set in sets:
            await asyncio.sleep(random.randrange(1, 6))
            relative_url = brick_set.css("h1 a::attr(href)").get()
            yield response.follow(relative_url, callback=self.parse_set)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    async def parse_set(self, response):
        main_div = response.css("div.text")

        brick_item = BrickItem()

        terms = main_div.xpath("//dl/dt/text()").getall()

        details = main_div.xpath("//dl/dd/text()").getall()
        details_href = main_div.xpath("//dl/dd/a/text()").getall()

        all_dict = {}

        for element in main_div.xpath("//dl/*"):
            if element.root.tag == "dt":
                # If the element is a <dt>, set it as the current term
                current_term = element.xpath("text()").get()
            elif element.root.tag == "dd":
                # If the element is a <dd>, add it to the current term
                current_description = element.xpath("string(.)").get()
                if current_term not in all_dict:
                    all_dict[current_term] = set()
                all_dict[current_term].add(current_description)
            elif element.root.tag == "a":
                # If the element is an <a>, you can choose to extract and store
                # the link/text
                text = element.xpath("text()").get()
                if current_term not in all_dict:
                    all_dict[current_term] = set()
                all_dict[current_term].add(f"Link: {text}")

        for k, v in all_dict.items():
            all_dict[k] = list(v)[0]

        brick_item["age_range"] = (
            all_dict["Age range"] if "Age range" in all_dict else None
        )
        brick_item["availability"] = (
            all_dict["Availability"] if "Availability" in all_dict else None
        )
        brick_item["barcodes"] = (
            all_dict["Barcodes"] if "Barcodes" in all_dict else None
        )
        brick_item["designer"] = (
            all_dict["Designer"] if "Designer" in all_dict else None
        )
        brick_item["dimensions"] = (
            all_dict["Dimensions"] if "Dimensions" in all_dict else None
        )
        brick_item["item_numbers"] = (
            all_dict["LEGO item numbers"] if "LEGO item numbers" in all_dict else None
        )
        brick_item["launch_exit"] = (
            all_dict["Launch/exit"] if "Launch/exit" in all_dict else None
        )
        brick_item["minifigs"] = (
            all_dict["Minifigs"] if "Minifigs" in all_dict else None
        )
        brick_item["name"] = all_dict["Name"] if "Name" in all_dict else None
        brick_item["number"] = all_dict["Number"] if "Number" in all_dict else None
        brick_item["packaging"] = (
            all_dict["Packaging"] if "Packaging" in all_dict else None
        )
        brick_item["pieces"] = all_dict["Pieces"] if "Pieces" in all_dict else None
        brick_item["price_per_piece"] = (
            all_dict["Price per piece"] if "Price per piece" in all_dict else None
        )
        brick_item["rrp"] = all_dict["RRP"] if "RRP" in all_dict else None
        brick_item["rating"] = all_dict["Rating"] if "Rating" in all_dict else None
        brick_item["subtheme"] = (
            all_dict["Subtheme"] if "Subtheme" in all_dict else None
        )
        brick_item["tags"] = all_dict["Tags"] if "Tags" in all_dict else None
        brick_item["theme"] = all_dict["Theme"] if "Theme" in all_dict else None
        brick_item["theme_group"] = (
            all_dict["Theme group"] if "Theme group" in all_dict else None
        )
        brick_item["set_type"] = all_dict["Type"] if "Type" in all_dict else None
        brick_item["weight"] = all_dict["Weight"] if "Weight" in all_dict else None
        brick_item["year_released"] = (
            all_dict["Year released"] if "Year released" in all_dict else None
        )

        yield brick_item
