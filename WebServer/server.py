import os
import cgi
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

UPLOAD_DIR = "uploads"

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

    # verificação simples de login
    def accont_user(self, login, password):
        loga = "laysllaeduarda@gmail.com"
        senha = "1009"
        return login == loga and senha == password

    # requisições do tipo GET
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # API de filmes
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

        # rota para editar filme
        if path == '/editar_filme':
            query_params = parse_qs(parsed_path.query)
            titulo_para_editar = query_params.get('titulo', [None])[0]

            if not titulo_para_editar:
                self.send_error(400, "Título do filme não fornecido")
                return

            try:
                with open("filmes.json", "r", encoding="utf-8") as f:
                    filmes = json.load(f)

                filme_encontrado = next((f for f in filmes if f['titulo'] == titulo_para_editar), None)
                if not filme_encontrado:
                    self.send_error(404, "Filme não encontrado")
                    return

                with open("editar_filme.html", "r", encoding="utf-8") as f:
                    content = f.read()

                # preencher os valores do formulário
                for campo in ["titulo", "atores", "diretor", "ano", "genero", "produtora"]:
                    content = content.replace(f'name="{campo}"', f'name="{campo}" value="{filme_encontrado.get(campo, "")}"')

                content = content.replace(
                    '<textarea name="sinopse"></textarea>',
                    f'<textarea name="sinopse">{filme_encontrado.get("sinopse", "")}</textarea>'
                )

                # Exibir pré-visualização da capa
                capa = filme_encontrado.get("capa", "")
                if capa:
                    content = content.replace(
                        '</form>',
                        f'<p>Capa atual:</p><img src="{capa}" width="120"><br>'
                        f'<input type="hidden" name="capa_antiga" value="{capa}"></form>'
                    )
                else:
                    content = content.replace('</form>', '<input type="hidden" name="capa_antiga" value=""></form>')

                content = content.replace('</form>',
                    f'<input type="hidden" name="titulo_antigo" value="{titulo_para_editar}"></form>')

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))

            except FileNotFoundError:
                self.send_error(404, "Arquivo de filmes ou template não encontrado")
            return

        # rotas fixas
        routes = {
            "/login": "login.html",
            "/cadastro_filmes": "cadastro_filmes.html",
            "/listar_filmes": "listar_filmes.html",
            "/editar_filme": "editar_filme.html",
        }

        if path in routes:
            file_path = os.path.join(os.getcwd(), routes[path])
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

    # requisições do tipo POST
    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email', [""])[0]
            password = form_data.get('senha', [""])[0]

            if self.accont_user(login, password):
                self.send_response(303)
                self.send_header("Location", "/cadastro_filmes")
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Usuário ou senha inválidos".encode('utf-8'))
            return

        elif self.path == '/cadastro_filme':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            filme = {
                "titulo": form.getvalue("titulo", ""),
                "atores": form.getvalue("atores", ""),
                "diretor": form.getvalue("diretor", ""),
                "ano": form.getvalue("ano", ""),
                "genero": form.getvalue("genero", ""),
                "produtora": form.getvalue("produtora", ""),
                "sinopse": form.getvalue("sinopse", ""),
            }

            # upload da capa
            capa_field = form['capa'] if 'capa' in form else None
            if capa_field and capa_field.filename:
                if not os.path.exists(UPLOAD_DIR):
                    os.makedirs(UPLOAD_DIR)
                file_path = os.path.join(UPLOAD_DIR, capa_field.filename)
                with open(file_path, "wb") as f:
                    f.write(capa_field.file.read())
                filme["capa"] = "/" + file_path.replace("\\", "/")
            else:
                filme["capa"] = ""

            if os.path.exists("filmes.json"):
                with open("filmes.json", "r", encoding="utf-8") as f:
                    filmes = json.load(f)
            else:
                filmes = []

            filmes.append(filme)

            with open("filmes.json", "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            self.send_response(303)
            self.send_header("Location", "/listar_filmes")
            self.end_headers()

        elif self.path == '/delete_filme':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            titulo = form_data.get('titulo', [""])[0]

            try:
                with open("filmes.json", "r", encoding="utf-8") as f:
                    filmes = json.load(f)
            except FileNotFoundError:
                filmes = []

            filmes = [f for f in filmes if f['titulo'] != titulo]

            with open("filmes.json", "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Filme deletado')
            return

        elif self.path == '/editar_filme':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            titulo_antigo = form.getvalue("titulo_antigo", "")
            capa_antiga = form.getvalue("capa_antiga", "")

            novo_filme = {
                "titulo": form.getvalue("titulo", ""),
                "atores": form.getvalue("atores", ""),
                "diretor": form.getvalue("diretor", ""),
                "ano": form.getvalue("ano", ""),
                "genero": form.getvalue("genero", ""),
                "produtora": form.getvalue("produtora", ""),
                "sinopse": form.getvalue("sinopse", ""),
            }

            # upload da nova capa
            capa_field = form['capa'] if 'capa' in form else None
            if capa_field and capa_field.filename:
                if not os.path.exists(UPLOAD_DIR):
                    os.makedirs(UPLOAD_DIR)
                file_path = os.path.join(UPLOAD_DIR, capa_field.filename)
                with open(file_path, "wb") as f:
                    f.write(capa_field.file.read())
                novo_filme["capa"] = "/" + file_path.replace("\\", "/")
            else:
                novo_filme["capa"] = capa_antiga

            try:
                with open("filmes.json", "r", encoding="utf-8") as f:
                    filmes = json.load(f)

                filmes = [novo_filme if f['titulo'] == titulo_antigo else f for f in filmes]

                with open("filmes.json", "w", encoding="utf-8") as f:
                    json.dump(filmes, f, ensure_ascii=False, indent=4)

                self.send_response(303)
                self.send_header("Location", "/listar_filmes")
                self.end_headers()
            except FileNotFoundError:
                self.send_error(404, "Arquivo de filmes não encontrado")
            return

        else:
            super(MyHandle, self).do_POST()
            return


def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server running in http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
