import os

filename = "userdb.ssu"

def deep_scan(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    print("--- DERİN TARAMA MODU ---")
    
    # 1. MPEG-I Frame Araması (Genelde 00 00 01 B3 ile başlar)
    mpeg_offset = data.find(b'\x00\x00\x01\xb3')
    if mpeg_offset != -1:
        print(f"[!] MPEG Başlangıç Kodu Bulundu! Offset: {mpeg_offset}")
        with open("extracted_logo.m1v", "wb") as out:
            out.write(data[mpeg_offset:mpeg_offset+102400]) # 100KB çıkar

    # 2. Sıkıştırılmış Blok Araması (LZMA Magic Number: ] \x00 \x00)
    lzma_offset = data.find(b'\x5d\x00\x00')
    if lzma_offset != -1:
        print(f"[!] LZMA Sıkıştırılmış Blok İzi! Offset: {lzma_offset}")

    # 3. GIF Araması (GIF89a veya GIF87a)
    if b'GIF8' in data:
        gif_offset = data.find(b'GIF8')
        print(f"[!] GIF Dosyası İzi! Offset: {gif_offset}")

    if mpeg_offset == -1 and lzma_offset == -1:
        print("\n[?] Sonuç: Standart görsel imzası bulunamadı.")
        print("Tahmin: Bu dosya sadece kanal veritabanını içeriyor.")

deep_scan(filename)