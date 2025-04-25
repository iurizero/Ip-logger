from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import sqlite3
from datetime import datetime
import socket

# Inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('localizacoes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS localizacoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  latitude REAL,
                  longitude REAL,
                  timestamp TEXT,
                  ip TEXT,
                  user_agent TEXT)''')
    conn.commit()
    conn.close()

class LocationHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/localizacoes':
            try:
                conn = sqlite3.connect('localizacoes.db')
                c = conn.cursor()
                c.execute('SELECT * FROM localizacoes')
                localizacoes = c.fetchall()
                conn.close()

                # Converter para lista de dicionários
                result = []
                for loc in localizacoes:
                    result.append({
                        'id': loc[0],
                        'latitude': loc[1],
                        'longitude': loc[2],
                        'timestamp': loc[3],
                        'ip': loc[4],
                        'user_agent': loc[5]
                    })

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                print(f'Erro ao buscar localizações: {str(e)}')
                self.send_error(500, 'Erro interno do servidor')
                return
                
        elif self.path == '/dados':
            try:
                conn = sqlite3.connect('localizacoes.db')
                c = conn.cursor()
                c.execute('SELECT * FROM localizacoes ORDER BY timestamp DESC LIMIT 10')
                localizacoes = c.fetchall()
                conn.close()

                # Formato diferente de retorno
                result = {
                    'total_registros': len(localizacoes),
                    'ultimas_localizacoes': [
                        {
                            'coordenadas': f"{loc[1]}, {loc[2]}",
                            'data_hora': loc[3],
                            'dispositivo': loc[5]
                        } for loc in localizacoes
                    ]
                }

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
                return
            except Exception as e:
                print(f'Erro ao buscar dados: {str(e)}')
                self.send_error(500, 'Erro interno do servidor')
                return

        # Servir o arquivo index.html para qualquer outra requisição GET
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
                timestamp = datetime.now().isoformat()
                ip = self.client_address[0]
                user_agent = self.headers.get('User-Agent', 'Desconhecido')
                
                # Salva no banco de dados
                conn = sqlite3.connect('localizacoes.db')
                c = conn.cursor()
                c.execute('''INSERT INTO localizacoes 
                            (latitude, longitude, timestamp, ip, user_agent)
                            VALUES (?, ?, ?, ?, ?)''',
                         (data['latitude'], data['longitude'], timestamp, ip, user_agent))
                conn.commit()
                conn.close()
                
                print("Localização salva com sucesso")
                
                # Responde com sucesso
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
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
    # Inicializar o banco de dados
    init_db()
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor rodando em http://localhost:{port}')
    print('Pressione Ctrl+C para parar o servidor')
    httpd.serve_forever()

if __name__ == '__main__':
    run()