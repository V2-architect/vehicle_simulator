#include <iostream>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <csignal>
#include <cstring>
#include <chrono>
#include <iomanip>
#include <sstream>

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

std::string get_current_time() {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    auto ms = std::chrono::duration_cast<std::chrono::microseconds>(now.time_since_epoch()) % 1000000;

    std::stringstream ss;
    ss << "[VSimul]["
       << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S")
       << "," << std::setw(6) << std::setfill('0') << ms.count() << "]";
    return ss.str();
}

void log_message(const std::string& message) {
    std::cout << get_current_time() << " " << message << std::endl;
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
        log_message("Failed to create socket");
        return 1;
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, socket_path, sizeof(addr.sun_path) - 1);

    if (bind(server_socket, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        log_message("Failed to bind socket");
        close(server_socket);
        return 1;
    }

    if (listen(server_socket, 1) < 0) {
        log_message("Failed to listen on socket");
        close(server_socket);
        return 1;
    }

    log_message("Server is listening");

    while (true) {
        int client_socket = accept(server_socket, nullptr, nullptr);
        if (client_socket < 0) {
            log_message("Failed to accept client connection");
            continue;
        }

        log_message("Client connected");

        while (true) {
            float buffer[3];
            ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
            if (bytes_received <= 0) {
                break;
            }

            std::stringstream ss;
            ss << "Received: " << buffer[0] << ", " << buffer[1] << ", " << buffer[2];
            log_message(ss.str());
        }

        close(client_socket);
        log_message("Client disconnected");
    }

    close(server_socket);
    unlink(socket_path);
    return 0;
}
