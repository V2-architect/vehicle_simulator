#include <iostream>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <csignal>
#include <cstring>

const char* socket_path = "/home/jhshin/work/morai/uds_vehicle_speed";
int server_socket = -1;

void cleanup_and_exit(int signum) {
    if (server_socket != -1) {
        close(server_socket);
    }
    unlink(socket_path);
    std::cout << "Server shutting down gracefully" << std::endl;
    exit(0);
}

int main() {
    // 기존 소켓 파일이 존재하면 삭제
    unlink(socket_path);

    // 신호 처리기 등록
    signal(SIGINT, cleanup_and_exit);
    signal(SIGTERM, cleanup_and_exit);

    // 소켓 생성
    server_socket = socket(AF_UNIX, SOCK_STREAM, 0);
    if (server_socket < 0) {
        std::cerr << "Failed to create socket" << std::endl;
        return 1;
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, socket_path, sizeof(addr.sun_path) - 1);

    if (bind(server_socket, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        std::cerr << "Failed to bind socket" << std::endl;
        close(server_socket);
        return 1;
    }

    if (listen(server_socket, 1) < 0) {
        std::cerr << "Failed to listen on socket" << std::endl;
        close(server_socket);
        return 1;
    }

    std::cout << "Server is listening" << std::endl;

    while (true) {
        int client_socket = accept(server_socket, nullptr, nullptr);
        if (client_socket < 0) {
            std::cerr << "Failed to accept client connection" << std::endl;
            continue;
        }

        std::cout << "Client connected" << std::endl;

        while (true) {
            float buffer[3];
            ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
            if (bytes_received <= 0) {
                break;
            }

            std::cout << "Received: " << buffer[0] << ", " << buffer[1] << ", " << buffer[2] << std::endl;
        }

        close(client_socket);
        std::cout << "Client disconnected" << std::endl;
    }

    close(server_socket);
    unlink(socket_path);
    return 0;
}
