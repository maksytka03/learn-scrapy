# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()


class BrickItem(scrapy.Item):
    age_range = scrapy.Field()
    availability = scrapy.Field()
    barcodes = scrapy.Field()
    designer = scrapy.Field()
    dimensions = scrapy.Field()
    item_numbers = scrapy.Field()
    launch_exit = scrapy.Field()
    minifigs = scrapy.Field()
    name = scrapy.Field()
    notes = scrapy.Field()
    number = scrapy.Field()
    packaging = scrapy.Field()
    pieces = scrapy.Field()
    price_per_piece = scrapy.Field()
    rrp = scrapy.Field()
    rating = scrapy.Field()
    subtheme = scrapy.Field()
    tags = scrapy.Field()
    theme = scrapy.Field()
    theme_group = scrapy.Field()
    set_type = scrapy.Field()
    weight = scrapy.Field()
    year_released = scrapy.Field()
