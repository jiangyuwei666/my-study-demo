"""
启动类
在pycharm里打开终端输入 
python main.py < test.txt > test.html
就能运行程序
"""

from markup import *
from handlers import *
import sys

handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)
