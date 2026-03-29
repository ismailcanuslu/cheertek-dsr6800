import pandas as pd
import struct

def extract_satellites(file_path):
    # Tespit ettiğimiz değerler
    START_OFFSET = 108388
    RECORD_SIZE = 36
    sats = []

    with open(file_path, 'rb') as f:
        f.seek(START_OFFSET)
        
        # Maksimum 100 uydu tarayalım (Genelde limit budur)
        for i in range(100):
            chunk = f.read(RECORD_SIZE)
            if len(chunk) < RECORD_SIZE or chunk[0] == 0x00:
                break
            
            # Byte 0-15: Uydu Adı (String)
            name = chunk[:16].split(b'\x00')[0].decode('ascii', errors='ignore').strip()
            
            # Byte 20-21: Yörünge Pozisyonu (420 = 42.0)
            pos_raw = struct.unpack('>H', chunk[20:22])[0]
            position = pos_raw / 10.0
            
            # Byte 16-19: LNB Frekansları
            lnb_high = struct.unpack('>H', chunk[16:18])[0]
            lnb_low = struct.unpack('>H', chunk[18:20])[0]

            # Byte 31: Uydu Index/ID (Kanal listesiyle bağlanan ID)
            sat_id = chunk[31]

            sats.append({
                'Index': i,
                'Uydu Adı': name,
                'Pozisyon': f"{position}E",
                'LNB High': lnb_high,
                'LNB Low': lnb_low,
                'Internal ID': hex(sat_id)
            })

    return pd.DataFrame(sats)

df = extract_satellites('userdb.ssu')
df.to_csv('uydu_listesi.csv', index=False, encoding='utf-8-sig')
print("--- UYDU LİSTESİ ---")
print(df)