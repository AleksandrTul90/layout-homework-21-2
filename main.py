from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

HOST_NAME = "localhost"
SERVER_PORT = 8080
PAGES_DIR = Path(__file__).parent / "pages"
CONTACTS_PAGE = PAGES_DIR / "contacts.html"
ERROR_404_PAGE = PAGES_DIR / "404.html"
ERROR_500_PAGE = PAGES_DIR / "500.html"


def read_html_file(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


class MyServer(BaseHTTPRequestHandler):

    def _send_html(self, html_content: str, status_code: int = 200) -> None:
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html_content, "utf-8"))

    def do_GET(self) -> None:
        try:
            html_content = read_html_file(CONTACTS_PAGE)
            self._send_html(html_content)
        except FileNotFoundError:
            html_content = read_html_file(ERROR_404_PAGE)
            self._send_html(html_content, 404)
        except Exception:
            html_content = read_html_file(ERROR_500_PAGE)
            self._send_html(html_content, 500)

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = parse_qs(post_data)

        print("Получены данные POST-запроса:")
        for key, value in parsed_data.items():
            print(f"  {key}: {', '.join(value)}")

        try:
            html_content = read_html_file(CONTACTS_PAGE)
            self._send_html(html_content)
        except Exception:
            html_content = read_html_file(ERROR_500_PAGE)
            self._send_html(html_content, 500)


if __name__ == "__main__":
    web_server = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")
