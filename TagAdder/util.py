"""
获取文本内容
"""
def lines(file):
    """
    文本最后一行为空行
    先通过循环用yield返回所有内容，最后再多返回一个换行符\n
    :param file:
    :return:
    """
    for line in file:
        yield line
    yield "\n"

def blocks(file):
    """
    把每一段作为一个元素放入列表中
    :param file:
    :return:
    """
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield "".join(block).strip()
            block = []


