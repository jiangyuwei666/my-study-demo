# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # id (可以和 type 拼成个人主页)
    id = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 头像地址
    avatar_url = scrapy.Field()
    # 个人简介
    headline = scrapy.Field()
    # url_token
    url_token = scrapy.Field()
    # 关注
    follower_count = scrapy.Field()
    # 回答问题数量
    answer_count = scrapy.Field()
    # 职业
    employments = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # type  一般都是people(可以与id拼成个人界面url)
    type = scrapy.Field()
    # url
    url = scrapy.Field()
    # 是否接收私信
    # 因为没有加cookies登陆，所以全是false
    allow_message = scrapy.Field()
    # 职业
    employments = scrapy.Field()



