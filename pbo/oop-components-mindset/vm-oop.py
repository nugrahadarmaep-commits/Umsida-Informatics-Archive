import time
from abc import ABC, abstractmethod

# =========================================================
# Sistem vending mesin dengan OOP (Class, Object, Inheritance, 
# Encapsulation, Polymorphism, Abstraction)
# VERSI MURNI TANPA DATABASE (Menggunakan Dictionary In-Memory)
# =========================================================

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
    def __init__(self):
        # Pengganti Database: Data disimpan dalam struktur Dictionary (Encapsulation)
        self.__stok_produk = {
            "1": {"nama": "Coca Cola", "harga": 7000, "jumlah": 3},
            "2": {"nama": "Pocari Sweat", "harga": 9000, "jumlah": 2},
            "3": {"nama": "Teh Pucuk Harum", "harga": 4000, "jumlah": 5},
            "4": {"nama": "Kopi Good Day", "harga": 6000, "jumlah": 4},
            "5": {"nama": "Susu Ultra Milk", "harga": 8500, "jumlah": 1},
        }

    def format_rupiah(self, nominal):
        return f"Rp {nominal:,.0f}".replace(",", ".")

    def tampilkan_menu(self):
        print("\n" + "=" * 45)
        print("🥤     VENDING MACHINE PRODUCT LIST    🥤")
        print("=" * 45)
        print(f"{'No':<5} | {'Nama Produk':<20} | {'Harga':<10} | {'Stok'}")
        print("-" * 45)

        # Mengambil data dari Dictionary Local
        for id_p, data in self.__stok_produk.items():
            status_stok = data["jumlah"] if data["jumlah"] > 0 else "HABIS!"
            harga_rp = self.format_rupiah(data["harga"])
            print(f"[{id_p}]   | {data['nama']:<20} | {harga_rp:<10} | {status_stok}")

        print("=" * 45)

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

            # 🛠️ Hubungkan ke Dictionary buat nyari produk
            if pilihan not in self.__stok_produk:
                print("\n❌ Nomor produk tidak ada di menu!\n")
                continue

            produk_pilihan = self.__stok_produk[pilihan]
            nama_produk = produk_pilihan["nama"]
            harga_produk = produk_pilihan["harga"]
            stok_produk = produk_pilihan["jumlah"]

            if stok_produk <= 0:
                print(f"\n❌ {nama_produk} habis! Pilih yang lain.\n")
                continue

            try:
                harga_rp = self.format_rupiah(harga_produk)
                print(f"\n🛒 Product: {nama_produk} | Harga: {harga_rp}")
                uang_masuk = float(input("💵 Masukkan Jumlah Uang Anda (Rp): "))
            except ValueError:
                print("\n❌ Input angka nominal uang yang sesuai!\n")
                continue

            if uang_masuk < harga_produk:
                kurang = harga_produk - uang_masuk
                print(f"\n💸 Nominal Kurang! kurang {self.format_rupiah(kurang)}.\n")
                continue

            # --- PROSES BERHASIL ---
            kembalian = uang_masuk - harga_produk

            # UPDATE STOK DI DICTIONARY REAL-TIME
            self.__stok_produk[pilihan]["jumlah"] -= 1

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

            print(f"{produk_objek.keluar_efek()}\n")

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
    mesin = VendingMachine()
    mesin.mulai_operasi()