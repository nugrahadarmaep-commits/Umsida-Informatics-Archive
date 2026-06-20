def hitung_faraidh():
    print("="*50)
    print("Kalkulator Waris Islam (Faraidh) Keluarga Inti")
    print("="*50)
    
    # 1. Input Dinamis dari User
    try:
        harta = float(input("Masukkan total harta warisan (Rp): "))
        print("\n--- Masukkan Anggota Keluarga yang Ditinggalkan ---")
        suami = int(input("Apakah ada Suami? (1 jika ya, 0 jika tidak): "))
        istri = int(input("Berapa jumlah Istri? (0-4): "))
        bapak = int(input("Apakah ada Bapak? (1 jika ya, 0 jika tidak): "))
        ibu = int(input("Apakah ada Ibu? (1 jika ya, 0 jika tidak): "))
        anak_laki = int(input("Berapa jumlah Anak Laki-laki?: "))
        anak_pr = int(input("Berapa jumlah Anak Perempuan?: "))
    except ValueError:
        print("Mohon masukkan angka yang valid!")
        return

    # 2. Logika Dasar Pembagian
    ada_anak = (anak_laki > 0) or (anak_pr > 0)
    pembagian = {}
    sisa_harta = harta

    # Hak Suami / Istri
    if suami == 1:
        porsi_suami = 1/4 if ada_anak else 1/2
        pembagian['Suami'] = harta * porsi_suami
        sisa_harta -= pembagian['Suami']
    elif istri > 0:
        porsi_istri = (1/8 if ada_anak else 1/4) / istri
        pembagian['Istri (Masing-masing)'] = harta * porsi_istri
        sisa_harta -= (pembagian['Istri (Masing-masing)'] * istri)

    # Hak Ibu
    if ibu == 1:
        porsi_ibu = 1/6 if ada_anak else 1/3
        pembagian['Ibu'] = harta * porsi_ibu
        sisa_harta -= pembagian['Ibu']

    # Hak Bapak
    if bapak == 1:
        porsi_bapak = 1/6 if ada_anak else 0 # Jika tidak ada anak, bapak jadi Asabah (mengambil sisa)
        nilai_bapak = harta * porsi_bapak
        pembagian['Bapak'] = nilai_bapak
        sisa_harta -= nilai_bapak

    # Hak Anak (Asabah - Sisa Harta)
    # Aturan: Anak Laki-laki mendapat 2x lipat porsi Anak Perempuan
    if ada_anak:
        total_bagian_anak = (anak_laki * 2) + (anak_pr * 1)
        if total_bagian_anak > 0:
            nilai_per_bagian = sisa_harta / total_bagian_anak
            if anak_laki > 0:
                pembagian['Anak Laki-laki (Masing-masing)'] = nilai_per_bagian * 2
            if anak_pr > 0:
                pembagian['Anak Perempuan (Masing-masing)'] = nilai_per_bagian
            sisa_harta = 0 # Harta habis dibagi ke anak

    # Bapak mengambil sisa jika tidak ada keturunan laki-laki (Asabah Bapak)
    if bapak == 1 and sisa_harta > 0 and anak_laki == 0:
        pembagian['Bapak'] += sisa_harta
        sisa_harta = 0

    # 3. Menampilkan Hasil
    print("\n" + "="*50)
    print("HASIL PEMBAGIAN WARISAN")
    print("="*50)
    print(f"Total Harta: Rp {harta:,.2f}")
    print("-" * 50)
    for ahli_waris, nilai in pembagian.items():
        if nilai > 0:
            print(f"> {ahli_waris:<30}: Rp {nilai:,.2f}")
    
    if sisa_harta > 0.1: # Toleransi pembulatan desimal
        print(f"\n*Sisa harta (bisa masuk ke Baitul Mal / radd): Rp {sisa_harta:,.2f}")

# menjalankan program 
hitung_faraidh()