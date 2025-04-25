import socket
import threading
import sys

def redirect_traffic(source_port, target_port):
    # Criar socket para a porta de origem
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Vincular à porta de origem
        server_socket.bind(('', source_port))
        server_socket.listen(5)
        print(f'Redirecionador ativo: porta {source_port} -> {target_port}')
        
        while True:
            # Aceitar conexão
            client_socket, client_address = server_socket.accept()
            print(f'Nova conexão de {client_address[0]}:{client_address[1]}')
            
            # Criar socket para a porta de destino
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect(('localhost', target_port))
            
            # Criar threads para redirecionar o tráfego em ambas as direções
            threading.Thread(target=forward_traffic, args=(client_socket, target_socket)).start()
            threading.Thread(target=forward_traffic, args=(target_socket, client_socket)).start()
            
    except Exception as e:
        print(f'Erro: {str(e)}')
        server_socket.close()
        sys.exit(1)

def forward_traffic(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.send(data)
    except:
        pass
    finally:
        source.close()
        destination.close()

if __name__ == '__main__':
    # Redirecionar da porta 80 para a porta 8000
    redirect_traffic(80, 8000) 