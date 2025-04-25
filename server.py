from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from datetime import datetime
import socket

class LocationHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Servir o arquivo index.html para qualquer requisição GET
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/salvar-localizacao':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                print(f"Dados recebidos: {data}")
                
                # Adiciona informações extras
                data['timestamp'] = datetime.now().isoformat()
                data['ip'] = self.client_address[0]
                data['user_agent'] = self.headers.get('User-Agent', 'Desconhecido')
                
                # Carrega localizações existentes
                localizacoes = []
                if os.path.exists('localizacoes.json'):
                    with open('localizacoes.json', 'r', encoding='utf-8') as f:
                        localizacoes = json.load(f)
                
                # Adiciona nova localização
                localizacoes.append(data)
                
                # Salva no arquivo
                with open('localizacoes.json', 'w', encoding='utf-8') as f:
                    json.dump(localizacoes, f, indent=2, ensure_ascii=False)
                
                print(f"Localização salva com sucesso. Total: {len(localizacoes)}")
                
                # Responde com sucesso
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                # Garante que a resposta seja um JSON válido
                response_data = json.dumps({'success': True, 'message': 'Localização salva com sucesso'})
                self.wfile.write(response_data.encode('utf-8'))
                
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {str(e)}")
                self.send_error(400, 'Dados JSON inválidos')
            except Exception as e:
                print(f'Erro ao processar localização: {str(e)}')
                self.send_error(500, 'Erro interno do servidor')
            return
        
        return SimpleHTTPRequestHandler.do_POST(self)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=LocationHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor rodando em http://localhost:{port}')
    print('Pressione Ctrl+C para parar o servidor')
    httpd.serve_forever()

if __name__ == '__main__':
    run()