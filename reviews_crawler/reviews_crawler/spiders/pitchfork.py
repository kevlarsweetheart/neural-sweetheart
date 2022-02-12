import scrapy
import uuid
from reviews_crawler.items import ReviewsCrawlerItem


class PitchforkReviewsCrawler(scrapy.Spider):
    name = 'pitchfork'
    start_urls = ['https://pitchfork.com/reviews/albums/?page=1']
    allowed_domains = ['pitchfork.com']

    def parse_page(self, response):
        pages = response.xpath('//a[contains(@class, "review__link")]/@href').extract()
        for page in pages:
            yield scrapy.Request('https://pitchfork.com' + page, callback=self.parse_review_page)

    @staticmethod
    def parse_review_page(response):
        _id = str(uuid.uuid4().hex)
        url = response.url
        album = response.xpath('//h1[contains(@class, "ContentHeaderHed-")]//text()').extract_first()
        rating = str(int(float(response.xpath('//div[contains(@class, "ScoreCircle")]/p/text()').extract_first()) * 10))
        artist = response.xpath('//div[contains(@class, "ContentHeaderArtist-")]/text()').extract_first()
        intro = response.xpath('//div[contains(@class, "ContentHeaderDekDown-")]/text()').extract_first()

        text = []
        for paragraph in response.xpath('//div[contains(@class, "body__inner-container")]/p'):
            text.append("".join(paragraph.xpath(".//text()").extract()))
        text = ' '.join(text)
        review = ReviewsCrawlerItem(_id=_id, url=url, artist=artist, album=album, rating=rating, intro=intro, text=text)
        yield review

    def parse(self, response):
        for page in range(1, 1001):
            new_page = response.url[:-1] + str(page)
            yield scrapy.Request(new_page, callback=self.parse_page)
