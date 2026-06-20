from abc import ABC, abstractmethod

# =====================================================================
# 1. CLASS & 6. ABSTRACTION
# =====================================================================
# Class Minuman ini adalah CETAKAN ABSTRAK (Blueprint).
# Gak bisa dibikin Object langsung, karena minuman itu harus jelas panas/dinginnya.
class Minuman(ABC):
    def __init__(self, nama, harga):
        # 3. ENCAPSULATION
        # Pakai double underscore (__) biar jadi PRIVATE.
        # Artinya 'nama' & 'harga' gak bisa diubah langsung dari luar.
        self.__nama = nama
        self.__harga = harga

    # Ini jalur resmi (public method) buat ngambil data private di atas
    def get_nama(self):
        return self.__nama

    def get_harga(self):
        return self.__harga

    # Ini metode abstrak. Semua class anak WAJIB bikin implementasinya!
    @abstractmethod
    def proses_keluar(self):
        pass


# =====================================================================
# 4. INHERITANCE (PEWARISAN)
# =====================================================================
# MinumanDingin mewarisi sifat nama & harga dari Minuman
class MinumanDingin(Minuman):
    
    # 5. POLYMORPHISM
    # Cara dia keluar beda dari minuman panas!
    def proses_keluar(self):
        return f"❄️  [DINGIN] {self.get_nama()} jatuh dari rak pendingin! KLONTANG!"


# MinumanPanas juga mewarisi sifat dari Minuman
class MinumanPanas(Minuman):
    
    # 5. POLYMORPHISM
    # Cara dia keluar pake efek pemanas
    def proses_keluar(self):
        return f"🔥 [PANAS] {self.get_nama()} disiapkan dari heater! SSSSHHH..."


# =====================================================================
# CLASS VENDING MACHINE 
# =====================================================================
class VendingMachine:
    def __init__(self):
        # 3. ENCAPSULATION
        # Stok dibungkus rahasia (private), gak boleh diutak-atik pembeli!
        self.__stok = {}

    def tambah_minuman(self, minuman, jumlah):
        self.__stok[minuman] = jumlah

    # 6. ABSTRACTION
    # Pembeli cuma manggil fungsi ini. Mereka gak tau kalau di dalem sini
    # ada validasi stok, pengurangan data, dll. Pokoknya tau beres!
    def beli(self, minuman, bayar):
        print(f"\n🛒 Mencoba beli {minuman.get_nama()} dengan uang Rp {bayar}...")
        
        # Cek stok di dalam (Encapsulation beraksi)
        if self.__stok.get(minuman, 0) <= 0:
            print("❌ Gagal: Stok habis bro!")
            return

        # Validasi harga
        harga = minuman.get_harga()
        if bayar < harga:
            print(f"💸 Gagal: Duit lu kurang! Harganya Rp {harga}.")
            return

        # Eksekusi pembelian
        self.__stok[minuman] -= 1
        kembalian = bayar - harga
        
        # POLYMORPHISM BERAKSI DI SINI!
        # Mesin tinggal panggil .proses_keluar(), bentuk aksinya bakal ngikutin jenis minumannya!
        print(minuman.proses_keluar())
        
        if kembalian > 0:
            print(f"💵 Kembalian lu: Rp {kembalian}")
        print("✅ Transaksi Sukses!")


# =====================================================================
# 2. OBJECT (WUJUD NYATA)
# =====================================================================
# Di bagian bawah ini, cetakan Class tadi kita wujudin jadi Object nyata!
if __name__ == "__main__":
    
    print("🛠️ MENGHIDUPKAN VENDING MACHINE...\n" + "="*40)
    
    # Bikin Object Minuman
    pocari = MinumanDingin("Pocari Sweat", 9000)
    kopi = MinumanPanas("Kopi Boss", 12000)
    
    # Bikin Object Mesin
    mesin_stasiun = VendingMachine()
    
    # Masukin stok ke dalam mesin (2 pocari, 1 kopi)
    mesin_stasiun.tambah_minuman(pocari, 2)
    mesin_stasiun.tambah_minuman(kopi, 1)

    # --- SIMULASI PEMBELIAN ---
    
    # Skenario 1: Beli Pocari (sukses)
    mesin_stasiun.beli(pocari, 10000)

    # Skenario 2: Beli Kopi tapi duit kurang
    mesin_stasiun.beli(kopi, 10000)
    
    # Skenario 3: Beli Kopi duit pas
    mesin_stasiun.beli(kopi, 12000)

    # Skenario 4: Maksa beli Kopi lagi padahal stok cuma 1 tadi
    mesin_stasiun.beli(kopi, 50000)