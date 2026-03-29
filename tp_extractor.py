import pandas as pd
import struct

def extract_transponders(file_path):
    # Tespit ettiğimiz değerler
    START_OFFSET = 88352
    RECORD_SIZE = 16
    tps = []

    with open(file_path, 'rb') as f:
        f.seek(START_OFFSET)
        
        # Maksimum 1000 TP tarayalım
        for i in range(1000):
            chunk = f.read(RECORD_SIZE)
            # 0xFF ile başlayanlar boş TP slotlarıdır
            if len(chunk) < RECORD_SIZE or chunk[0] == 0xFF:
                continue
            
            # Byte 0-1: Symbol Rate (Baud)
            baud = struct.unpack('>H', chunk[0:2])[0]
            
            # Byte 14-15: Frekans (MHz)
            freq = struct.unpack('>H', chunk[14:16])[0]
            
            # Byte 11: TP Unique ID (Kanal listesindeki 26. byte burayı işaret eder)
            tp_id = chunk[11]

            # Byte 2: Polarizasyon tahmini (Genelde 0=H, 1=V)
            pol_flag = chunk[2]
            polarization = "V" if pol_flag == 1 else "H"

            if freq > 0:
                tps.append({
                    'TP Index': i,
                    'TP ID': hex(tp_id),
                    'Frekans': freq,
                    'Symbol Rate': baud,
                    'Pol': polarization,
                    'Ham Hex': chunk.hex(' ')
                })

    return pd.DataFrame(tps)

df = extract_transponders('userdb.ssu')
df.to_csv('tp_listesi.csv', index=False, encoding='utf-8-sig')
print("--- TP LİSTESİ (İlk 20) ---")
print(df.head(20))