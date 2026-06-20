import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def jalankan_scraping():
    print("Mulai proses scraping ke UMSIDA...")
    
    # DETERMINING THE TARGET WEBSITE THAT I WILL SCRAPING
    url = "https://admisi.umsida.ac.id/fortama/"

    # SEBAGAI KIRIM KURIR (REQUESTS)
    response = requests.get(url)

    # MEMBEDAH ISI WEB (SOUP)
    soup = BeautifulSoup(response.text, 'html.parser')

    # MENCARI DATA SPESIFIK
    table = soup.find('table') 

    # MENGAMBIL BARIS-BARISNYA (LOOPING)
    rows = table.find_all('tr')
    list_data = []

    for row in rows:
        cols = row.find_all('td')
        cols = [data.text.strip() for data in cols]
        if cols: 
            list_data.append(cols)
            
    # MENKONVERSI KE TABEL PANDAS
    df = pd.DataFrame(list_data)

    # MENG-EKSPOR KE FILE CSV & JSON
    df.to_csv('tugas_akhir.csv', index=False)
    df.to_json('tugas_akhir.json', orient='records', indent=4)

    # MEMBACA HASIL JSON UNTUK DIKIRIM KE SERVER
    with open('tugas_akhir.json', 'r', encoding='utf-8') as f:
        data_json = f.read()
        
    print("Scraping selesai, data siap dikirim ke web!")
    return data_json

# Baris ini gunanya biar script tetap bisa dites jalan sendiri tanpa server
if __name__ == "__main__":
    jalankan_scraping()