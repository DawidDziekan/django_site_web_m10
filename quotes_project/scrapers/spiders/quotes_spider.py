import scrapy
from scrapers.items import QuoteItem
from quotes.models import Quote

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']
    allowed_domains = ['quotes.toscrape.com']

    custom_settings = {
        'FEEDS': {
            'quotes.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
            }
        }
    }

    def parse(self, response):
        # Zbieranie cytatów z bieżącej strony
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.xpath('./span[@class="text"]/text()').get()
            item['author'] = quote.xpath('./span/small[@class="author"]/text()').get()
            item['tags'] = quote.xpath('./div[@class="tags"]/a[@class="tag"]/text()').getall()
            
            author = Quote.objects.create(
            author=item['author'],
            text=item['text'],
            tags=item['Tag'],
            )
            author.save()
            
            yield item

        # Szukanie linku do następnej strony i przechodzenie do niej
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    
