import socket
import threading

HOST = '0.0.0.0'
PORT = 5000
clients = []

def Handle_Client(Client_socket, addr):
    print(f"[+] New connection from {addr}")
    while True:
        try:
            message = Client_socket.recv(1024).decode()
            if message:
                print(f"{addr}: {message}")
                broadcast(message, Client_socket)
            else:
                remove_client(Client_socket)
                break
        except:
            remove_client(Client_socket)
            break

def broadcast(message, Sender_socket):
    for client in clients:
        if client != Sender_socket:
            try:
                client.send(message.encode())
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Server listening on {HOST}, {PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=Handle_Client, args=(client_socket, addr)).start()

#  This is REQUIRED to start the server
if __name__ == '__main__':
    main()
