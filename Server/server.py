import socket
import threading
import os

def handle_client(client_socket):
    try:
        client_socket.send(b"220 Welcome to FTP server\r\n")
        current_dir = os.getcwd()
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            print("Received:", data)
            command_parts = data.split()
            if len(command_parts) == 0:
                client_socket.send(b"500 Empty command\r\n")
                continue
            command = command_parts[0].upper()
            if command == "LIST":
                files = os.listdir(current_dir)
                client_socket.send("\r\n".join(files).encode() + b"\r\n")
            elif command == "RETR":
                if len(command_parts) < 2:
                    client_socket.send(b"500 Missing filename\r\n")
                    continue
                filename = command_parts[1]
                if os.path.exists(os.path.join(current_dir, filename)):
                    with open(os.path.join(current_dir, filename), "rb") as file:
                        while True:
                            file_data = file.read(1024)
                            if not file_data:
                                break
                            client_socket.send(file_data)
                    client_socket.send(b"\r\n")
                else:
                    client_socket.send(b"550 File not found\r\n")
            elif command == "STOR":
                if len(command_parts) < 2:
                    client_socket.send(b"500 Missing filename\r\n")
                    continue
                filename = command_parts[1]
                with open(os.path.join(current_dir, filename), "wb") as file:
                    while True:
                        file_data = client_socket.recv(1024)
                        if not file_data:
                            break
                        file.write(file_data)
                client_socket.send(b"226 File transferred successfully\r\n")
            elif command == "CD":
                if len(command_parts) < 2:
                    client_socket.send(b"500 Missing directory name\r\n")
                    continue
                directory = command_parts[1]
                new_dir = os.path.join(current_dir, directory)
                if os.path.isdir(new_dir):
                    current_dir = new_dir
                    client_socket.send(b"250 Directory changed successfully\r\n")
                else:
                    client_socket.send(b"550 Directory not found\r\n")
            else:
                client_socket.send(b"500 Unknown command\r\n")
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3000))
    server_socket.listen(10)
    print("FTP server started on port 3000...")
    while True:
        client_socket, _ = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
