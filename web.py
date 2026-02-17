from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    # --- PROPIEDAD DE CLASE: DICCIONARIO DE RUTAS ---
    # Definimos el diccionario aquí para simular una base de datos de páginas.
    # Usamos try/except al leer archivos para evitar que el servidor falle si no existen.
    
    # 1. Leemos el contenido de home.html
    try:
        with open("home.html", "r", encoding="utf-8") as f:
            home_content = f.read()
    except FileNotFoundError:
        home_content = "<h1>Error: home.html no encontrado</h1>"

    # 2. Leemos el contenido de 1.html (Proyecto web-uno)
    try:
        with open("1.html", "r", encoding="utf-8") as f:
            web_uno_content = f.read()
    except FileNotFoundError:
        web_uno_content = "<h1>Proyecto: web-uno (Archivo 1.html no encontrado)</h1>"

    # 3. Definimos el diccionario 'contenido' mapeando Rutas -> HTML
    contenido = {
        '/': home_content,
        '/proyecto/web-uno': web_uno_content,
        '/proyecto/web-dos': "<html><h1>Proyecto: web-dos</h1><p>Contenido en construcción</p></html>",
        '/proyecto/web-tres': "<html><h1>Proyecto: web-tres</h1><p>Contenido en construcción</p></html>",
    }

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        # Obtenemos la ruta solicitada (ej: '/proyecto/web-uno')
        path = self.url().path
        
        # --- LÓGICA PRINCIPAL MODIFICADA ---
        # Verificamos si la ruta existe dentro de nuestro diccionario 'contenido'
        if path in self.contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            # Recuperamos el HTML del diccionario usando la ruta como llave
            html_response = self.contenido[path]
            self.wfile.write(html_response.encode("utf-8"))
            
        else:
            # Si la ruta no está en el diccionario, enviamos error 404
            self.send_error(404, "Pagina no encontrada en el sistema")

if __name__ == "__main__":
    port = 8000
    print(f"Starting server on http://localhost:{port}")
    server = HTTPServer(("localhost", port), WebRequestHandler)
    server.serve_forever()