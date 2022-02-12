import scrapy


class ReviewsCrawlerItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    artist = scrapy.Field()
    album = scrapy.Field()
    rating = scrapy.Field()
    intro = scrapy.Field()
    text = scrapy.Field()
