"""
WEB SERVER LANJUTAN - VERSI STABIL UNTUK WINDOWS
- Support multiple client dengan threading
- Bisa serve file statis
- Parsing query parameter
- Tidak putus koneksi di browser
- SAYA MODIFIKASI Ditambah fitur Web Scraping UMSIDA!
- SAYA MODIFIKASI Auto-generate External CSS!
"""

import socket
import threading
import os
from urllib.parse import urlparse, parse_qs

HOST = 'localhost'
PORT = 8081
STATIC_DIR = 'www'

# Buat folder www jika belum ada
os.makedirs(STATIC_DIR, exist_ok=True)

def create_sample_files():
    """Membuat file contoh dan CSS kekinian jika belum ada"""
    
    # 1. AUTO-GENERATE FILE CSS (Biar lu gak usah bikin manual!)
    style_path = os.path.join(STATIC_DIR, 'style.css')
    if not os.path.exists(style_path):
        with open(style_path, 'w', encoding='utf-8') as f:
            f.write("""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

body {
    font-family: 'Poppins', sans-serif; background-color: #0f172a; color: #f8fafc; 
    margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center;
}
.box {
    background: #1e293b; padding: 40px; border-radius: 16px; 
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); width: 100%; max-width: 800px; border: 1px solid #334155;
}
h1 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 15px; margin-top: 0; }
pre {
    background: #020617; padding: 20px; border-radius: 10px; overflow-x: auto; 
    color: #a7f3d0; font-family: 'Courier New', Courier, monospace; border: 1px solid #1e293b;
}
.btn {
    display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; 
    border-radius: 8px; text-decoration: none; font-weight: 600; transition: all 0.3s ease; margin-top: 10px;
}
.btn:hover { background: #2563eb; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4); }
.nav {
    background: #1e293b; padding: 20px; border-radius: 12px; margin-top: 20px; 
    width: 100%; max-width: 800px; text-align: center; border: 1px solid #334155;
}
.nav a { color: #38bdf8; margin: 0 15px; text-decoration: none; font-weight: bold; }
.nav a:hover { text-decoration: underline; color: #f8fafc; }
            """)

    # 2. AUTO-GENERATE INDEX.HTML
    index_path = os.path.join(STATIC_DIR, 'index.html')
    if not os.path.exists(index_path):
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Advanced Server</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="box">
        <h1>🚀 Advanced Socket Server</h1>
        <p>Server ini bisa serve file statis, form POST, dan Live Scraping!</p>
    </div>
    <div class="nav">
        <a href="/data?nama=Andi&umur=20">Test Query Parameter</a> |
        <a href="/submit">Test Form POST</a> |
        <a href="/about.html">About Page</a> |
        <a href="/scrape" class="btn">🔥 LIHAT DATA SCRAPING UMSIDA</a>
    </div>
</body>
</html>""")
    
    # 3. AUTO-GENERATE ABOUT.HTML
    about_path = os.path.join(STATIC_DIR, 'about.html')
    if not os.path.exists(about_path):
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>About</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="box">
        <h1>Tentang Server Ini</h1>
        <p>Ini adalah advanced web server dengan threading support.</p>
        <p>Server ini berjalan di port 8081</p>
        <a href="/" class="btn">Kembali ke Home</a>
    </div>
</body>
</html>""")

def parse_request(request_data):
    """Parse HTTP request menjadi struktur data"""
    try:
        lines = request_data.split('\r\n')
        if not lines:
            return None
        
        request_line = lines[0].split(' ')
        if len(request_line) < 2:
            return None
            
        method = request_line[0]
        path = request_line[1]
        version = request_line[2] if len(request_line) > 2 else "HTTP/1.1"
        
        headers = {}
        for line in lines[1:]:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value
            elif line == '':
                break
        
        parsed_url = urlparse(path)
        path_only = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        body = ''
        if 'Content-Length' in headers:
            try:
                content_length = int(headers['Content-Length'])
                body_parts = request_data.split('\r\n\r\n', 1)
                if len(body_parts) > 1:
                    body = body_parts[1][:content_length]
            except:
                pass
        
        return {
            'method': method,
            'path': path_only if path_only else '/',
            'version': version,
            'headers': headers,
            'query_params': query_params,
            'body': body
        }
    except Exception as e:
        print(f"Error parsing request: {e}")
        return None

def serve_static_file(path):
    """Membaca file statis dari disk"""
    safe_path = path.lstrip('/')
    if not safe_path or safe_path == '/':
        safe_path = 'index.html'
    
    full_path = os.path.join(STATIC_DIR, safe_path)
    
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
            
            if full_path.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif full_path.endswith('.css'):
                content_type = 'text/css'
            elif full_path.endswith('.js'):
                content_type = 'application/javascript'
            else:
                content_type = 'text/plain'
            
            return content, content_type, 200
        except Exception as e:
            print(f"Error reading file: {e}")
            return None, None, 500
    
    return None, None, 404

