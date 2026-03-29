# 🛰️ Cheertek DVB-S Binary Data Research (DSR-6800)

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)
![.NET](https://img.shields.io/badge/.NET-8.0-purple?style=for-the-badge&logo=dotnet)
![Status](https://img.shields.io/badge/Status-Research_Phase-orange?style=for-the-badge)
![Field](https://img.shields.io/badge/Field-Embedded_Systems-red?style=for-the-badge)

Bu proje, **Cheertek CT216S** tabanlı uydu alıcılarının `userdb.ssu` (445 KB) veritabanı dosyası üzerinde gerçekleştirilen derinlemesine tersine mühendislik (reverse engineering) çalışmasını içerir. Bir "black box" olarak görülen binary dosyanın içindeki yapısal kurallar, byte-level analizlerle deşifre edilmiştir.

---

## 🔍 Proje Özeti ve Kazanımlar

Bu çalışma sırasında ham veri (raw data) üzerinden anlamlı bilgi setleri (datasets) üretilmiş ve gömülü sistemlerin veri saklama mantığı çözülmüştür.

- **Entropy Analysis:** Verinin sıkıştırma oranları incelenerek LZMA ve GZIP imzaları (Magic Numbers) üzerinden "sıkıştırılmış paket" avı yapıldı.
- **Pattern Recognition:** Tekrar eden byte dizilimleri üzerinden veritabanı şeması (Schema) çıkarıldı.
- **Embedded Logic:** Verinin RAM üzerindeki hizalaması (alignment) ve RTOS (Real-Time Operating System) katmanındaki veri işleme mantığı kavrandı.
- **Low-Level Debugging:** `hexdump` ve `binwalk` araçları kullanılarak dosya ofsetleri üzerinden veri cerrahisi uygulandı.

---

## 🛠️ Kullanılan Araçlar (Toolchain)

| Araç | Kullanım Amacı |
| :--- | :--- |
| **Hexdump & Strings** | Binary dosyanın görselleştirilmesi ve gizli metinlerin (DDR_FREQ, HW_VER) tespiti. |
| **Grep (Regex)** | Belirli frekansların (Türksat 42.0E) ve imzaların (5D 00 00) tespiti. |
| **Binwalk** | Firmware içindeki gizli dosya sistemlerinin ve sıkıştırma bloklarının (LZMA) analizi. |
| **Python (Struct)** | Ham byte'ları insan tarafından okunabilir CSV formatına dönüştüren Parser yazımı. |

---

## 📐 Keşfedilen Veri Kuralları (The Laws of 6800)

Analizler sonucunda cihazın veriyi saklarken kullandığı **"Fixed-Stride"** yapısı deşifre edilmiştir:

### 1. Uydu Tablosu (The 36-Byte Rule)
Her uydu kaydı tam olarak $36 \text{ byte}$ uzunluğundadır.
- **Offset 20-21:** Orbital Position (Örn: $420 \rightarrow 42.0^\circ$E).
- **Offset 16-19:** LNB High/Low frekans parametreleri.

### 2. Transponder Tablosu (The 16-Byte Rule)
Her TP kaydı $16 \text{ byte}$ uzunluğunda dinamik bir dizidir.
- **Header:** Symbol Rate (Baud) verisiyle başlar.
- **Footer:** MHz cinsinden frekans değeriyle biter.

### 3. Kanal Tablosu (The 44-Byte Rule)
Ana kanal listesi $44 \text{ byte}$'lık devasa bir `struct` dizisidir.
- **Padding Logic:** Cihazın 4000 kanal kapasitesi için ayrılan alan, kullanılmayan slotlarda `0x00` padding ile rezerve edilmiştir.

---

## 🚀 Gelecek Vizyonu (Roadmap)

- [ ] **Server-Client Simulation:** Çözülen bu yapıyı bir simülatör üzerinden sanal bir uydu yayınına bağlamak.
- [ ] **RTOS Layer Implementation:** Kendi mini "işletim sistemi" katmanımı yazarak, ilgili veriyi ilgili HEX adresine doğrudan yazan bir patcher geliştirmek.
- [ ] **Binary Patching:** .NET üzerinden Checksum hesaplamalı, hata payı sıfır bir Channel Editor yazılımı.

---

## 👨‍💻 Mühendislik Notu
Bu çalışma, bir 4. sınıf bilgisayar mühendisi olarak **debugging**, **binary manipulation** ve **low-level programming** becerilerimi uç noktaya taşımıştır. Bir dosyanın sadece veri değil, bir donanımın "vasiyeti" olduğunu öğrenmek muazzam bir tecrübeydi.

---
**Developed by [İsmailcan Uslu](https://github.com/ismailcanuslu)** *Erzurum Technical University - Computer Engineering*
