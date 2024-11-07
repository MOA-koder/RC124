import socket
import select
import sys

def chat_client(host, port):
    # Criação do socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexão com servidor
        client_socket.connect((host, int(port)))
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        sys.exit(-1)

    print(f"A conectar ao servidor {host}:{port}. \n === Agora você já pode começar a enviar mensagens ===\n")

    while True:
        sockets_list = [sys.stdin, client_socket]
        
        read_sockets, _, _ = select.select(sockets_list, [], [])
        
        for sock in read_sockets:
            
            if sock == client_socket:
                message = sock.recv(4096)
                if not message:
                    print("\nConexão encerrada pelo servidor.")
                    sys.exit(0)
                else:
                    sys.stdout.write(message.decode('utf-8'))
                    sys.stdout.flush()
            
            else:
                message = sys.stdin.readline()
                if message:
                    client_socket.send(message.encode('utf-8'))
                else:
                    print("\nA sair do chat...")
                    client_socket.close()
                    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso correto: python chat-client.py <hostname> <porta>")
        sys.exit(-1)
    
    chat_client(sys.argv[1], sys.argv[2])
