import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from sobacoincore.items import Article


class SobacoincoreSpider(scrapy.Spider):
    name = 'sobacoincore'
    start_urls = ['https://www.sobaco-incore.com/sobaco-gruppe/news']

    def parse(self, response):
        links = response.xpath('//a[@class="btn btn-default btn-read-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)


    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="extra"]//text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="teaser-text lead"]//text()').getall() + \
                  response.xpath('//div[@class="news-text-wrap"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
