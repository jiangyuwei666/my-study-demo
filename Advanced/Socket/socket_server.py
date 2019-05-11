import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8000))
server.listen()

# 获取冲客户端发送的数据
while True:
    sock, addr = server.accept()
    data = sock.recv(1024)  # 一次获取1024个字节(1k)
    if data.decode('utf8') == 'exit':
        break
    print(data.decode("utf8"))
    s = input()
    sock.send(s.encode('utf8'))
sock.close()
server.close()
