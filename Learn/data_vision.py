from pymongo import MongoClient
import json
from pyecharts import WordCloud

local = 'localhost'
port = 27017
client = MongoClient(host=local, port=port)
db = client['tutorial']
collection = db['QuotesItem']

result = collection.find()
authors = []
author_dict = {}
tags_dict = {}
for i in result:
    if i.get('author') in author_dict.keys():
        author_dict[i.get('author')] += 1
    else:
        author_dict[i.get('author')] = 1
    for tag in i.get('tags'):
        if tag in tags_dict.keys():
            tags_dict[tag] += 1
        else:
            tags_dict[tag] = 1

w = WordCloud(width=1200, height=900)
w.add('quotes', author_dict.keys(), author_dict.values(), word_size_range=[20, 100])
w.render('quotes.html')
word = WordCloud(width=900, height=600)
word.add('tags', tags_dict.keys(), tags_dict.values(), shape='pentagon')
word.render('tags.html')

