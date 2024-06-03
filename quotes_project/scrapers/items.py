import scrapy

class QuoteItem(scrapy.Item):
    tags = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()

class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    bio = scrapy.Field()

