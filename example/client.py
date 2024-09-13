import socket
import os
import time

# Unix domain socket 경로
socket_path = "/home/jhshin/work/morai/uds_vehicle_speed"

def main():
    while True:
        # 소켓이 존재하는지 확인
        if os.path.exists(socket_path):
            try:
                # 소켓 생성
                client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client_socket.connect(socket_path)
                print("Connected to server")

                counter = 1
                while True:
                    try:
                        # 1초에 한번씩 숫자 전송
                        client_socket.sendall(str(counter).encode('utf-8'))
                        print(f"Sent: {counter}")
                        counter += 1
                        time.sleep(1)
                    except socket.error:
                        print("Server closed the connection")
                        break
                client_socket.close()
            except socket.error:
                print("Failed to connect to server")
        else:
            print("Waiting for server to open the socket")
        time.sleep(1)

if __name__ == "__main__":
    main()
