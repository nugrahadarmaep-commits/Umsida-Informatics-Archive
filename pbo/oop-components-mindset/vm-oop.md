# 🥤 Vending Machine OOP - PBL09-PBO

Repositori ini berisi program simulasi **Vending Machine (Mesin Penjual Otomatis)** yang dibuat murni menggunakan bahasa Python. 

Program ini adalah contoh penerapan **6 Pilar Pemrograman Berorientasi Objek (OOP)** secara utuh, tanpa menggunakan database eksternal. Semua data disimpan sementara di dalam memori program (menggunakan *Dictionary*).

---

## 🧠 Konsep OOP yang Dipakai

Biar gampang dipahami, ini penjelasan konsep OOP yang ada di dalam program ini:

### 1. Class & Object (Cetakan & Wujud Nyata)
* **Class:** Ibarat cetakan atau cetak biru (blueprint). Di kode ini ada cetakan bernama `VendingMachine` dan `Minuman`.
* **Object:** Wujud nyata dari cetakan tersebut. Saat kita mengetik `mesin = VendingMachine()`, kita baru saja menciptakan satu wujud mesin minuman di dunia nyata program ini.

### 2. Encapsulation (Keamanan Data / Kapsul)
* Kita menyembunyikan data sensitif biar nggak gampang dirusak atau diubah sembarangan dari luar. 
* **Contoh di kode:** Data stok minuman disimpan dalam variabel `__stok_produk`. Tanda garis bawah ganda (`__`) itu ibarat brankas; data cuma bisa diakses dan diubah melalui prosedur resmi dari dalam mesin.

### 3. Inheritance (Pewarisan Sifat)
* Ibarat bapak mewariskan sifat ke anaknya.
* **Contoh di kode:** Kita punya cetakan induk bernama `Minuman`. Kemudian kita bikin cetakan anak bernama `MinumanDingin` dan `MinumanPanas`. Kedua anak ini otomatis punya sifat (seperti id, nama, dan harga) yang diwariskan dari induknya.

### 4. Polymorphism (Banyak Bentuk / Beda Gaya)
* Satu perintah yang sama, tapi ditanggapi dengan cara berbeda tergantung siapa yang disuruh.
* **Contoh di kode:** Ada perintah `keluar_efek()`. Kalau yang dipesan adalah `MinumanDingin`, efek yang keluar adalah teks *"❄️ KLONTANG!"*. Tapi kalau yang dipesan `MinumanPanas`, efek yang keluar adalah *"🔥 SSSHH..."*.

### 5. Abstraction (Aturan Baku)
* Aturan wajib yang harus ditaati oleh semua turunannya tanpa perlu menjelaskan detailnya di awal.
* **Contoh di kode:** Cetakan induk `Minuman` mewajibkan semua minuman harus punya fitur `keluar_efek()`. Induknya nggak peduli efeknya bunyinya gimana, pokoknya harus ada!

---

## 🛠️ Cara Memainkan Program

Nggak perlu ribet *install* database! Cukup ikuti langkah ini:
1. Pastikan di komputermu sudah ter-install Python.
2. Buka terminal (CMD/PowerShell) di dalam folder tempat file ini berada.
3. Jalankan perintah ini:
   ```bash
   python nama_file_programmu.py