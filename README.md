# Etkinlik Kayıt Sistemi

Modern, koyu temalı PyQt5 masaüstü uygulaması. Etkinlik, katılımcı ve bilet yönetimi yapan, JSON tabanlı veri saklayan, tam fonksiyonel bir sistem.

## Özellikler

- **Etkinlik Yönetimi**: Etkinlik ekleme, düzenleme, silme; tarih/kapasite takibi
- **Katılımcı Yönetimi**: Benzersiz e-posta kontrolü ile katılımcı kayıt
- **Bilet Sistemi**: Otomatik bilet kodu üretimi (`BLT-XXXXXXXX` formatında)
- **Kapasite Kontrolü**: Etkinlik kapasitesi dolduğunda kayıt engellenir
- **Katılım Raporu** (ek özellik): Etkinlik bazlı detaylı katılım analizi + CSV dışa aktarım
- **Doluluk Göstergesi**: Renkli progress bar (yeşil → sarı → kırmızı)
- **Arama**: Tüm tablolarda gerçek zamanlı arama
- **Kalıcılık**: JSON dosyalarında otomatik kayıt

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python main.py
```

## Proje Yapısı

```
etkinlik_kayit/
├── main.py                          # Giriş noktası
├── requirements.txt
├── backend/                         # İş mantığı (UI'dan bağımsız)
│   ├── etkinlik.py                 # Etkinlik sınıfı + katilimci_ekle()
│   ├── katilimci.py                # Katılımcı sınıfı + e-posta validasyonu
│   ├── bilet.py                    # Bilet sınıfı + bilet_olustur()
│   └── veri_yoneticisi.py          # Repository / persistence katmanı
├── frontend/                        # PyQt5 UI
│   ├── tema.py                     # QSS stylesheet (koyu tema)
│   ├── ana_pencere.py              # Sidebar + sayfa yığını
│   ├── views/                      # Sayfalar
│   │   ├── dashboard.py
│   │   ├── etkinlikler.py
│   │   ├── katilimcilar.py
│   │   ├── biletler.py
│   │   └── raporlar.py
│   └── widgets/                    # Yeniden kullanılabilir bileşenler
│       ├── bilesenler.py           # IstatistikKart, Kart, DolulukGosterge
│       └── diyaloglar.py           # Form modalları
└── data/                            # JSON veri dosyaları (otomatik oluşur)
    ├── etkinlikler.json
    ├── katilimcilar.json
    └── biletler.json
```

## Sınıf Yapısı (Görev Spesifikasyonu)

### Etkinlik
- Öznitelikler: `etkinlik_id`, `ad`, `tarih`, `kapasite`
- Metod: `katilimci_ekle()`

### Katılımcı
- Öznitelikler: `katilimci_id`, `ad`, `email`

### Bilet
- Öznitelikler: `bilet_id`, `etkinlik`, `katilimci`
- Metod: `bilet_olustur()` (factory)

### Ek Özellik
- Etkinliğe kaç kişi katıldı raporu — `Raporlar` sekmesinde detaylı görünüm + CSV indirme
```
