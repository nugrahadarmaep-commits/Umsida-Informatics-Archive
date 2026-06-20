"""
APLIKASI CRUD LENGKAP + WEB SOCKET SCRAPING
Tampilan Elegant (Tanpa perlu folder templates!)
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import scrapping_tugas
import time
import json

app = Flask(__name__)
app.secret_key = 'rahasia_crud_123'
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================================
# DATABASE SEDERHANA
# ============================================================
daftar_mahasiswa = [
    {"id": 1, "nama": "Andi Wijaya", "nim": "20230001", "jurusan": "Teknik Informatika", "angkatan": 2023},
    {"id": 2, "nama": "Budi Santoso", "nim": "20230002", "jurusan": "Sistem Informasi", "angkatan": 2023},
    {"id": 3, "nama": "Citra Dewi", "nim": "20230003", "jurusan": "Teknik Komputer", "angkatan": 2023},
]

def get_next_id():
    return max([m["id"] for m in daftar_mahasiswa] + [0]) + 1

def find_mahasiswa_by_id(m_id):
    return next((m for m in daftar_mahasiswa if m["id"] == m_id), None)

# ============================================================
# CSS & DESAIN ELEGANT 
# ============================================================
STYLE_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
    body { background-color: #F3F4F6; color: #1F2937; }
    .navbar { background-color: #2563EB; color: white; padding: 15px 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .navbar h2 { font-size: 20px; font-weight: 600; margin: 0; }
    .container { max-width: 1000px; margin: 30px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .top-controls { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .search-box { display: flex; gap: 10px; }
    .search-box input { padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px; width: 250px; outline: none; }
    .btn { padding: 10px 15px; border-radius: 6px; border: none; cursor: pointer; color: white; text-decoration: none; font-size: 14px; font-weight: 500; transition: 0.2s; }
    .btn-green { background-color: #10B981; } .btn-green:hover { background-color: #059669; }
    .btn-blue { background-color: #3B82F6; } .btn-blue:hover { background-color: #2563EB; }
    .btn-yellow { background-color: #F59E0B; color: white; } .btn-yellow:hover { background-color: #D97706; }
    .btn-red { background-color: #EF4444; } .btn-red:hover { background-color: #DC2626; }
    .btn-purple { background-color: #8B5CF6; width: 100%; margin-bottom: 20px; font-size: 16px; } .btn-purple:hover { background-color: #7C3AED; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    table, th, td { border: 1px solid #E5E7EB; }
    th { background-color: #F9FAFB; padding: 12px; text-align: left; color: #4B5563; }
    td { padding: 12px; }
    tr:nth-child(even) { background-color: #F9FAFB; }
    #log-container { display: none; background: #1E293B; color: #10B981; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 13px; margin-bottom: 20px; max-height: 100px; overflow-y: auto; }
    .form-group { margin-bottom: 15px; }
    .form-group label { display: block; margin-bottom: 5px; font-weight: 500; }
    .form-group input { width: 100%; padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px; outline: none; }
    .flash { padding: 15px; border-radius: 6px; margin-bottom: 20px; }
    .flash.success { background: #D1FAE5; color: #065F46; border: 1px solid #10B981; }
    .flash.error { background: #FEE2E2; color: #991B1B; border: 1px solid #EF4444; }
</style>
"""

# ============================================================
# TEMPLATE HTML (INDEX)
# ============================================================
INDEX_HTML = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Aplikasi CRUD Mahasiswa</title>
    {STYLE_CSS}
