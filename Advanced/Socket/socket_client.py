import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))
client.send("jiangyuwei".encode("utf8"))
while True:
    data = client.recv(1024)
    print(data.decode('utf8'))
    s = input()
    client.send(s.encode("utf8"))
    if s == "exit":
        break


client.close()
