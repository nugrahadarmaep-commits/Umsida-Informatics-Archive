import time
from dataclasses import dataclass
from typing import List, Optional, Union

# =========================================================
# 2. DATA-ORIENTED PATTERNS & 3. TYPE HINTS + STATIC TYPING
# Menggunakan @dataclass untuk memisahkan struktur data dari behavior.
# Menggunakan Type Hints (str, int, dll) untuk validasi tipe data statis.
# =========================================================

@dataclass
class Produk:
    id_produk: str
    nama: str
    harga: int
    stok: int
    kategori: str

@dataclass
class KartuSuica:
    saldo: int

@dataclass
class UangTunai:
    nominal: int

# Type alias untuk multi-pembayaran
MetodePembayaran = Union[KartuSuica, UangTunai]


# =========================================================
# 1. MULTI-PARADIGM PROGRAMMING
# Menggabungkan OOP (Class/Object) dengan Functional Programming (filter/lambda)
# =========================================================

class VendingMachineModern:
    def __init__(self, daftar_produk: List[Produk]) -> None:
        self.inventory: List[Produk] = daftar_produk

    def format_rupiah(self, nominal: int) -> str:
        return f"Rp {nominal:,.0f}".replace(",", ".")

    def tampilkan_menu(self) -> None:
        print("\n" + "=" * 50)
        print("🤖 VENDING MACHINE NEXT-GEN SUICA 🤖")
        print("=" * 50)
        
        # Pendekatan Declarative/Functional untuk filter produk yang masih ada stok
        produk_tersedia = list(filter(lambda p: p.stok > 0, self.inventory))
        
        for p in produk_tersedia:
            print(f"[{p.id_produk}] | {p.nama:<18} | {self.format_rupiah(p.harga)}")
        print("=" * 50)

    def cari_produk(self, id_cari: str) -> Optional[Produk]:
        # Functional approach menggunakan generator dan next()
        return next((p for p in self.inventory if p.id_produk == id_cari), None)

    # =========================================================
    # 4. PATTERN MATCHING (Fitur baru Python 3.10+)
    # Menggunakan match...case untuk memproses berbagai tipe data secara elegan
    # =========================================================
    def proses_pembayaran(self, metode: MetodePembayaran, harga_produk: int) -> tuple[bool, int]:
        match metode:
            # Jika user bayar pakai Kartu Suica dan saldo cukup
            case KartuSuica(saldo) if saldo >= harga_produk:
                print("💳 [SUICA] Tit! Saldo berhasil dipotong.")
                return True, saldo - harga_produk
            
            # Jika user bayar pakai Kartu Suica tapi kere
            case KartuSuica(saldo):
                print(f"❌ [SUICA] Saldo lo cuma {self.format_rupiah(saldo)}, kurang Ngab!")
                return False, saldo
            
            # Jika user bayar Cash dan uang cukup/lebih
            case UangTunai(nominal) if nominal >= harga_produk:
                print("💵 [CASH] Uang tunai diterima mesin.")
                return True, nominal - harga_produk
            
            # Jika user bayar Cash tapi duitnya kurang
            case UangTunai(nominal):
                print(f"❌ [CASH] Uang lo cuma {self.format_rupiah(nominal)}, kurang Ngab!")
                return False, nominal
            
            # Fallback jika error tak terduga
            case _:
                print("❌ Sistem menolak jenis pembayaran alien ini!")
                return False, 0

    def transaksi(self, id_pilihan: str, metode_bayar: MetodePembayaran) -> None:
        produk = self.cari_produk(id_pilihan)
        
        if not produk:
            print("\n❌ ID Produk kagak ada di database memori!\n")
            return
            
        if produk.stok <= 0:
            print(f"\n❌ Yah, {produk.nama} udah ludes!\n")
            return

        print(f"\n🛒 Memproses {produk.nama} ({self.format_rupiah(produk.harga)})...")
        time.sleep(1)

        # Proses lewat pattern matching
        sukses, sisa_uang = self.proses_pembayaran(metode_bayar, produk.harga)

        if sukses:
            produk.stok -= 1
            print(f"🎉 KLONTANG! {produk.nama} keluar!")
            if isinstance(metode_bayar, UangTunai) and sisa_uang > 0:
                print(f"Kembalian lo: {self.format_rupiah(sisa_uang)}")
            elif isinstance(metode_bayar, KartuSuica):
                print(f"Sisa saldo Suica lo: {self.format_rupiah(sisa_uang)}")
        print("-" * 30)


# =========================================================
# MAIN EXECUTION
# =========================================================
if __name__ == "__main__":
    # Inisialisasi Data Menggunakan Data-Oriented Pattern (@dataclass)
    db_produk = [
        Produk("1", "Ocha Tea", 15000, 5, "Dingin"),
        Produk("2", "Pocari Sweat", 10000, 2, "Dingin"),
        Produk("3", "Coffee Boss", 20000, 3, "Panas")
    ]

    mesin = VendingMachineModern(db_produk)
    mesin.tampilkan_menu()

    # SIMULASI 1: Coba bayar Ocha Tea (Rp 15.000) pake Cash Rp 20.000 (Berhasil)
    print("\n>>> PEMBELI 1 (Cash Rp 20.000) <<<")
    dompet_cash = UangTunai(20000)
    mesin.transaksi("1", dompet_cash)

    # SIMULASI 2: Coba bayar Pocari (Rp 10.000) pake Kartu Suica isi Rp 5.000 (Gagal)
    print("\n>>> PEMBELI 2 (Suica Kere Rp 5.000) <<<")
    kartu_suica_kere = KartuSuica(5000)
    mesin.transaksi("2", kartu_suica_kere)

    # SIMULASI 3: Coba bayar Coffee Boss (Rp 20.000) pake Kartu Suica Sultan (Berhasil)
    print("\n>>> PEMBELI 3 (Suica Sultan Rp 100.000) <<<")
    kartu_suica_sultan = KartuSuica(100000)
    mesin.transaksi("3", kartu_suica_sultan)