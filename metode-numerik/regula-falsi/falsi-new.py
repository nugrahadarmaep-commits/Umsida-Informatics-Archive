def f(x):
    return x**3 - 2*x - 5

def main():
    # Header
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + "🚨 PROGRAM METODE NUMERIK - REGULA FALSI 🚨".center(70) + "║")
    print("╚" + "═"*70 + "╝")
    
    print(" 📌 Fungsi : f(x) = x^3 - 2x - 5\n") 
    
    try:
        a = float(input(" ➔ Masukkan batas bawah (a) : "))
        b = float(input(" ➔ Masukkan batas atas (b)  : "))
        max_iter = 20 
        print(f" ➔ Jumlah iterasi otomatis  : {max_iter}\n")
    except ValueError:
        print(" ❌ [ERROR] Masukkan angka yang sesuai! Program berhenti.")
        return

    if a >= b:
      print(" ❌ [ERROR] Batas atas (b) harus lebih besar dari batas bawah (a)!")
      return
      
    if f(a) * f(b) >= 0:
        print(" ❌ [ERROR] Interval tidak sesuai! Syarat f(a) * f(b) < 0 tidak terpenuhi.")
        return
        
    # Section Iterasi
    print("╔" + "═"*70 + "╗")
    print("║" + "PENYELESAIAN LANGKAH DEMI LANGKAH".center(70) + "║")
    print("╚" + "═"*70 + "╝")

    c_lama = 0.0
    data_tabel = []

    for i in range(1, max_iter + 1):
        fa = f(a)
        fb = f(b)
        
        # Rumus utama Regula Falsi
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        
        # Hitung Error
        if i == 1:
            error_str = "-"
        else:
            error_persen = abs((c - c_lama) / c) * 100
            error_str = f"{error_persen:.6f}"
        
        # Tampilan langkah per iterasi yang lebih menjorok dan rapi
        print(f"\n 🔄 ITERASI KE-{i}")
        print(f"    • a = {a:<9.6f} =>  f(a) = {fa:.6f}")
        print(f"    • b = {b:<9.6f} =>  f(b) = {fb:.6f}")
        print(f"    • c = ({a:.6f} * {fb:.6f} - {b:.6f} * {fa:.6f}) / ({fb:.6f} - {fa:.6f})")
        print(f"    • c = {c:<9.6f} =>  f(c) = {fc:.6f}")
        
        if error_str == "-":
            print(f"    • Error = {error_str}")
        else:
            print(f"    • Error = {error_str} %")
        
        # Simpan data buat tabel rekap
        data_tabel.append([i, a, b, fa, fb, c, fc, error_str])
        
        # Cek akar eksak
        if fc == 0:
            print(f"    🎯 BINGO! Akar eksak ditemukan pada iterasi ke-{i} (f(c) = 0)")
            c_lama = c
            break

        # Logika pindah interval
        if fa * fc < 0:
            print("    👉 Karena f(a) * f(c) < 0, maka batas (b) bergeser menjadi (c)")
            b = c
        else:
            print("    👉 Karena f(a) * f(c) > 0, maka batas (a) bergeser menjadi (c)")
            a = c
            
        c_lama = c

    # ==========================================
    # TABEL REKAPAN SUPER ESTETIK (ASCII BOX)
    # ==========================================
    print("\n" + "╔" + "═"*111 + "╗")
    print("║" + "📊 REKAPAN TABEL HASIL AKHIR REGULA FALSI 📊".center(111) + "║")
    print("╠" + "═"*7 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*18 + "╣")
    print("║ Iter  ║     a      ║     b      ║    f(a)    ║    f(b)    ║  c (Akar)  ║    f(c)    ║     Error (%)    ║")
    print("╠" + "═"*7 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*18 + "╣")
    
    for row in data_tabel:
        # Merapikan output persen agar sejajar
        err_display = f"{row[7]} %" if row[7] != "-" else "-"
        print(f"║ {row[0]:<5} ║ {row[1]:>10.6f} ║ {row[2]:>10.6f} ║ {row[3]:>10.6f} ║ {row[4]:>10.6f} ║ {row[5]:>10.6f} ║ {row[6]:>10.6f} ║ {err_display:>16} ║")
        
    print("╚" + "═"*7 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*18 + "╝")
    
    # Kesimpulan Akhir
    print(f"\n 🎉 Akar persamaan hampiran (c) pada iterasi terakhir adalah : {c_lama:.6f} 🎉\n")

if __name__ == "__main__":
    main()