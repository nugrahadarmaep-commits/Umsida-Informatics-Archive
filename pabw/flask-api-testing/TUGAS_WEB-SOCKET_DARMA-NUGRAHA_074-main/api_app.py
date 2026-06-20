from flask import Flask, jsonify, request

app = Flask(__name__)

# ============================================================
# DATABASE SEMENTARA (DUMMY DATA)
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
# ROUTING RESTFUL API
# ============================================================

# 1. READ: Mengambil semua data mahasiswa (GET)
@app.route('/api/mahasiswa', methods=['GET'])
def get_semua_mahasiswa():
    # Membungkus data dengan jsonify agar menjadi format JSON
    return jsonify({
        "pesan": "Berhasil mengambil data mahasiswa",
        "data": daftar_mahasiswa
    }), 200

# 2. CREATE: Menambah data mahasiswa baru (POST)
@app.route('/api/mahasiswa', methods=['POST'])
def tambah_mahasiswa():
    # 1. Menangkap "paket" JSON yang dikirim dari Thunder Client
    data_baru = request.get_json()
    
    # 2. Menyusun data tersebut menjadi format mahasiswa
    mahasiswa_baru = {
        "id": get_next_id(), # Otomatis membuat ID baru
        "nama": data_baru.get("nama"),
        "nim": data_baru.get("nim"),
        "jurusan": data_baru.get("jurusan"),
        "angkatan": data_baru.get("angkatan", 2024) # Default 2024 jika lupa diisi
    }
    
    # 3. Memasukkan data baru ke dalam List (Database sementara)
    daftar_mahasiswa.append(mahasiswa_baru)
    
    # 4. Memberikan jawaban ke Thunder Client bahwa proses sukses
    return jsonify({
        "pesan": f"Mantap! Data mahasiswa {mahasiswa_baru['nama']} berhasil masuk dapur cuy!",
        "data": mahasiswa_baru
    }), 201  # 201 adalah kode HTTP untuk 'Created' (Berhasil dibuat)

# 3. UPDATE: Mengedit data mahasiswa (PUT)
@app.route('/api/mahasiswa/<int:id>', methods=['PUT'])
def edit_mahasiswa(id):
    # Cari dulu mahasiswanya berdasarkan ID
    mahasiswa = find_mahasiswa_by_id(id)
    
    # Kalau ID-nya ngawur / tidak ditemukan
    if not mahasiswa:
        return jsonify({"pesan": "Waduh, data tidak ditemukan cuy gimana dong cuy!"}), 404

    # Kalau ketemu, tangkap data perubahannya dari Thunder Client
    data_update = request.get_json()
    
    # Update datanya (jika tidak ada data baru yang dikirim, biarkan pakai data lama)
    mahasiswa.update({
        "nama": data_update.get("nama", mahasiswa["nama"]),
        "nim": data_update.get("nim", mahasiswa["nim"]),
        "jurusan": data_update.get("jurusan", mahasiswa["jurusan"]),
        "angkatan": data_update.get("angkatan", mahasiswa["angkatan"])
    })
    
    return jsonify({
        "pesan": f"Sip! Data {mahasiswa['nama']} berhasil diupdate!",
        "data": mahasiswa
    }), 200

# 4. DELETE: Menghapus data mahasiswa (DELETE)
@app.route('/api/mahasiswa/<int:id>', methods=['DELETE'])
def hapus_mahasiswa(id):
    # Panggil list global karena kita mau menghapus isinya
    global daftar_mahasiswa 
    
    # Cari dulu mahasiswanya
    mahasiswa = find_mahasiswa_by_id(id)
    
    # Kalau ID-nya ngawur
    if not mahasiswa:
        return jsonify({"pesan": "Waduh sepuranya cuy, data tidak ditemukan cuy!"}), 404
        
    # Kalau ketemu, langsung eksekusi hapus dari list!
    daftar_mahasiswa.remove(mahasiswa)
    
    return jsonify({
        "pesan": f"Mantap! Data {mahasiswa['nama']} berhasil dihapus dari muka bumi!"
    }), 200


# SYNTAX OUTPUT PROGRAM KELUAR
if __name__ == '__main__':
    app.run(debug=True, port=5000)

