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
    user_info_query = 'allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    # 关注的人页面请求的接口url和参数
    follows_url = 'https://www.zhihu.com/api/v4/members/{user_token}/followees?include={include}&limit={limit}&offset={offset}'
    follows_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    # 关注者的页面请求接口url和参数
    followers_url = 'https://www.zhihu.com/api/v4/members/{user_token}/followers?include={followers_url}&offset={offset}&limit={limit}'
    followers_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    # 起始user
    start_user = 'excited-vczh'
    # 测试api接口url
    test_url = 'https://www.zhihu.com/api/v4/members/su-jia-30-86/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'

    # 第一次的请求
    def start_requests(self):
        # # 生成返回 个人信息 界面解析请求
        # yield scrapy.Request(url=self.user_info_url.format(user_token=self.start_user, include=self.user_info_query), callback=self.parse_user)
        # # 生成返回 我的关注 界面解析请求
        # yield scrapy.Request(url=self.follows_url.format(user_token=self.start_user, include=self.follows_query, offset=20, limit=20), callback=self.parse_follow)
        # # 生成返回 关注我的人 界面的解析请求
        # yield scrapy.Request(url=self.followers_url.format(user_token=self.start_user, include=self.followers_query, offset=20, limit=20), callback=self.parse_follower)
        yield scrapy.Request(url=self.test_url, callback=self.parse_test)

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

    # 关注的人界面的解析方法
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

    # 关注者界面（跟关注的人界面相似）
    def parse_follower(self, response):
        pass

    # 测试api接口是否可用的
    def parse_test(self, response):
        follow_result = json.loads(response.text)
        if 'data' in follow_result.keys():
            print("***")
            for i in follow_result.get('data'):
                print(i.get('name'))
        if 'paging' in follow_result.keys():
            if follow_result.get('paging').get('is_end') is False:
                yield scrapy.Request(url=follow_result.get('paging').get('next').replace('https://www.zhihu.com/', 'https://www.zhihu.com/api/v4/'), callback=self.parse_test)






