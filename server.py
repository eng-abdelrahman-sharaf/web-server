#NOTE - Kindly Don't Use A Good Browser for testing
import re, os, socket

def get_file_path( file_name , ext = ".html" , dir = "./files") -> str:
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file == file_name+ext:
                return os.path.join(dir, file)
    return None

def find_files(HTTP_request) -> list[str]:
    files = re.findall(  r"(?<=GET \/).*?(?= HTTP)", HTTP_request )
    return files

def content_to_HTTP(content , found = True) -> str:
        return f'HTTP/1.1 {"200 OK" if found else "404 NOT Found"}\n\
        Content-Type: text/html; charset=utf-8\n\n\
        {content}'


def init_server( HOST, PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on port {PORT}...")
    return server_socket

server_socket = init_server("localhost", 8080)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} has been established.")
    
    request = client_socket.recv(1024).decode('utf-8')

    files = find_files(request)
    
    for file in  files:
        file_path = get_file_path(file)
        print(file_path)
        if(file_path == None):
            HTTP_response = content_to_HTTP("<h1>404 Not Found</h1>", False)
            client_socket.sendall(HTTP_response.encode('utf-8'))
            continue
        with open(file_path, "r") as file:
            content = file.read()
            print(content)
            HTTP_response = content_to_HTTP(content)
            client_socket.sendall(HTTP_response.encode('utf-8'))
    client_socket.close()
    