#!/usr/bin/python3
import socket
import os
import signal
import sys
import struct
import logging
import time
import datetime

'''
class NanoSecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
        s = "%s,%09d" % (t, record.msecs * 1000000)
        return s

# 로그 설정
formatter = NanoSecondFormatter(fmt='[VSimul][%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
'''

class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = datetime.datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            t = datetime.datetime.fromtimestamp(record.created)
            s = t.strftime("%Y-%m-%d %H:%M:%S")
            s = f"{s},{int(record.msecs):06d}"
        return s

# 로그 설정
formatter = MillisecondFormatter(fmt='[VSimul][%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# Unix domain socket 경로
#socket_path = "/home/jhshin/work/morai/uds_vehicle_accel"
socket_path = "/home/jhshin/work/morai/uds_location"

def cleanup_and_exit(signum, frame):
    """신호를 처리하고 소켓 파일을 삭제한 후 종료"""
    if os.path.exists(socket_path):
        os.remove(socket_path)
    logger.info("Server shutting down gracefully")
    sys.exit(0)

def main():
    # 기존 소켓 파일이 존재하면 삭제
    if os.path.exists(socket_path):
        os.remove(socket_path)

    # 신호 처리기 등록
    signal.signal(signal.SIGINT, cleanup_and_exit)
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    # 소켓 생성
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(socket_path)
    server_socket.listen(1)
    logger.info("Server is listening")

    while True:
        try:
            # 클라이언트 연결 수락
            conn, _ = server_socket.accept()
            logger.info("Client connected")

            while True:
                data = conn.recv(12)  # 3개의 float 값 (4 bytes each)
                if not data:
                    break
                unpacked_data = struct.unpack('fff', data)
                logger.info(f"Received: {unpacked_data}")
            conn.close()
            logger.info("Client disconnected")
        except socket.error as e:
            logger.info(f"Socket error: {e}")
            break

    server_socket.close()
    if os.path.exists(socket_path):
        os.remove(socket_path)

if __name__ == "__main__":
    main()
