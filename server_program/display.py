import cv2

import pickle
import socket
import struct
import numpy


# 创建socket连接
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('服务器 IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# 绑定socket地址
server_socket.bind(socket_address)

# 开始监听连接
server_socket.listen(5)
print("等待客户端连接...")

# 接受客户端连接
client_socket, addr = server_socket.accept()
print('连接地址:', addr)

# 持续接收并显示视频流
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K字节缓冲区大小
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # 反序列化并显示帧
    frame = pickle.loads(frame_data)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭连接
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()