</head>
<body>
    <div class="navbar">
        <h2>Aplikasi CRUD Data Mahasiswa</h2>
    </div>
    <div class="container">
        {{% with messages = get_flashed_messages(with_categories=true) %}}
            {{% if messages %}}
                {{% for category, message in messages %}}
                    <div class="flash {{{{ category }}}}">{{{{ message }}}}</div>
                {{% endfor %}}
            {{% endif %}}
        {{% endwith %}}

        <button onclick="startScraping()" id="btn-scrape" class="btn btn-purple">⚡ Sinkronisasi Data UMSIDA (Web Socket)</button>
        <div id="log-container"></div>

        <div class="top-controls">
            <a href="/tambah" class="btn btn-green">+ Tambah Data</a>
            <form action="/search" method="GET" class="search-box">
                <input type="text" name="q" placeholder="Cari nama atau NIM..." value="{{{{ search_keyword | default('') }}}}">
                <button type="submit" class="btn btn-blue">Cari</button>
            </form>
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th><th>Nama</th><th>NIM</th><th>Jurusan</th><th>Angkatan</th><th style="width: 150px; text-align: center;">Aksi</th>
                </tr>
            </thead>
            <tbody>
                {{% for m in mahasiswa %}}
                <tr>
                    <td>{{{{ m.id }}}}</td><td>{{{{ m.nama }}}}</td><td>{{{{ m.nim }}}}</td><td>{{{{ m.jurusan }}}}</td><td>{{{{ m.angkatan }}}}</td>
                    <td style="text-align: center; gap: 5px; display: flex; justify-content: center;">
                        <a href="/edit/{{{{ m.id }}}}" class="btn btn-yellow" style="padding: 6px 12px;">Edit</a>
                        <a href="/hapus/{{{{ m.id }}}}" class="btn btn-red" style="padding: 6px 12px;" onclick="return confirm('Yakin ingin menghapus data ini?');">Hapus</a>
                    </td>
                </tr>
                {{% else %}}
                <tr><td colspan="6" style="text-align: center;">Tidak ada data ditemukan.</td></tr>
                {{% endfor %}}
            </tbody>
        </table>
    </div>
    <script>
        var socket = io();
        function startScraping() {{
            document.getElementById('btn-scrape').disabled = true;
            document.getElementById('log-container').style.display = 'block';
            document.getElementById('log-container').innerHTML = "Memulai koneksi Web Socket...<br>";
            socket.emit('start_scraping');
        }}
        socket.on('log_message', function(msg) {{
            var log = document.getElementById('log-container');
            log.innerHTML += "> " + msg + "<br>";
            log.scrollTop = log.scrollHeight;
        }});
        socket.on('reload_page', function() {{
            setTimeout(() => {{ window.location.reload(); }}, 1500);
        }});
    </script>
</body>
</html>
"""

# ============================================================
# TEMPLATE HTML (FORM TAMBAH & EDIT)
# ============================================================
FORM_HTML = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>{{{{ title }}}}</title>
    {STYLE_CSS}
</head>
<body>
    <div class="navbar"><h2>Aplikasi CRUD Data Mahasiswa</h2></div>
    <div class="container" style="max-width: 600px;">
        <h2 style="margin-bottom: 20px; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px;">{{{{ title }}}}</h2>
        {{% with messages = get_flashed_messages(with_categories=true) %}}
            {{% if messages %}}
                {{% for category, message in messages %}}
                    <div class="flash {{{{ category }}}}">{{{{ message }}}}</div>
                {{% endfor %}}
            {{% endif %}}
        {{% endwith %}}
        <form method="POST">
            <div class="form-group"><label>Nama Lengkap</label>
                <input type="text" name="nama" value="{{{{ mhs.nama if mhs else '' }}}}" required>
            </div>
            <div class="form-group"><label>NIM</label>
                <input type="text" name="nim" value="{{{{ mhs.nim if mhs else '' }}}}" required>
            </div>
            <div class="form-group"><label>Jurusan</label>
                <input type="text" name="jurusan" value="{{{{ mhs.jurusan if mhs else '' }}}}" required>
            </div>
            <div class="form-group"><label>Angkatan</label>
                <input type="number" name="angkatan" value="{{{{ mhs.angkatan if mhs else '2023' }}}}" required>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button type="submit" class="btn btn-blue" style="flex: 1;">Simpan Data</button>
                <a href="/" class="btn btn-red" style="flex: 1; text-align: center;">Batal</a>
            </div>
        </form>
    </div>
</body>
</html>
"""

