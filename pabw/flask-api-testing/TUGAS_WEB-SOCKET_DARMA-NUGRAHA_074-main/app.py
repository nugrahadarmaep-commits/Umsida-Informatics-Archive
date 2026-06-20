"""
PORTAL DATA UNIVERSITAS MUHAMMADIYAH SIDOARJO (UMSIDA)
Implementasi Flask Framework DASAR.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================================
# KONFIGURASI DESAIN (CSS GLOBAL)
# ============================================================
STYLE_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Inter', sans-serif;
        background-color: #F3F4F6;
        color: #1F2937;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    .container {
        background: #FFFFFF;
        padding: 50px 40px;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
        max-width: 600px;
        width: 100%;
        text-align: center;
    }
    h1 { font-weight: 600; font-size: 26px; color: #111827; margin-bottom: 12px; letter-spacing: -0.5px; }
    p.subtitle { color: #6B7280; font-size: 15px; line-height: 1.6; margin-bottom: 35px; }
    .btn-primary {
        display: inline-block;
        background-color: #2563EB;
        color: #FFFFFF;
        padding: 16px 32px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 500;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.2);
    }
    .btn-primary:hover { background-color: #1D4ED8; transform: translateY(-2px); }
    .divider { height: 1px; background-color: #E5E7EB; margin: 35px 0; }
    .menu-list { list-style: none; text-align: left; }
    .menu-list li { margin-bottom: 16px; }
    .menu-list a { color: #4B5563; text-decoration: none; font-size: 14px; display: flex; align-items: center; }
    .menu-list a:hover { color: #2563EB; }
    .menu-list a::before { content: "→"; margin-right: 12px; color: #D1D5DB; font-weight: bold; }
    pre { background: #F8FAFC; padding: 20px; border-radius: 12px; overflow-x: auto; border: 1px solid #E2E8F0; font-family: 'Courier New', monospace; font-size: 13px; text-align: left; color: #334155; margin-top: 20px; }
    p.status { color: #059669; font-size: 15px; margin-bottom: 25px; font-weight: 500; display: flex; align-items: center; justify-content: center; }
    p.status::before { content: "●"; margin-right: 8px; font-size: 18px; }
</style>
"""

# ============================================================
# HALAMAN UTAMA
# ============================================================

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>Portal Data UMSIDA</title>
        {STYLE_CSS}
    </head>
    <body>
        <div class="container">
            <h1>Portal Data UMSIDA</h1>
            <p class="subtitle">Akses informasi dan sinkronisasi data mahasiswa secara real-time melalui infrastruktur Flask yang aman.</p>
            <a href="/scrape" class="btn-primary">Sinkronisasi Data Sekarang</a>
            <div class="divider"></div>
            <ul class="menu-list">
                <li><a href="/hello/Mahasiswa">Uji Coba Rute Dinamis</a></li>
                <li><a href="/query?nama=Darma&umur=25">Uji Coba Data Darma (Parameter Query)</a></li>
                <li><a href="/api/data">Uji Coba Format API JSON</a></li>
                <li><a href="/form">Uji Coba Formulir Sistem</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

# ============================================================
# PROSES SCRAPING
# ============================================================

@app.route('/scrape')
def scrape_umsida():
    import scrapping_tugas 
    try:
        data_hasil = scrapping_tugas.jalankan_scraping()
        return f"""
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <title>Laporan Sinkronisasi</title>
            {STYLE_CSS}
        </head>
        <body>
            <div class="container" style="max-width: 850px;">
                <h1>Laporan Penarikan Data</h1>
                <p class="status">Sistem berhasil melakukan sinkronisasi real-time</p>
                <pre>{data_hasil}</pre>
                <a href="/" class="btn-primary" style="background-color: #F3F4F6; color: #374151; box-shadow: none; margin-top: 30px;"> Kembali ke Beranda</a>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"<div class='container'><h1>Terjadi Kesalahan</h1><p>{e}</p></div>", 500

# ============================================================
# FITUR TAMBAHAN (PROTOTYPE)
# ============================================================

@app.route('/hello/<name>')
def say_hello(name):
    return f"""
    <div class="container">
        <h1>Halo, {name}!</h1>
        <p class="subtitle">Sistem Flask berhasil mendeteksi identitas Anda melalui URL dinamis.</p>
        <a href="/" class="btn-primary">Kembali</a>
    </div>
    """

@app.route('/query')
def handle_query():
    nama = request.args.get('nama', 'Pengguna')
    umur = request.args.get('umur', '-')
    return f"""
    <div class="container">
        <h1>Informasi Parameter</h1>
        <p class="subtitle">Data yang diterima dari sistem: <b>{nama}</b> (Umur: {umur})</p>
        <a href="/" class="btn-primary">Kembali</a>
    </div>
    """

@app.route('/form', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        name = request.form.get('name')
        return f"<div class='container'><h1>Berhasil!</h1><p>Data {name} telah tersimpan.</p><a href='/form' class='btn-primary'>Kembali</a></div>"
    return f"""
    <div class="container">
        <h1>Formulir Data</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Masukkan Nama Lengkap" required style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #E5E7EB; margin-bottom: 20px;">
            <input type="submit" value="Kirim Data" class="btn-primary" style="cursor: pointer; width: 100%; border: none;">
        </form>
    </div>
    """

@app.route('/api/data')
def api_data():
    return jsonify({"status": "success", "message": "API siap digunakan"})

if __name__ == '__main__':
    print("Mempersiapkan server Flask Premium...")
    app.run(debug=True, host='localhost', port=5000)