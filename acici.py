import lzma

def fix_and_decompress():
    input_file = "data.lzma"
    output_file = "decompressed_data.bin"
    
    print(f"[*] {input_file} üzerinde 'Header Patching' yapılıyor...")
    
    try:
        with open(input_file, "rb") as f:
            # data.lzma zaten '5d 00 00 00 01' (örnek) ile başlıyor
            raw_data = f.read()
        
        # LZMA ALONE formatı için: 
        # İlk 5 byte (Properties) + 8 byte (0xFF -> Unknown Size) + Payload
        properties = raw_data[:5]
        payload = raw_data[5:]
        dummy_size = b'\xff' * 8
        
        fixed_data = properties + dummy_size + payload
        
        # Yama yapılmış veriyi açmaya çalış
        decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        decompressed = decompressor.decompress(fixed_data)
        
        with open(output_file, "wb") as f:
            f.write(decompressed)
            
        print(f"[✔] BAŞARILI! '{output_file}' oluşturuldu.")
        print(f"    Yeni Boyut: {len(decompressed)} byte")

    except Exception as e:
        print(f"[X] Hata: {e}")
        print("\nİpucu: Eğer hala hata veriyorsa, 'skip=19361' ofsetinde bir kayma olabilir.")
        print("HxD veya Hex Fiend ile 19361 adresine bakıp '5d 00 00'ın tam yerini teyit et.")

if __name__ == "__main__":
    fix_and_decompress()