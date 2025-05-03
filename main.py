import socket
from datetime import datetime

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_IP, SERVER_PORT))

server_socket.listen(5)

print(f"[{datetime.now()}] SERVER IS LISTENING ON {SERVER_IP}:{SERVER_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    print(request)

    headers = request.split("\n")
    http_method = headers[0].split(" ")[0]
    http_path = headers[0].split(" ")[1]

    if http_method != "GET":
        response = "HTTP/1.1 405 METHOD NOT ALLOWED\n\n"
        client_socket.sendall(response.encode())
        client_socket.close()
        continue

    match http_path:
        case "/":
            fin = open("index.html")
            content = fin.read()
            response = "HTTP/1.1 200 OK\n\n" + content
        case "/menu":
            fin = open("menu.json")
            content = fin.read()
            response = "HTTP/1.1 200 OK\n\n" + content
        case _:
            fin = open("404.html")
            content = fin.read()
            response = "HTTP/1.1 404 NOT FOUND\n\n" + content
    client_socket.sendall(response.encode())
    client_socket.close()
