import socket
import select
import sys

def broadcast_message(server_socket, client_socket, message, clients):
    """Envia a mensagem para todos os clientes, exceto o remetente."""
    for client in clients:
        if client != server_socket and client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def chat_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind(('', int(port)))

    server_socket.listen(1000)
    print(f"Servidor activo! O Servidor está a rodar na porta {port}")

    clients = [server_socket]

    while True:
        
        read_sockets, _, _ = select.select(clients, [], [])
        
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                clients.append(client_socket)
                print(f"Cliente {client_address} conectado")

                welcome_message = f"{client_address[0]}:{client_address[1]} Conectou-se ao chat!.\n"
                broadcast_message(server_socket, client_socket, welcome_message, clients)
            
            
            else:
                try:
                    message = sock.recv(4096)
                    if message:
                        client_address = sock.getpeername()
                        message_to_send = f"{client_address[0]}:{client_address[1]} {message.decode('utf-8')}"
                        broadcast_message(server_socket, sock, message_to_send, clients)
                    else:
                        client_address = sock.getpeername()
                        left_message = f"{client_address[0]}:{client_address[1]} Saiu da conversa!.\n"
                        broadcast_message(server_socket, sock, left_message, clients)
                        sock.close()
                        clients.remove(sock)
                except:
                    continue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso correcto: python chat-server.py <porta>")
        sys.exit(-1)
    
    chat_server(sys.argv[1])
