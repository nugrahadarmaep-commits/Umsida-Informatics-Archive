def f(x):
    return x**3 - 2 * x - 5

def main():
    print("\n" + "➖" * 35)
    print("🚨 PROGRAM METNUM - REGULA FALSI  🚨".center(70))
    print("➖" * 35)

    # fungsi persamaan polinemial non linier
    print("Fungsi      : f(x) = x^3 - 2x - 5")

    try:
        a = float(input("MASUKKAN BATAS FUNGSI BAWAH (a) : "))
        b = float(input("MASUKAN BATAS FUNGSI ATAS (b)  : "))
        max_iter = 20
        print(f"jumlah iterasi otomatis {max_iter}")
    except ValueError:
        print("\n[Peringatan] Masukan angka yang sesaui! Program berhenti!")
        return

    if a >= b:
        print(
            "\n[Peringatan] Batas atas harus lebih besar dari batas bawah! Program berhenti karena salah input pada angka"
        )
        return

    print("=" * 60)

    if f(a) * f(b) >= 0:
        print(
            "\n[Peringatan] Interval tidak sesuai! Syarat f(a) * f(b) < 0 tidak terpenuhi."
        )
        print("Cari angka lain yang pas, program berhenti.\n")
        return

    print("\n" + "=" * 60)
    print(" PENYELESAIAN PER ITERASI".center(60))
    print("=" * 60)

    c_lama = 0.0
    # List buat nyimpen data yang bakal di-print di tabel akhir
    data_tabel = []

    for i in range(1, max_iter + 1):
        fa = f(a)
        fb = f(b)

        # Rumus utama Regula Falsi.
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        # Hitung Error
        if i == 1:
            error_str = "-"
        else:
            error_persen = abs((c - c_lama) / c) * 100
            error_str = f"{error_persen:.6f} %"

        # Output yang dikeluarkan di terminal memberikan penjelasan langkah per iterasi
        print(f"✅ ITERASI KE-{i}")
        print(f"  • a    = {a:.6f}  =>  f(a) = ({a:.6f})^3 - 2({a:.6f}) - 5 = {fa:.6f}")
        print(f"  • b    = {b:.6f}  =>  f(b) = ({b:.6f})^3 - 2({b:.6f}) - 5 = {fb:.6f}")
        print(f"  • Cari Nilai c (Akar):")
        print(f"    c    = (a * f(b) - b * f(a)) / (f(b) - f(a))")
        print(
            f"    c    = ({a:.6f} * {fb:.6f} - {b:.6f} * {fa:.6f}) / ({fb:.6f} - {fa:.6f})"
        )
        print(f"    c    = {c:.6f}")
        print(f"  • Evaluasi f(c):")
        print(f"    f(c) = ({c:.6f})^3 - 2({c:.6f}) - 5 = {fc:.6f}")
        print(f"  • Error = {error_str}")

        # Simpan data buat tabel rekap di bawah
        data_tabel.append([i, a, b, fa, fb, c, fc, error_str])

        # Syarat pemindahan sebuah interval
        if fa * fc < 0:
            print("  • Karena f(a) * f(c) < 0, maka b baru diganti jadi c")
            b = c
        else:
            print("  • Karena f(a) * f(c) > 0, maka a baru diganti jadi c")
            a = c

        c_lama = c
        print("-" * 60)

    print("\n" + "=" * 105)
    print("📊 REKAPAN TABEL HASIL AKHIR 📊".center(105))
    print("=" * 105)
    print(
        f"{'Iter':<5} | {'a':<10} | {'b':<10} | {'f(a)':<10} | {'f(b)':<10} | {'c (Akar)':<10} | {'f(c)':<10} | {'Error (%)':<15}"
    )
    print("-" * 105)
    for row in data_tabel:
        print(
            f"{row[0]:<5} | {row[1]:<10.6f} | {row[2]:<10.6f} | {row[3]:<10.6f} | {row[4]:<10.6f} | {row[5]:<10.6f} | {row[6]:<10.6f} | {row[7]:<15}"
        )
    print("-" * 105)
    print(
        f"🎉 Akar persamaan hampiran (c) pada iterasi ke-{max_iter} adalah : {c_lama:.6f} 🎉"
    )
    print("=" * 105 + "\n")


if __name__ == "__main__":
    main()
