import socket
import threading
import time
def dealClient(sock , addr):
    print( 'Accept new connection from %s:%s...' %addr )
    sock.send(b'hello,im server')#可以看出发送的时候都是用的字节串
    while True:
        data = sock.recv(1024)#接受TCP套字的数据，数据以字符串的形式返回，1024表示可以接受的最大的数据量字节数
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit' :
            break
        print('-->>%s!' %data.decode('utf-8'))#将字符串先进行解码得到我们看得懂的字符串
        sock.send(('loop_msg:%s!'%data.decode('utf-8')).encode('utf-8'))#发送的时候，把需要发送的内容先进行编码，得到字节串然后发送出去
    sock.close()#关闭socket
    print('Connection from %s:%s closed' % addr)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建一个socket，AF_INET是使用IPv4进行服务器之间的网络通信；SOCK_STREAM流式socket，用于TCP；这两个用来参数用来创建TCP socket
    s.bind(('10.0.117.116',9999))#socket 绑定本机的IP与端口
    #监听连接
    s.listen(5)#5是最大监听数量，至少为1
    print('waiting for connection...')
    while True:#这个循环表示一直在监听，不断的接受客户端的请求，只要有新的连接就会被捕捉到进行下一次循环（由上面知道，最多有5个）
        #接受一个新的连接
        sock , addr = s.accept()#返回一个新的socket对象以及ip地址(返回的应该是个元组，后面才能实现打印)
        t = threading.Thread(target=dealClient , args=(sock,addr))#开一个新的线程z执行dealClient方法，来处理TCP连接
        t.start()#线程开始工作
