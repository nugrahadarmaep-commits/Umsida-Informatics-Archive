# 🚨 Program Metode Numerik - Mencari Akar Persamaan dengan Regula Falsi (20 Iterasi Auto-Rekap)

Repositori ini berisi program Python untuk mencari akar persamaan non-linier dari fungsi $f(x) = x^3 - 2x - 5$ menggunakan **Metode Regula Falsi (Metode Posisi Palsu)**. 

Program ini didesain agar otomatis berjalan sebanyak **20 iterasi penuh** untuk memberikan akurasi tinggi dan menyajikan data rekapitulasi akhir menggunakan tabel grafis ASCII yang sangat rapi.

---

## 🧠 Konsep Dasar & Logika Program

Biar gak pusing sama istilah matematika dewa, ini penjelasan simpel gimana program ini bekerja mencari akar:

1. **Pengecekan Awal (Syarat Batas):**
   Program bakal minta input batas bawah ($a$) dan batas atas ($b$). Sistem bakal ngecek dulu lewat rumus $f(a) \times f(b) < 0$. Kalau hasilnya positif, program bakal mogok kerja karena itu artinya di dalam jarak/interval tersebut kagak ada akar persamaannya.
2. **Pencarian Akar Otomatis (20 Iterasi):**
   Program bakal langsung nge-looping otomatis sebanyak 20 kali menggunakan rumus utama Regula Falsi:
   $$c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)}$$
3. **Penyaringan Interval Baru:**
   Setiap dapet nilai $c$ baru, program ngecek:
   * Jika $f(a) \times f(c) < 0$, maka nilai $b$ bakal diganti sama nilai $c$.
   * Jika sebaliknya, maka nilai $a$ yang diganti sama nilai $c$.
4. **Sistem Auto-Stop (Fitur Cerdas):**
   Jika di tengah jalan (misal pada iterasi ke-5 atau ke-12) nilai $f(c)$ sudah menyentuh angka `0` mutlak, program bakal langsung berhenti secara cerdas karena akar sejatinya sudah ketemu, jadi gak bakal buang-buang waktu sampai 20 kali putaran.

---

## 📊 Format Output Tabel Akhir

Di akhir proses, program bakal ngebungkus semua histori perhitungan dari iterasi 1 sampai 20 ke dalam satu tabel kotak presisi dengan kolom-kolom berikut:
* **Iter:** Nomor urut iterasi (1-20).
* **a & b:** Batas interval yang terus mengecil dan bergeser.
* **f(a) & f(b):** Hasil evaluasi fungsi pada batas interval.
* **c (Akar):** Nilai tebakan akar persamaan pada iterasi tersebut.
* **f(c):** Nilai evaluasi fungsi pada titik $c$ (semakin mendekati 0 semakin bagus).
* **Error (%):** Tingkat kesalahan persentase dibanding iterasi sebelumnya.

---

## 🛠️ Cara Eksekusi Program (Jalur Windows Terminal)

1. Pastikan Python sudah ter-install di perangkatmu.
2. Buka Terminal/PowerShell langsung di dalam folder projek ini.
3. Ketik perintah berikut lalu tekan Enter:
   ```bash
   python nama_file_metnum_kamu.py