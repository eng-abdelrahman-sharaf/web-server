#NOTE - Kindly Don't Use A Good Browser for testing
import re, os, socket

def get_file_path( file_name , ext = ".html" , dir = "./ServerFiles") -> str:
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file == file_name+ext:
                return os.path.join(dir, file)
    return None

def find_end_of_keyword(string , keyword) -> int:
    return string.find(keyword) + len(keyword) - 1

def find_file(HTTP_request , method) -> str:
    file = re.findall(  fr"(?<={method} \/).*?(?= HTTP)", HTTP_request )[0]
    return file

def content_to_HTTP(content , success = True , include_content = True) -> str:
        return f'HTTP/1.1 {"200 OK" if success else "404 NOT Found"}\r\n\
        {"Content-Type: text/html; charset=UTF-8" if include_content else ""}\r\n\r\n\
        {content}'

def HTTP_to_content(HTTP):
    keyword = "\r\n\r\n"
    return HTTP[find_end_of_keyword(HTTP , keyword):]

def HTTP_type(HTTP):
    return HTTP[:HTTP.find(" ")]

def init_server( HOST, PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on port {PORT}...")
    return server_socket

def handle_get_request(client_socket, request):
    try:
        file = find_file(request, "GET")
        file_path = get_file_path(file)
        if file_path is None:
            send_response(client_socket, "<h1>404 Not Found</h1>", success=False)
            return
        with open(file_path, "r") as file:
            content = file.read()
            send_response(client_socket, content)
    except Exception as e:
        print(e)
        send_response(client_socket, "", success=False, include_content=False)

def handle_post_request(client_socket, request):
    try:
        file = find_file(request, "POST")
        content = HTTP_to_content(request)
        file_path = os.path.join("./ServerFiles", file + ".html")
        with open(file_path, "w") as file:
            file.write(content)
        send_response(client_socket, "", include_content=False)
    except Exception as e:
        print(e)
        send_response(client_socket, "", include_content=False)

def send_response(client_socket, content, success=True, include_content=True):
    HTTP_response = content_to_HTTP(content, success, include_content)
    client_socket.sendall(HTTP_response.encode('utf-8'))
    
def main():
    
    server_socket = init_server("localhost", 8080)
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        
        request = client_socket.recv(32768).decode('utf-8')
        # print(request)

        method = HTTP_type(request)
        if method == "GET":
            handle_get_request(client_socket, request)
        elif method == "POST":
            handle_post_request(client_socket, request)

        client_socket.close()

if __name__ == "__main__":
    main()