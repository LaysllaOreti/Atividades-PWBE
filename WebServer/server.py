import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/": "index.html",
            "/login": "login.html",
            "/cadastro": "cadastro.html",
            "/listarFilmes": "listarFilmes.html"
        }

        file_path = routes.get(self.path, None)
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, f"Arquivo {file_path} não encontrado!")
        else:
            # Se a rota não estiver definida, usa o comportamento padrão
            super().do_GET()

def main():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server Running at http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
