import requests
from bs4 import BeautifulSoup
import pandas as pd

# DETERMINING THE TARGET WEBSITE THAT I WILL SCRAPPING
url = "https://admisi.umsida.ac.id/fortama/"

# B. KIRIM KURIR (REQUESTS)
response = requests.get(url)

# C. BEDAH ISI WEB (SOUP)
soup = BeautifulSoup(response.text, 'html.parser')

# D. CARI DATA SPESIFIK
# Misal kita cari semua tabel
table = soup.find('table') 

# E. AMBIL BARIS-BARISNYA (LOOPING)
rows = table.find_all('tr')
list_data = []

for row in rows:
    # Ambil tiap kolom (td) di dalam baris
    cols = row.find_all('td')
    # Bersihin spasi dan teks nggak penting
    cols = [data.text.strip() for data in cols]
    if cols: # Cek biar baris kosong gak ikut
        list_data.append(cols)
        
# F. KONVERSI KE TABEL PANDAS
df = pd.DataFrame(list_data)

# G. EKSPOR KE FILE
df.to_csv('tugas_akhir.csv', index=False)
df.to_json('tugas_akhir.json', orient='records', indent=4)

print("YOU CAN CHECK MY FOLDER")