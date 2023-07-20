import cv2
import pickle
import socket
import struct

# 创建socket连接
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_ip = '192.168.1.112'
print('客户端 IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# 连接到服务器
client_socket.connect(socket_address)
print('服务器连接成功')

# 使用摄像头捕获视频流
cap = cv2.VideoCapture(0)

# 持续获取视频帧并发送给服务端
while True:
    ret, frame = cap.read()
    serialized_data = pickle.dumps(frame)

                # 获取数据大小并进行打包
    data_size = len(serialized_data)
    packed_data_size = struct.pack("Q", data_size)

                            # 发送数据大小及帧数据给服务端
    client_socket.sendall(packed_data_size + serialized_data)

cap.release()
client_socket.close()
