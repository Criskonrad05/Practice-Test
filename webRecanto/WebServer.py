import socket
import os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 8080)) # Escuta na porta 8080
serverSocket.listen(1)

print("Servidor pronto na porta 8080...")

while True:
    connectionSocket, addr = serverSocket.accept()
    try:
        # Recebe a requisição do navegador (cliente)
        message = connectionSocket.recv(1024).decode()
        # Pega o nome do arquivo da requisição GET
        filename = message.split()[1]
        
        # Remove a barra inicial para abrir o arquivo
        filepath = filename[1:]
        
        # Se a requisição for apenas '/', serve o index.html por padrão
        if filepath == "":
            filepath = "index.html"
            
        # Verifica se o arquivo existe
        if os.path.exists(filepath):
            f = open(filepath, 'rb') # Abre o arquivo em modo binário
            outputdata = f.read()
            f.close()
            
            # Determina o Content-Type com base na extensão do arquivo
            if filepath.endswith('.html'):
                content_type = 'text/html'
            elif filepath.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'application/octet-stream' # Tipo genérico para outros arquivos
            
            # Monta a resposta HTTP 200 OK
            header = f'HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n'
            connectionSocket.send(header.encode('utf-8'))
            connectionSocket.send(outputdata)

        else:
            # Monta a resposta HTTP 404 Not Found se o arquivo não existir
            header = 'HTTP/1.1 404 Not Found\n\n'
            body = '<html><body><h1>404 Not Found</h1></body></html>'
            connectionSocket.send(header.encode('utf-8'))
            connectionSocket.send(body.encode('utf-8'))
            
    except IndexError:
        # Lida com requisições inválidas ou vazias
        pass
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        
    connectionSocket.close()
