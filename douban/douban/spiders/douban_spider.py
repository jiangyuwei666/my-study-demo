# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名。别和项目名重复
    name = 'douban_spider'
    # 允许的域名（不在该域名下的就不爬取）
    allowed_domains = ['movie.douban.com']
    # 入口url，放在调度器里
    start_urls = ['http://movie.douban.com/top250']

    # 默认的解析方法
    def parse(self, response):
        # 循环item的条目
        movie_list = response.xpath('//ol[@class="grid_view"]//li')
        for movie in movie_list:
            item = DoubanItem()
            item['serial_number'] = movie.xpath('.//div[@class="pic"]//em/text()').extract_first()
            item['movie_name'] = movie.xpath('.//div[@class="hd"]//span/text()').extract_first()
            item['star'] = movie.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item['evaluate'] = movie.xpath('.//div[@class="star"]/span/text()').extract()[-1]
            item['describe'] = movie.xpath('.//p[@class="quote"]/span/text()').extract_first()
            # 每次返回道pipeline中
            yield item

        # 解析下一页
        next_url = response.xpath('//span[@class="next"]//a/@href').extract()
        if next_url:
            next_url = next_url[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_url, callback=self.parse)



