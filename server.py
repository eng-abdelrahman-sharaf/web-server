#NOTE - Kindly Don't Use A Good Browser for testing
import re, os, socket

def get_file_path( file_name , ext = ".html" , dir = "./files") -> str:
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file == file_name+ext:
                return os.path.join(dir, file)
    return None

def find_file(HTTP_request , method) -> str:
    file = re.findall(  fr"(?<={method} \/).*?(?= HTTP)", HTTP_request )[0]
    return file

def content_to_HTTP(content , found = True) -> str:
        return f'HTTP/1.1 {"200 OK" if found else "404 NOT Found"}\r\n\
        Content-Type: text/html; charset=UTF-8\r\n\r\n\
        {content}'

def HTTP_to_content(HTTP):
    return re.findall( r"(?<=\r\n\r\n)[\s\S]*", HTTP)[0]

def HTTP_type(HTTP):
    return HTTP[:HTTP.find(" ")]

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
    
    request = client_socket.recv(32768).decode('utf-8')

    method = HTTP_type(request)
    if(method == "GET"):
        file = find_file(request , method)
        file_path = get_file_path(file)
        # print(file_path)
        if(file_path == None):
            HTTP_response = content_to_HTTP("<h1>404 Not Found</h1>", False)
            client_socket.sendall(HTTP_response.encode('utf-8'))
            continue
        with open(file_path, "r") as file:
            content = file.read()
            # print(content)
            HTTP_response = content_to_HTTP(content)
            client_socket.sendall(HTTP_response.encode('utf-8'))

    elif(method == "POST"):
        file = find_file(request , method)
        content = HTTP_to_content(request)
        file_path = os.path.join("./files", file+".html")
        with open(file_path, "w") as file:
            file.write(content)
        HTTP_response = content_to_HTTP("<h1>File Created</h1>")


    client_socket.close()
    