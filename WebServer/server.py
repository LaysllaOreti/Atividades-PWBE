import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

class MyHandler(SimpleHTTPRequestHandler):

    # Verifica se o usuário existe e faz o login
    def accont_user(self, login, password):
        loga = "laysllaeduarda@gmail.com"
        senha = "1008"
        
        if login == loga and password == senha:
            print("Usuário logado!") 
            # Redireciona para a página de cadastro de filmes após o login
            self.send_response(303)
            self.send_header('Location', '/cadastro_filmes')
            self.end_headers()
        else:
            print("Usuário não existe!") 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Usuário não existe".encode('utf-8'))
    
    # Trata requisições GET (rotas de páginas e API)
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API: retorna todos os filmes
        if path == '/api/filmes':
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

        # API: retorna filme específico pelo índice
        if path.startswith('/api/filmes/'):
            try:
                movie_index = int(path.split('/')[-1])  # Pega o índice da URL
                with open("filmes.json", "r", encoding="utf-8") as f:
                    movies = json.load(f)
                    if 0 <= movie_index < len(movies):
                        self.send_response(200)
                        self.send_header("Content-type", "application/json; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(json.dumps(movies[movie_index], ensure_ascii=False).encode('utf-8'))
                    else:
                        self.send_error(404, "Filme não encontrado")
            except (ValueError, FileNotFoundError, json.JSONDecodeError):
                self.send_error(400, "Requisição inválida")
            return

        # Rotas de páginas HTML e CSS
        routes = {
            "/login": "login.html",
            "/cadastro_filmes": "cadastro_filmes.html",
            "/listar_filmes": "listar_filmes.html",
            "/editar_filme": "editar_filme.html",
            "/style.css": "style.css",
        }
        
        if path in routes:
            file_path = os.path.join(os.getcwd(), routes[path])
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "Arquivo não encontrado")
        else:
            super().do_GET()

    # Trata requisições POST (login e cadastro de filmes)
    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email', [""])[0]
            password = form_data.get('senha', [""])[0]
            
            # Valida o login
            self.accont_user(login, password)
            return

        elif self.path == '/send_cadastro':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)
            
            # Novo filme vindo do formulário
            new_movie = {
                'nomeFilme': form_data.get('nomeFilme', [""])[0],
                'atores': form_data.get('atores', [""])[0],
                'diretor': form_data.get('diretor', [""])[0],
                'ano': form_data.get('ano', [""])[0],
                'genero': form_data.get('genero', [""])[0],
                'produtora': form_data.get('produtora', [""])[0],
                'sinopse': form_data.get('sinopse', [""])[0],
            }
            
            # Lê JSON, adiciona filme e salva
            try:
                with open("filmes.json", "r", encoding="utf-8") as f:
                    movies = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                movies = []
            
            movies.append(new_movie)

            with open("filmes.json", "w", encoding="utf-8") as f:
                json.dump(movies, f, indent=4, ensure_ascii=False)
            
            print("Novo Filme Cadastrado:")
            print(new_movie)
            
            # Redireciona para listagem
            self.send_response(303)
            self.send_header('Location', '/listar_filmes')
            self.end_headers()
            
        else:
            super().do_POST()

    # Trata requisições DELETE (remove filmes pelo índice)
    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/api/filmes/'):
            try:
                movie_index = int(parsed_path.path.split('/')[-1])  # Índice do filme
                
                with open("filmes.json", "r+", encoding="utf-8") as f:
                    movies = json.load(f)
                    
                    if 0 <= movie_index < len(movies):
                        deleted_movie = movies.pop(movie_index)  # Remove filme
                        
                        f.seek(0)
                        json.dump(movies, f, indent=4, ensure_ascii=False)
                        f.truncate()
                        
                        print(f"Filme deletado: {deleted_movie['nomeFilme']}")
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"message": "Filme deletado com sucesso"}).encode('utf-8'))
                    else:
                        self.send_error(404, "Índice de filme não encontrado")
            except (ValueError, FileNotFoundError, json.JSONDecodeError):
                self.send_error(400, "Requisição inválida ou arquivo não encontrado")
        else:
            self.send_error(404, "Recurso não encontrado")

    # Trata requisições PUT (atualiza filmes pelo índice)
    def do_PUT(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/api/filmes/'):
            try:
                movie_index = int(parsed_path.path.split('/')[-1])  # Índice do filme
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode('utf-8')
                updated_data = json.loads(body)
                
                with open("filmes.json", "r+", encoding="utf-8") as f:
                    movies = json.load(f)
                    
                    if 0 <= movie_index < len(movies):
                        movies[movie_index].update(updated_data)  # Atualiza dados
                        
                        f.seek(0)
                        json.dump(movies, f, indent=4, ensure_ascii=False)
                        f.truncate()
                        
                        print(f"Filme atualizado: {movies[movie_index]['nomeFilme']}")
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"message": "Filme atualizado com sucesso"}).encode('utf-8'))
                    else:
                        self.send_error(404, "Índice de filme não encontrado")
            except (ValueError, FileNotFoundError, json.JSONDecodeError):
                self.send_error(400, "Requisição inválida")
        else:
            self.send_error(404, "Recurso não encontrado, veja lista de filmes")

# Inicia o servidor HTTP
def main():
    server_address =('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
