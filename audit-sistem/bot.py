import subprocess
import re

print("=========================================================")
print("[INFO] Memulai proses automasi Nikko Puzzle...")
print("[INFO] Menjalankan sistem dan menghubungkan ke game...\n")
print("==========================================================")

game = subprocess.Popen(
    ['nikko_puzzle_windows_amd64.exe'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, bufsize=1
)

def baca_soal():
    output = ""
    while True:
        char = game.stdout.read(1)
        if not char: break
        output += char
        if "Answer:" in output or "Aborting" in output or "Time's up" in output:
            return output

# --- AUTO LOGIN ---
game.stdin.write("2\n")
game.stdin.flush()
game.stdin.write("Darma Nugraha\n")
game.stdin.flush()
game.stdin.write("241080200074\n")
game.stdin.flush()

# --- LOOPING 100 SOAL ---
for i in range(1, 101):
    soal_mentah = baca_soal()
    
    if not soal_mentah or "Aborting" in soal_mentah:
        print("\n[PERINGATAN] Proses terhenti. Permainan berakhir atau waktu habis.")
        break
        
    print(f"\n[SOAL {i}] Mendapatkan Pertanyaan:\n{soal_mentah.strip()}")
    
    # PARSING TEXT
    if "Question" in soal_mentah:
        teks_inti = soal_mentah.split("Question")[1].lower()
    else:
        teks_inti = soal_mentah.lower()
        
    angka = re.findall(r'\d+', teks_inti)
    jawaban = "0"
    
    try:
        if "persegi panjang" in teks_inti:
            panjang = int(angka[2])
            lebar = int(angka[3])
            if "luas" in teks_inti:
                jawaban = str(panjang * lebar)
            elif "keliling" in teks_inti:
                jawaban = str(2 * (panjang + lebar))
                
        elif "persegi" in teks_inti:
            sisi = int(angka[2]) 
            if "luas" in teks_inti:
                jawaban = str(sisi * sisi)
            elif "keliling" in teks_inti:
                jawaban = str(4 * sisi)
                
        elif "segitiga" in teks_inti:
            if "luas" in teks_inti:
                alas = int(angka[2])
                tinggi = int(angka[3])
                jawaban = str(int(0.5 * alas * tinggi))
            elif "keliling" in teks_inti: 
                sisi = int(angka[2])
                jawaban = str(3 * sisi)

        elif "lingkaran" in teks_inti:
            jari_jari = int(angka[2])
            if "luas" in teks_inti:
                # Rumus: (22 * r * r) / 7
                jawaban = str(int((22 * jari_jari * jari_jari) / 7))
            elif "keliling" in teks_inti:
                # Rumus: (2 * 22 * r) / 7
                jawaban = str(int((2 * 22 * jari_jari) / 7))

        elif "kubus" in teks_inti and "volume" in teks_inti:
            sisi = int(angka[2])
            jawaban = str(sisi * sisi * sisi)
            
        elif "balok" in teks_inti and "volume" in teks_inti:
            panjang = int(angka[2])
            lebar = int(angka[3])
            tinggi = int(angka[4])
            jawaban = str(panjang * lebar * tinggi)
            
        else:
            jawaban = "0" 
            
    except IndexError:
        jawaban = "0"

    print(f"[SISTEM] Mengirimkan jawaban: {jawaban}")
    game.stdin.write(f"{jawaban}\n")
    game.stdin.flush()

print("\n[INFO] Proses eksekusi selesai. Silakan periksa hasil Anda.")