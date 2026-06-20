import codecs

def pecahkan_sandi():
    print("="*40)
    print("Alat Pemecah Sandi Rahasia (ROT13)")
    print("="*40)
    
    # Teks rahasia dari tugas Anda
    ciphertext = "Gur dhvpx oebja sbk whzcf bire gur ynml qbt"
    
    # Python memiliki library bawaan 'codecs' yang sangat praktis untuk ROT13
    plaintext = codecs.decode(ciphertext, 'rot_13')
    
    print(f"Teks Rahasia  : {ciphertext}")
    print(f"Hasil Dekripsi: {plaintext}")
    print("\nPenjelasan:")
    print("Huruf 'G' digeser 13 kali menjadi 'T'.")
    print("Huruf 'u' digeser 13 kali menjadi 'h'.")
    print("Dan seterusnya...")

# menjalankan program
pecahkan_sandi()