def send_response(client_socket, status_code, content_type, content):
    """Helper untuk mengirim response HTTP"""
    try:
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        response = f"HTTP/1.1 {status_code}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n".encode('utf-8') + content
        
        client_socket.sendall(response)
        return True
    except Exception as e:
        print(f"Error sending response: {e}")
        return False

def handle_client(client_socket, client_address):
    """Menangani satu koneksi client"""
    print(f"[Thread] Menangani {client_address}")
    
    try:
        client_socket.settimeout(10)
        request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
        
        if not request_data:
            client_socket.close()
            return
        
        parsed = parse_request(request_data)
        if not parsed:
            send_response(client_socket, "400 Bad Request", "text/html", "<h1>400 Bad Request</h1>")
            client_socket.close()
            return
        
        print(f"{parsed['method']} {parsed['path']} from {client_address}")
        
        # ROUTING
        # Route 1: Home page
        if parsed['path'] == '/' or parsed['path'] == '/index.html':
            content, content_type, status = serve_static_file('/index.html')
            if content:
                send_response(client_socket, "200 OK", content_type, content)
            else:
                html = "<h1>Advanced Socket Server</h1><p>Server berjalan dengan baik!</p>"
                send_response(client_socket, "200 OK", "text/html", html)
        
        # Route 2: Data dengan query parameter
        elif parsed['path'] == '/data':
            nama = parsed['query_params'].get('nama', ['Guest'])[0]
            umur = parsed['query_params'].get('umur', ['?'])[0]
            html = f"<html><body><h1>Data Diterima</h1><p>Nama: {nama}</p><p>Umur: {umur}</p><a href='/'>Kembali</a></body></html>"
            send_response(client_socket, "200 OK", "text/html", html)
        
        # Route 3: Form submit (GET dan POST)
        elif parsed['path'] == '/submit':
            if parsed['method'] == 'POST':
                html = f"<html><body><h1>POST Diterima</h1><pre>{parsed['body']}</pre><a href='/'>Kembali</a></body></html>"
                send_response(client_socket, "200 OK", "text/html", html)
            else:
                html = "<html><body><h1>Form Submit</h1><form method='POST'><input name='nama'><input type='submit'></form></body></html>"
                send_response(client_socket, "200 OK", "text/html", html)
        
        # ==========================================
        #  ROUTE SCRAPING DENGAN EXTERNAL CSS
        # ==========================================
        elif parsed['path'] == '/scrape':
            import scrapping_tugas 
            try:
                print("⏳ Menjalankan script scraping...")
                data_hasil = scrapping_tugas.jalankan_scraping()
                
                # HTML bersih, CSS dipanggil dari /style.css
                html = f"""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>LIVE SCRAPING WEB SOCKET</title>
                    <link rel="stylesheet" href="/style.css">
                </head>
                <body>
                    <div class="box">
                        <h1>SCRAPING DATA UMSIDA BERHASIL!</h1>
                        <p>Data diambil secara real-time dan disave ke <b>tugas_akhir.csv</b> dan <b>tugas_akhir.json</b>.</p>
                        <h3>[ Preview Data JSON ]</h3>
                        <pre>{data_hasil}</pre>
                        <a href="/" class="btn">← KEMBALI KE HOME</a>
                    </div>
                </body>
                </html>"""
                send_response(client_socket, "200 OK", "text/html", html)
            except Exception as e:
                error_html = f"<html><head><link rel='stylesheet' href='/style.css'></head><body><div class='box'><h1>Gagal Scraping Bang!</h1><p>Error: {e}</p><a href='/' class='btn'>Kembali</a></div></body></html>"
                send_response(client_socket, "500 Internal Error", "text/html", error_html)
                
        # ==========================================
        #  BATAS AKHIR ROUTE SCRAPING 
        # ==========================================

        # Route 4: Serve static files
        else:
            content, content_type, status = serve_static_file(parsed['path'])
            if content:
                send_response(client_socket, "200 OK", content_type, content)
            else:
                html = f"<html><body><h1>404 Not Found</h1><p>Path: {parsed['path']}</p><a href='/'>Kembali</a></body></html>"
                send_response(client_socket, "404 Not Found", "text/html", html)
        
    except socket.timeout:
        print(f" Timeout untuk {client_address}")
    except ConnectionResetError:
        print(f"🔌 Koneksi di-reset oleh client {client_address}")
    except Exception as e:
        print(f" Error handling {client_address}: {type(e).__name__}: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

def run_advanced_server():
    """Menjalankan server dengan threading"""
    create_sample_files()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    
    print("=" * 60)
    print(" 🚀 ADVANCED WEB SERVER (SOCKET + LIVE SCRAPING)")
    print("=" * 60)
    print(f" 🌐 Buka Browser di: http://{HOST}:{PORT}")
    print(" 💡 Tekan Ctrl+C di sini untuk menghentikan server")
    print("=" * 60)
    print("\n📡 Server siap menerima koneksi...\n")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server dihentikan oleh user")
    finally:
        server_socket.close()
        print("🔒 Socket server ditutup")

if __name__ == "__main__":
    run_advanced_server()