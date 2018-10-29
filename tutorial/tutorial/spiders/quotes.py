# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            item = QuotesItem()
            test1 = quote.xpath('.//span[@class="text"]/text()')
            test2 = quote.xpath('.//span[@class="text"]/text()').extract()
            test3 = quote.xpath('.//span[@class="text"]/text()').extract_first()
            # item['text'] = quote.xpath('.//span[@class="text"]/text()').extract_first()
            # item['author'] = quote.xpath('.//small[@class="author"]/text()').extract_first()
            # item['tags'] = quote.xpath('.//a[@class="tag"]/text()').extract()
            # print(item)
            # yield item
            print("*******")
            print(test1)
            print(test2)
            print(test3)

        # next_url = response.xpath('//nav//li[@class="next"]/a/@href').extract_first()
        # url = response.urljoin(next_url)
        # yield scrapy.Request(url=url, callback=self.parse)

