import ephem
import json

# 1. SETUP LOKASI (Sidokumpul, Sidoarjo)
observer = ephem.Observer()
observer.lat = '-7.4478'  
observer.lon = '112.7183' 
observer.elevation = 10   

# 2. SETUP WAKTU
observer.date = '2026/5/3 11:00:28' 

# KOMPUTASI POSISI BULAN
bulan = ephem.Moon()
bulan.compute(observer)

# OUTPUT JSON (Biar kelihatan expert)
data_hisab = {
    "status": "200 OK",
    "metode": "Komputasi Hisab Python",
    "waktu_wib": "2026-05-03 18:00:28",
    "hasil_koordinat": {
        "target": "Moon",
        "altitude": str(bulan.alt),
        "azimuth": str(bulan.az),
        "illuminasi_persen": round(bulan.phase, 2)
    }
}

print(json.dumps(data_hisab, indent=4))