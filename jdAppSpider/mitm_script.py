import json
from db import MongodbClient
from urllib.parse import unquote
import re
from mitmproxy import ctx

client1 = MongodbClient(db_name='jd', collection_name='comments')

# https://36.110.181.150

def response(flow):
    global client1
    # url = 'https://36.110.181.220'
    # if url in flow.request.url:
    #     info = ctx.log.warn
    #     text = flow.response.text
    #     data = json.loads(text)
    #     if data.get('wareInfo'):
    #         s = data.get('wareInfo')
    #         for i in s:
    #             info("********************")
    #             info("---------" + str(i.get('wname')))
    #             info("---------" + str(i.get('jdPrice')))
    #             info("********************")
    url = '36.110.181.220/client.action?functionId=getCommentListWithCard'
    url1 = '36.110.181.150/client.action?functionId=getCommentListWithCard'
    if url in flow.request.url or url1 in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        if data.get('commentInfoList'):
            s = data.get('commentInfoList')
            for i in s:
                ctx.log.warn("***************")
                ctx.log.warn(str(i.get('commentInfo').get('userNickName')))
                ctx.log.warn(str(i.get('commentInfo').get('commentData')))
                ctx.log.warn("***************")




