"""
因为要取第一个，考虑到字典是无序的，这里采用有序字典来左
"""

from collections import OrderedDict


def get_once(arr):
    dd = OrderedDict()
    for i in arr:
        if i in dd.keys():
            dd[i] += 1
        else:
            dd[i] = 1

    for i in dd.keys():
        if dd[i] == 1:
            print(i)
            break


get_once(list('ajsidofdoifgjdfkjoibxgfioyfhgqwfweedthtreyhudfighoofsljgiosdfgnsfjkdgkjsijoogjfsk'))  # a
get_once(list('jsidofdoifgjdfksljgczjkoijjoioijzljkojzoojjoifjzokovbzojvcbioasdfgnsfjkdgkjsijoogjfsk'))  # a
get_once(list(
    'jsidofdoifgjmdfzkfbjpoijdfojkbkclvopvkbjzoidfbjzodfbjoidkzjfbiojodcknhmdfnhdkojksljgiosdfgnsfjkdgkjsijoogjfska'))  # a
