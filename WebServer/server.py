import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
            return None
        except FileNotFoundError:
            return super().list_directory(path)

    def account_user(self, login, password):
        loga = "laysllaeduarda@gmail.com"
        senha = "1008"

        if login == loga and password == senha:
            self.send_response(303)
            self.send_header("Location", "/cadastro_filmes")
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Usuário Não Existe".encode("utf-8"))

    def do_GET(self):
        if self.path == '/api/filmes':
            try:
                with open("filmes.json", "r", encoding="utf-8") as f:
                    data = f.read()
            except FileNotFoundError:
                data = "[]"

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(data.encode("utf-8"))
            return

        routes = {
            "/login": "login.html",
            "/cadastro_filmes": "cadastro_filmes.html",
            "/listar_filmes": "listar_filmes.html",
        }

        if self.path in routes:
            file_path = os.path.join(os.getcwd(), routes[self.path])
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "Arquivo não encontrado")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email', [""])[0]
            password = form_data.get('senha', [""])[0]

            print("Tentativa de login:", login)
            self.account_user(login, password)
            return

        elif self.path == '/cadastro_filme':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            titulo = form_data.get('titulo', [""])[0]
            atores = form_data.get('atores', [""])[0]
            diretor = form_data.get('diretor', [""])[0]
            ano = form_data.get('ano', [""])[0]
            genero = form_data.get('genero', [""])[0]
            produtora = form_data.get('produtora', [""])[0]
            sinopse = form_data.get('sinopse', [""])[0]

            filme = {
                "titulo": titulo,
                "atores": atores,
                "diretor": diretor,
                "ano": ano,
                "genero": genero,
                "produtora": produtora,
                "sinopse": sinopse
            }

            print("Cadastrando filme:", filme)

            # se o arquivo estiver vazio ou corrompido
            if os.path.exists("filmes.json"):
                try:
                    with open("filmes.json", "r", encoding="utf-8") as f:
                        filmes = json.load(f)
                except json.JSONDecodeError:
                    print("Arquivo filmes.json está vazio ou inválido. Inicializando lista vazia.")
                    filmes = []
            else:
                filmes = []

            filmes.append(filme)

            with open("filmes.json", "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            self.send_response(303)
            self.send_header("Location", "/listar_filmes")
            self.end_headers()
            return

        else:
            super().do_POST()


def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
