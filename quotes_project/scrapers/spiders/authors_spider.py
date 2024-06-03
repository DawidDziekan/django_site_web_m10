import scrapy
from scrapers.items import AuthorItem
from quotes.models import Author

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    start_urls = ['http://quotes.toscrape.com/']
    saved_authors: list[str] = []
    
    custom_settings = {
        'FEEDS': {
            'authors.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
            },
        },
    }
    
    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            
            author_name = quote.xpath('.//span/small[@class="author"]/text()').get()

            if author_name not in self.saved_authors:
                self.saved_authors.append(author_name)
                author_url = response.urljoin(quote.xpath('.//span/a/@href').get())
                yield scrapy.Request(author_url, callback=self.parse_author_info)

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_author_info(self, response):
        item = AuthorItem()
        item['name'] = response.xpath('//h3[@class="author-title"]/text()').get()
        item['born_date'] = response.xpath('//span[@class="author-born-date"]/text()').get()
        item['born_location'] = response.xpath('//span[@class="author-born-location"]/text()').get()
        item['bio'] = response.xpath('//div[@class="author-description"]/text()').get()
        
        author = Author.objects.create(
            name=item['name'],
            born_date=item['born_date'],
            born_location=item['born_location'],
            bio=item['bio']
        )
        author.save()
        yield item
