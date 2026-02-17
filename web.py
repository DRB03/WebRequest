from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        # 1. Caso: Ruta Raíz (Home)
        if self.url().path == '/':
            try:
                with open("home.html", "r", encoding="utf-8") as archivo:
                    html = archivo.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "Archivo home.html no encontrado")
        
        # 2. Caso: Ruta con Autor (Dinámico)
        elif self.valida_autor():
            # Limpiamos el path para que no salga la barra inclinada extra
            proyecto = self.url().path.strip("/")
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            # Usamos get_html pasándole el path limpio y los datos
            self.wfile.write(self.get_html(proyecto, self.query_data()).encode("utf-8"))
        
        # 3. Caso: Error si no hay autor en otras rutas
        else:
            self.send_error(404, "Autor no encontrado")

    def valida_autor(self):
        return 'autor' in self.query_data()

    def get_html(self, path, qs):
        # Retornamos el formato exacto que pide tu actividad
        return f"<h1>Proyecto: {path} Autor: {qs['autor']}</h1>"

if __name__ == "__main__":
    port = 8000
    print(f"Starting server on http://localhost:{port}")
    server = HTTPServer(("localhost", port), WebRequestHandler)
    server.serve_forever()