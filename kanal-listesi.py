import pandas as pd
import struct

def parse_full_database(file_path):
    # --- ADIM 1: TP TABLOSUNU HAFIZAYA AL (Apartmanlar) ---
    tp_table = {}
    tp_start = 88352
    tp_stride = 16
    
    with open(file_path, 'rb') as f:
        f.seek(tp_start)
        for i in range(256): # Maksimum 256 TP varsayımı
            chunk = f.read(tp_stride)
            if len(chunk) < tp_stride or chunk[0] == 0xFF: break
            
            baud = struct.unpack('>H', chunk[0:2])[0]
            # TP ID genellikle byte 11'dedir veya direkt dizin (index) sırasıdır
            tp_id = chunk[11] 
            freq = struct.unpack('>H', chunk[14:16])[0]
            
            # Bu cihazda TP ID mi yoksa Index mi kullanılıyor test etmek için ikisini de tutalım
            tp_table[tp_id] = {"Frekans": freq, "Baud": baud}
            tp_table[i] = {"Frekans": freq, "Baud": baud} # Fallback as index

    # --- ADIM 2: KANAL LİSTESİNİ OKU VE TP İLE BİRLEŞTİR (Daireler) ---
    channels = []
    ch_stride = 44
    ch_start = 68

    with open(file_path, 'rb') as f:
        f.seek(ch_start)
        while True:
            chunk = f.read(ch_stride)
            if len(chunk) < ch_stride or chunk[0] in [0x00, 0xFF]: break
            
            name = chunk[:20].split(b'\x00')[0].decode('ascii', errors='ignore').strip()
            sid = struct.unpack('>H', chunk[20:22])[0]
            v_pid = struct.unpack('>H', chunk[26:28])[0] & 0x1FFF
            a_pid = struct.unpack('>H', chunk[24:26])[0] & 0x1FFF
            
            # Kanalın bağlı olduğu TP Index (Offset 26. byte)
            tp_ptr = chunk[26] 
            
            # TP Bilgilerini Join Et
            tp_info = tp_table.get(tp_ptr, {"Frekans": 0, "Baud": 0})
            
            is_encrypted = "Şifreli ($)" if (chunk[30] & 0x20) else "Açık (FTA)"

            channels.append({
                'Kanal Adı': name,
                'Frekans (MHz)': tp_info['Frekans'],
                'Sembol Oranı (Baud)': tp_info['Baud'],
                'Durum': is_encrypted,
                'SID': sid,
                'V-PID': v_pid,
                'A-PID': a_pid,
                'TP ID (Pointer)': hex(tp_ptr),
                'Raw': chunk[20:34].hex(' ')
            })

    return pd.DataFrame(channels)

# Çalıştır ve Mac'te Numbers ile açmak için kaydet
df = parse_full_database('userdb.ssu')
df.to_csv('Hacked_Kanal_Listesi.csv', index=False, encoding='utf-8-sig')
print(f"--- BAŞARIYLA BİRLEŞTİRİLDİ ---")
print(df[['Kanal Adı', 'Frekans (MHz)', 'Sembol Oranı (Baud)', 'Durum']].head(20))