# ============================================================
# ROUTING CRUD (Menggunakan render_template_string)
# ============================================================

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, mahasiswa=daftar_mahasiswa)

@app.route('/search')
def search():
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return redirect(url_for('index'))
    results = [m for m in daftar_mahasiswa if keyword.lower() in m['nama'].lower() or keyword in m['nim']]
    return render_template_string(INDEX_HTML, mahasiswa=results, search_keyword=keyword)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama, nim, jurusan, angkatan = request.form.get('nama').strip(), request.form.get('nim').strip(), request.form.get('jurusan').strip(), request.form.get('angkatan').strip()
        if any(m['nim'] == nim for m in daftar_mahasiswa):
            flash(f'NIM {nim} sudah terdaftar!', 'error')
            return redirect(url_for('tambah'))
        daftar_mahasiswa.append({
            "id": get_next_id(), "nama": nama, "nim": nim, "jurusan": jurusan, "angkatan": int(angkatan) if angkatan.isdigit() else 2023
        })
        flash(f'Data mahasiswa {nama} berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))
    return render_template_string(FORM_HTML, title="Tambah Data Baru", mhs=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mahasiswa = find_mahasiswa_by_id(id)
    if not mahasiswa:
        flash('Data tidak ditemukan!', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        nama, nim, jurusan, angkatan = request.form.get('nama').strip(), request.form.get('nim').strip(), request.form.get('jurusan').strip(), request.form.get('angkatan').strip()
        if any(m['nim'] == nim and m['id'] != id for m in daftar_mahasiswa):
            flash(f'NIM {nim} sudah digunakan!', 'error')
            return redirect(url_for('edit', id=id))
        mahasiswa.update({"nama": nama, "nim": nim, "jurusan": jurusan, "angkatan": int(angkatan) if angkatan.isdigit() else 2023})
        flash(f'Data {nama} berhasil diupdate!', 'success')
        return redirect(url_for('index'))
    return render_template_string(FORM_HTML, title="Edit Data Mahasiswa", mhs=mahasiswa)

@app.route('/hapus/<int:id>')
def hapus(id):
    global daftar_mahasiswa
    mhs = find_mahasiswa_by_id(id)
    if mhs:
        daftar_mahasiswa.remove(mhs)
        flash(f'Data {mhs["nama"]} berhasil dihapus!', 'success')
    return redirect(url_for('index'))

# ============================================================
# ROUTING WEB SOCKET (SCRAPING)
# ============================================================

@socketio.on('start_scraping')
def handle_scraping():
    emit('log_message', 'Memanggil script koki (scrapping_tugas.py)...')
    time.sleep(1)
    try:
        scrapping_tugas.jalankan_scraping()
        with open('tugas_akhir.json', 'r') as f:
            data_json = json.load(f)
        emit('log_message', f'Data berhasil di-scrape! Menambahkan {len(data_json[1:6])} data ke tabel...')
        
        for item in data_json[1:6]:  # Ambil 5 data teratas dari JSON
            daftar_mahasiswa.append({
                "id": get_next_id(),
                "nama": item.get('2', 'N/A'),
                "nim": item.get('1', 'N/A'),
                "jurusan": item.get('3', 'N/A'),
                "angkatan": 2022
            })
            emit('log_message', f'Berhasil Menambah: {item.get("2", "")}')
            time.sleep(0.3)
            
        emit('log_message', 'Selesai! Merefresh halaman dalam 1 detik...')
        emit('reload_page')
    except Exception as e:
        emit('log_message', f'ERROR: {str(e)}')

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 APLIKASI CRUD + SCRAPING + WEB SOCKET")
    print("=" * 50)
    socketio.run(app, debug=True, host='localhost', port=5000)