# 🤖 Vending Machine Suica - PBL09 PBO (Modern Python)

Repositori ini berisi implementasi simulasi sistem Vending Machine Suica untuk memenuhi tugas Project Based Learning (PBL09) mata kuliah Pemrograman Berorientasi Objek (PBO). 

Sistem ini tidak hanya menggunakan konsep OOP klasik, tetapi juga mengimplementasikan fitur-fitur modern dari Python (versi 3.10 ke atas) agar kode lebih rapi, aman, dan mudah dibaca.

---

## 🚀 4 Konsep Modern yang Digunakan

Berikut adalah penjelasan simpel tentang teknologi Python modern yang dipakai di dalam kode ini:

### 1. Multi-paradigm Programming (Gabungan Konsep)
Di sini kita nggak cuma terpaku sama satu gaya *coding* (OOP). Kita menggabungkan OOP (membuat class/objek) dengan gaya *Functional Programming*. 
* **Contoh di kode:** Menggunakan fungsi bawaan `filter()` dan `lambda` saat menampilkan menu. Jadi, daripada bikin `for-loop` panjang buat nyari minuman yang stoknya masih ada, kita cukup pakai satu baris kode yang ringkas dan sat-set.

### 2. Data-Oriented Patterns (@dataclass)
Kalau biasanya di OOP kita capek nulis `__init__` berulang kali cuma buat nyimpen data, di sini kita pakai fitur `@dataclass`.
* **Maksudnya:** Fitur ini bikin class murni berfungsi sebagai "wadah data" (seperti struck/record). Objek seperti `Produk`, `KartuSuica`, dan `UangTunai` jadi lebih bersih dari fungsi-fungsi yang rumit, sehingga struktur data lebih mudah dikelola.

### 3. Type Hints & Static Typing (Label Tipe Data)
Python itu aslinya bebas (bisa masukin tipe data apa aja ke variabel), tapi kadang bikin bingung sendiri pas programnya udah gede. Nah, di sini kita kasih "label" ke setiap variabel dan fungsi.
* **Maksudnya:** Kita ngasih tahu secara eksplisit, misalnya fungsi ini butuh input berupa angka (`int`) atau teks (`str`), dan balikan fungsinya apa. Ini sangat membantu *code editor* (seperti VS Code) buat ngasih peringatan *error* SEBELUM programnya dijalankan.

### 4. Pattern Matching (match...case)
Ini adalah fitur baru yang keren banget di Python 3.10+. Fungsinya mirip `switch-case` di bahasa pemrograman lain, tapi jauh lebih pintar.
* **Maksudnya:** Daripada pakai rantai `if-elif-else` yang panjang dan bikin sakit mata buat ngecek user bayar pakai apa (Cash atau Suica), kita pakai `match...case`. Sistem bisa langsung menebak tipe pembayaran sekaligus mengekstrak nominal saldonya di dalam satu blok yang elegan.

---

## 🛠️ Cara Menjalankan Program

1. Pastikan laptop sudah ter-install **Python versi 3.10** atau yang lebih baru.
2. Clone repositori ini ke laptop.
3. Buka terminal, arahkan ke folder project.
4. Jalankan perintah berikut:
   ```bash
   python vending_machine.py