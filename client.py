import socket
import os

def connect_to_server(host, port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def get_req(client_socket, save_path, file_name):
    request = f"GET /{file_name} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    header, body = response.split('\r\n\r\n', 1)

    if "200 OK" in header:
        print("File received successfully.")
        with open(save_path, 'w') as f:
            f.write(body)
        print(f"Saved file as {save_path}")
    elif "404 Not Found" in header:
        print("Error: File not found on the server.")

def post_req(client_socket, file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    with open(file_path, 'r') as f:
        file_content = f.read()

    request = (f"POST /{os.path.splitext(os.path.basename(file_path))[0]} HTTP/1.1\r\n"
               f"Host: localhost\r\n"
               f"Content-Length: {len(file_content)}\r\n\r\n"
               f"{file_content}")

    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()

    if "200 OK" in response:
        print("File uploaded successfully.")
    else:
        print("Error uploading file.")

def close_connection(client_socket):
    client_socket.close()

def main():
    client_socket = connect_to_server(host='localhost', port=8080)

    while True:
        try:
            choice = input("Enter 'GET', 'POST', or 'exit': ").strip().lower()
            if choice == 'get':
                save_path = input("Enter the path where you want to save the file: ")
                file_name = input("Enter the file name to request from the server: ")
                get_req(client_socket, save_path, file_name)
            elif choice == 'post':
                file_path = input("Enter the file path to upload: ")
                post_req(client_socket, file_path)
            elif choice == 'exit':
                print("Closing connection...")
                close_connection(client_socket)
                break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
