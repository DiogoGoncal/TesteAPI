import csv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class ServidorCSV(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/buscar"):
            # Extrai parâmetros da URL
            query_params = parse_qs(urlparse(self.path).query)
            razao_social = query_params.get("razao", [""])[0].lower()
            modalidade = query_params.get("modalidade", [""])[0].lower()

            # Lê o arquivo CSV
            arquivo_csv = 'server/Relatorio_cadop.csv'
            dados_encontrados = []

            with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile, delimiter=';')
                for row in leitor:
                    # Verifica se a razão social contém o termo buscado
                    if razao_social in row["Razao_Social"].lower():
                        # Aplica o filtro de modalidade, se selecionado
                        if not modalidade or modalidade == row["Modalidade"].lower():
                            dados_encontrados.append(row)

            # Configura cabeçalhos CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Retorna os dados filtrados
            self.wfile.write(json.dumps(dados_encontrados, ensure_ascii=False).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=ServidorCSV, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
