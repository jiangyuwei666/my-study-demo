# -*- coding: utf-8 -*-
import json
from mitmproxy import ctx
from db import MongodbClient

mongodb = MongodbClient(db_name='test', collection_name='iGet')


def response(flow):
    global mongodb  # 使用全局变量
    url = 'https://dedao.igetget.com/v3/discover/bookList'
    if flow.request.url.startswith(url):  # 是否以上面这个字符串开头
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        ctx.log.warn(str(type(data)))
        for book in books:
            data = {
                'title': book.get('operating_title'),
                'author': book.get('book_author'),
                'cover': book.get('cover'),
                'summary': book.get('other_share_summary'),
                'price': book.get('price')
            }
            ctx.log.warn(str(data))

            # mongodb.collection.insert_one(data)

