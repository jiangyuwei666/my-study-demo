# -*- coding: utf-8 -*-
import json

import scrapy

from ZhihuUser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 个人信息请求接口的url和参数
    user_info_url = 'https://www.zhihu.com/api/v4/members/{user_token}?include={include}'
    user_info_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    # 关注者页面请求的接口url和参数
    follows_url = 'https://www.zhihu.com/api/v4/members/{user_token}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    # 测试user
    start_user = 'excited-vczh'

    # 第一次的请求
    def start_requests(self):
        # 生成返回 个人信息 界面解析请求
        yield scrapy.Request(url=self.user_info_url.format(user_token=self.start_user, include=self.user_info_query), callback=self.parse_user)
        # 生成返回 我的关注 界面解析请求
        yield scrapy.Request(url=self.follows_url.format(user_token=self.start_user, include=self.follows_query, offset=0, limit=20), callback=self.parse_follow)

    # 个人信息的解析方法
    def parse_user(self, response):
        user_result = json.loads(response.text)
        item = UserItem()
        # 因为设置好的item对象的变量名与请求到的json数据名称一致，所以直接将item遍历一次
        # 然后如果在返回的json结果里有这样一个变量，就对其进行赋值
        for field in item.fields:
            if field in user_result.keys():
                item[field] = user_result.get(field)
        yield item
        # 返回所有关注的人的关注列表的请求到队列中
        # yield scrapy.Request(url=self.follows_url.format(user_token=user_result.get('url_token'), include=self.follows_query, offset=0, limit=20), callback=self.parse_follow)

    # 关注界面的解析方法
    def parse_follow(self, response):
        follow_result = json.loads(response.text)
        # 查找当前页所有关注者的关注页面并获取url_token
        if 'data' in follow_result.keys():
            for i in follow_result.get('data'):
                # 返回每个关注的同学的关注界面的请求
                yield scrapy.Request(url=self.user_info_url.format(user_token=i.get('url_token'), include=self.user_info_query), callback=self.parse_user)
        # 查看是否有下一页的的关注者，有就将下一页的请求返回队列
        if 'paging' in follow_result.keys():
            if follow_result.get('paging').get('is_end') is False:
                yield scrapy.Request(url=follow_result.get('paging').get('next'), callback=self.parse_follow)




