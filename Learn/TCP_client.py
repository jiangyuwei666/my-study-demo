import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#初始化Socket
s.connect(('10.0.117.116',9999))#连接的IP和端口
print('-->>'+s.recv(1024).decode('utf-8'))#输出服务端第一次发送过来的消息（hello,im server）
s.send(b'hello,im client')#第一次发送的消息
print('-->>'+s.recv(1024).decode('utf-8'))#输出服务端第二次发送过来的消息（loop_msg:）
while(True):
    msg = input('客户端发送的信息：')
    if 'exit' == msg :
        s.send(b'exit')
        break
    s.send( msg.encode('utf-8') )
s.close()#关闭socket