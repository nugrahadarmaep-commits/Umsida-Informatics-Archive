import sqlite3
import time
from abc import ABC, abstractmethod

# =========================================================
# sistem vanding mesin dengan oop class, object, inheritance, e
# nchapsulation, polymorphism, abstraction
# terintegrasi dengan database sqlite3
# =========================================================


# =========================================================
# DATABASE SETUP
# =========================================================
def init_db():
    conn = sqlite3.connect("vending_machine.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stok (
            id TEXT PRIMARY KEY,
            nama TEXT,
            harga REAL,
            jumlah INTEGER
        )
    """
    )
    # Cek apakah tabel kosong, kalau kosong baru isi data awal
    cursor.execute("SELECT COUNT(*) FROM stok")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO stok VALUES (?, ?, ?, ?)",
            [
                ("1", "Coca Cola", 7000, 3),
                ("2", "Pocari Sweat", 9000, 2),
                ("3", "Teh Pucuk Harum", 4000, 5),
                ("4", "Kopi Good Day", 6000, 4),
                ("5", "Susu Ultra Milk", 8500, 1),
            ],
        )
    conn.commit()
    conn.close()


# =========================================================
# BLUEPRINT PRODUCT (OOP)
# =========================================================
class Minuman(ABC):

    def __init__(self, id_produk, nama, harga):
        self.__id = id_produk
        self.__nama = nama
        self.__harga = harga

    def get_id(self):
        return self.__id

    def get_nama(self):
        return self.__nama

    def get_harga(self):
        return self.__harga

    @abstractmethod
    def keluar_efek(self):
        pass


class MinumanDingin(Minuman):

    def keluar_efek(self):
        return f"❄️  KLONTANG! {self.get_nama()} dingin meluncur!"


class MinumanPanas(Minuman):

    def keluar_efek(self):
        return f"🔥 SSSHH... {self.get_nama()} panas sudah siap!"


# =========================================================
# SISTEM VENDING MACHINE INTERAKTIF
# =========================================================
class VendingMachine:

    def format_rupiah(self, nominal):
        return f"Rp {nominal:,.0f}".replace(",", ".")

    def tampilkan_menu(self):
        print("\n" + "=" * 45)
        print("🥤     VENDING MACHINE PRODUCT LIST    🥤")
        print("=" * 45)
        print(f"{'No':<5} | {'Nama Produk':<20} | {'Harga':<10} | {'Stok'}")
        print("-" * 45)

        # Mengambil data real-time langsung dari sqlite3
        conn = sqlite3.connect("vending_machine.db")
        c = conn.cursor()
        c.execute("SELECT id, nama, harga, jumlah FROM stok")
        rows = c.fetchall()

        for row in rows:
            id_p, nama, harga, jumlah = row
            status_stok = jumlah if jumlah > 0 else "HABIS!"
            harga_rp = self.format_rupiah(harga)
            print(f"[{id_p}]   | {nama:<20} | {harga_rp:<10} | {status_stok}")

        print("=" * 45)
        conn.close()

    def cetak_resi(self, produk, bayar, kembalian):
        print("\n" + "." * 35)
        print(" 🧾 STRUK PEMBELIAN VENDING MACHINE 🧾")
        print("." * 35)
        print(f" Produk  : {produk.get_nama()}")
        print(f" Harga   : {self.format_rupiah(produk.get_harga())}")
        print(f" Dibayar : {self.format_rupiah(bayar)}")
        print(f" Kembali : {self.format_rupiah(kembalian)}")
        print("." * 35)
        print(" Terima kasih sudah berbelanja... 😎\n")

    def mulai_operasi(self):
        while True:
            self.tampilkan_menu()
            pilihan = input("👉 Masukkan nomor produk (0 untuk keluar): ")

            if pilihan == "0":
                print("\nSelamat Berbelanja Kembali...\n")
                break

            # 🛠️ Hubungkan ke database buat nyari produk
            conn = sqlite3.connect("vending_machine.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nama, harga, jumlah FROM stok WHERE id = ?", (pilihan,)
            )
            produk_db = cursor.fetchone()

            if not produk_db:
                print("\n❌ Nomor produk tidak ada di menu!\n")
                conn.close()
                continue

            nama_produk, harga_produk, stok_produk = produk_db

            if stok_produk <= 0:
                print(f"\n❌ {nama_produk} habis! Pilih yang lain.\n")
                conn.close()
                continue

            try:
                harga_rp = self.format_rupiah(harga_produk)
                print(f"\n🛒 Product: {nama_produk} | Harga: {harga_rp}")
                uang_masuk = float(input("💵 Masukkan Jumlah Uang Anda (Rp): "))
            except ValueError:
                print("\n❌ Input angka nominal uang yang sesuai!\n")
                conn.close()
                continue

            if uang_masuk < harga_produk:
                kurang = harga_produk - uang_masuk
                print(
                    f"\n💸 Nominal Kurang! kurang {self.format_rupiah(kurang)}.\n"
                )
                conn.close()
                continue

            # --- PROSES BERHASIL ---
            kembalian = uang_masuk - harga_produk

            # UPDATE STOK DI DATABASES REAL-TIME
            cursor.execute(
                "UPDATE stok SET jumlah = jumlah - 1 WHERE id = ?", (pilihan,)
            )
            conn.commit()
            conn.close()

            # Jeda dramatis 3 detik request lu
            print("\n⚙️  Memproses pesanan", end="", flush=True)
            for _ in range(3):
                time.sleep(1)
                print(".", end="", flush=True)
            print("\n")

            # Polimorfisme secara dinamis agar konsep OOP-nya tetap jalan
            if "Kopi" in nama_produk or "Susu" in nama_produk:
                produk_objek = MinumanPanas(pilihan, nama_produk, harga_produk)
            else:
                produk_objek = MinumanDingin(pilihan, nama_produk, harga_produk)

            print(f"{produk_objek.clear_efek() if hasattr(produk_objek, 'clear_efek') else produk_objek.keluar_efek()}\n")

            # Cetak Resi
            self.cetak_resi(produk_objek, uang_masuk, kembalian)

            lanjut = input("👉 Mau beli lagi? (y/n): ").lower()
            if lanjut != "y":
                print("\n👋 Sampai jumpa lagi!\n")
                break


# =========================================================
# MAIN PROGRAM EXECUTOR
# =========================================================
if __name__ == "__main__":
    init_db()

    mesin = VendingMachine()
    mesin.mulai_operasi()