"""
Otomatik seed - Eğer data klasörü boşsa örnek verilerle doldurur.
Bu sayede uygulamayı ilk açan kişi dolu bir sistemle karşılaşır.
"""
from datetime import datetime, timedelta

from .veri_yoneticisi import VeriYoneticisi


def seed_gerekli_mi(vy: VeriYoneticisi) -> bool:
    """Sistem boşsa True döner."""
    return (
        len(vy.tum_etkinlikler()) == 0
        and len(vy.tum_katilimcilar()) == 0
        and len(vy.tum_biletler()) == 0
    )


def seed_uygula(vy: VeriYoneticisi) -> None:
    """Boş bir VeriYoneticisi'ye örnek veriler yükler."""
    simdi = datetime.now()

    # ETKİNLİKLER (hepsi gelecekte)
    e1 = vy.etkinlik_ekle(
        "Python ile Web Geliştirme Workshop",
        simdi + timedelta(days=14, hours=2), 30,
    )
    e2 = vy.etkinlik_ekle(
        "AI ve Machine Learning Konferansı",
        simdi + timedelta(days=28, hours=4), 100,
    )
    e3 = vy.etkinlik_ekle(
        "React Native Mobile Bootcamp",
        simdi + timedelta(days=42), 25,
    )
    e4 = vy.etkinlik_ekle(
        "Cybersecurity Sempozyumu 2026",
        simdi + timedelta(days=60), 80,
    )
    e5 = vy.etkinlik_ekle(
        "Game Development Meetup",
        simdi + timedelta(days=7, hours=6), 40,
    )
    e6 = vy.etkinlik_ekle(
        "DevOps & Cloud Native Day",
        simdi + timedelta(days=21), 60,
    )
    e7 = vy.etkinlik_ekle(
        "Frontend Performance Talks",
        simdi + timedelta(days=10), 50,
    )

    # KATILIMCILAR
    katilimcilar = [
        ("Beko Yılmaz", "beko.yilmaz@gmail.com"),
        ("Ali Demir", "ali.demir@hotmail.com"),
        ("Ayşe Kaya", "ayse.kaya@outlook.com"),
        ("Mehmet Şahin", "mehmet.sahin@gmail.com"),
        ("Zeynep Arslan", "zeynep.arslan@yahoo.com"),
        ("Can Öztürk", "can.ozturk@protonmail.com"),
        ("Selin Yıldız", "selin.yildiz@gmail.com"),
        ("Murat Koç", "murat.koc@outlook.com"),
        ("Elif Çelik", "elif.celik@gmail.com"),
        ("Burak Aydın", "burak.aydin@hotmail.com"),
        ("Deniz Kara", "deniz.kara@gmail.com"),
        ("Ece Yıldırım", "ece.yildirim@outlook.com"),
        ("Kerem Aksoy", "kerem.aksoy@gmail.com"),
        ("Pınar Doğan", "pinar.dogan@yahoo.com"),
        ("Tolga Erdem", "tolga.erdem@gmail.com"),
        ("Beril Şen", "beril.sen@hotmail.com"),
        ("Onur Polat", "onur.polat@gmail.com"),
        ("Sıla Avcı", "sila.avci@outlook.com"),
        ("Emre Tunç", "emre.tunc@gmail.com"),
        ("Gizem Yalçın", "gizem.yalcin@protonmail.com"),
        ("Berk Çetin", "berk.cetin@gmail.com"),
        ("Naz Bulut", "naz.bulut@yahoo.com"),
        ("Cem Korkmaz", "cem.korkmaz@gmail.com"),
        ("Defne Erol", "defne.erol@outlook.com"),
        ("Yiğit Aslan", "yigit.aslan@gmail.com"),
    ]
    for ad, email in katilimcilar:
        vy.katilimci_ekle(ad, email)

    ks = vy.tum_katilimcilar()

    # BİLETLER - farklı doluluk seviyelerinde
    def bilet_grubu(etkinlik, kid_baslangic, adet):
        for k in ks[kid_baslangic:kid_baslangic + adet]:
            try:
                vy.bilet_olustur(etkinlik.etkinlik_id, k.katilimci_id)
            except ValueError:
                pass

    bilet_grubu(e1, 0, 18)   # Python WS - 18/30  (60%)
    bilet_grubu(e2, 0, 22)   # AI Konf - 22/100  (22%)
    bilet_grubu(e3, 0, 24)   # React Native - 24/25 (96% - AZ KALDI)
    bilet_grubu(e4, 0, 12)   # Cyber - 12/80   (15%)
    bilet_grubu(e5, 0, 40)   # Game Dev - 40/40 (DOLU)
    bilet_grubu(e6, 0, 8)    # DevOps - 8/60   (13%)
    bilet_grubu(e7, 0, 15)   # Frontend - 15/50 (30%)
