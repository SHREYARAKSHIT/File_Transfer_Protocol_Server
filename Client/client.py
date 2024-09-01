import socket
import os

def main():
    server_ip = "localhost"
    server_port = 3000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    data = client_socket.recv(1024).decode()
    print(data)
    while True:
        try:
            command = input("Enter command (LIST/RETR/STOR/CD): ").strip().upper()
            if command == "RETR":
                filename = input("Enter filename to download: ").strip()
                command = f"{command} {filename}"
            elif command == "STOR":
                filename = input("Enter filename to upload: ").strip()
                if os.path.exists(filename):
                    command = f"{command} {filename}"
                else:
                    print("File does not exist.")
                    continue
            elif command == "CD":
                directory = input("Enter directory name to change: ").strip()
                command = f"{command} {directory}"

            client_socket.send(command.encode())

            if command.startswith("LIST"):
                data = client_socket.recv(1024).decode()
                print(data)
            elif command.startswith("RETR"):
                with open(filename, "wb") as file:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        if data.endswith(b"\r\n"):
                            file.write(data[:-2])
                            break
                        file.write(data)
                print("File downloaded successfully.")
            elif command.startswith("STOR"):
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            client_socket.send(data)
                    client_socket.send(b"\r\n")
                    print("File uploaded successfully.")
                else:
                    print("File does not exist.")
            elif command.startswith("CD"):
                response = client_socket.recv(1024).decode()
                print(response)
            else:
                print("Invalid command. Supported commands: LIST, RETR, STOR, CD")
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

if __name__ == "__main__":
    main()
