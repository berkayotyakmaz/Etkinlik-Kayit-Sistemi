"""
Veri Yöneticisi - Tüm modellerin merkezi yönetimi ve JSON tabanlı kalıcılık.
Repository pattern ile tüm CRUD operasyonlarını yürütür.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .etkinlik import Etkinlik
from .katilimci import Katilimci
from .bilet import Bilet


class VeriYoneticisi:
    """
    Tüm uygulama verilerini yöneten singleton-benzeri sınıf.
    Veriler JSON dosyalarında saklanır.
    """

    def __init__(self, veri_klasoru: str = "data"):
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self.etkinlikler_dosya = os.path.join(veri_klasoru, "etkinlikler.json")
        self.katilimcilar_dosya = os.path.join(veri_klasoru, "katilimcilar.json")
        self.biletler_dosya = os.path.join(veri_klasoru, "biletler.json")

        self._etkinlikler: Dict[int, Etkinlik] = {}
        self._katilimcilar: Dict[int, Katilimci] = {}
        self._biletler: Dict[int, Bilet] = {}

        self._sonraki_etkinlik_id = 1
        self._sonraki_katilimci_id = 1
        self._sonraki_bilet_id = 1

        self._yukle()

    # ---------------- KALICILIK ----------------

    def _yukle(self) -> None:
        """JSON dosyalarından verileri yükler."""
        if os.path.exists(self.etkinlikler_dosya):
            try:
                with open(self.etkinlikler_dosya, "r", encoding="utf-8") as f:
                    veri = json.load(f)
                    for d in veri:
                        e = Etkinlik.from_dict(d)
                        self._etkinlikler[e.etkinlik_id] = e
                        self._sonraki_etkinlik_id = max(
                            self._sonraki_etkinlik_id, e.etkinlik_id + 1
                        )
            except (json.JSONDecodeError, KeyError, ValueError) as ex:
                print(f"[UYARI] Etkinlikler dosyası okunamadı: {ex}")

        if os.path.exists(self.katilimcilar_dosya):
            try:
                with open(self.katilimcilar_dosya, "r", encoding="utf-8") as f:
                    veri = json.load(f)
                    for d in veri:
                        k = Katilimci.from_dict(d)
                        self._katilimcilar[k.katilimci_id] = k
                        self._sonraki_katilimci_id = max(
                            self._sonraki_katilimci_id, k.katilimci_id + 1
                        )
            except (json.JSONDecodeError, KeyError, ValueError) as ex:
                print(f"[UYARI] Katılımcılar dosyası okunamadı: {ex}")

        if os.path.exists(self.biletler_dosya):
            try:
                with open(self.biletler_dosya, "r", encoding="utf-8") as f:
                    veri = json.load(f)
                    for d in veri:
                        b = Bilet.from_dict(d)
                        self._biletler[b.bilet_id] = b
                        self._sonraki_bilet_id = max(
                            self._sonraki_bilet_id, b.bilet_id + 1
                        )
            except (json.JSONDecodeError, KeyError, ValueError) as ex:
                print(f"[UYARI] Biletler dosyası okunamadı: {ex}")

    def kaydet(self) -> None:
        """Tüm verileri JSON dosyalarına yazar."""
        with open(self.etkinlikler_dosya, "w", encoding="utf-8") as f:
            json.dump(
                [e.to_dict() for e in self._etkinlikler.values()],
                f,
                ensure_ascii=False,
                indent=2,
            )
        with open(self.katilimcilar_dosya, "w", encoding="utf-8") as f:
            json.dump(
                [k.to_dict() for k in self._katilimcilar.values()],
                f,
                ensure_ascii=False,
                indent=2,
            )
        with open(self.biletler_dosya, "w", encoding="utf-8") as f:
            json.dump(
                [b.to_dict() for b in self._biletler.values()],
                f,
                ensure_ascii=False,
                indent=2,
            )

    # ---------------- ETKINLIK CRUD ----------------

    def etkinlik_ekle(self, ad: str, tarih: datetime, kapasite: int) -> Etkinlik:
        """Yeni etkinlik oluşturup sisteme ekler."""
        if tarih < datetime.now():
            raise ValueError("Geçmiş tarihli etkinlik oluşturulamaz.")

        etkinlik = Etkinlik(
            etkinlik_id=self._sonraki_etkinlik_id,
            ad=ad,
            tarih=tarih,
            kapasite=kapasite,
        )
        self._etkinlikler[etkinlik.etkinlik_id] = etkinlik
        self._sonraki_etkinlik_id += 1
        self.kaydet()
        return etkinlik

    def etkinlik_guncelle(
        self, etkinlik_id: int, ad: str, tarih: datetime, kapasite: int
    ) -> Etkinlik:
        """Mevcut etkinliği günceller."""
        etkinlik = self._etkinlikler.get(etkinlik_id)
        if not etkinlik:
            raise ValueError(f"Etkinlik bulunamadı (ID: {etkinlik_id}).")

        simdi = datetime.now()
        # Etkinlik geçmişteyse tarih kilitli (sadece ad/kapasite düzenlenebilir)
        if etkinlik.tarih < simdi and tarih != etkinlik.tarih:
            raise ValueError(
                "Geçmişte gerçekleşen bir etkinliğin tarihi değiştirilemez."
            )
        # Etkinlik gelecekteyse, yeni tarih de geçmiş olamaz
        if etkinlik.tarih >= simdi and tarih < simdi:
            raise ValueError("Etkinlik tarihi geçmişe alınamaz.")

        if kapasite < etkinlik.katilimci_sayisi():
            raise ValueError(
                f"Yeni kapasite mevcut katılımcı sayısından küçük olamaz "
                f"(Mevcut: {etkinlik.katilimci_sayisi()})."
            )

        etkinlik.ad = ad.strip()
        etkinlik.tarih = tarih
        etkinlik.kapasite = kapasite
        self.kaydet()
        return etkinlik

    def etkinlik_sil(self, etkinlik_id: int) -> bool:
        """Etkinliği ve ilgili biletleri siler."""
        if etkinlik_id not in self._etkinlikler:
            return False

        # Etkinliğe ait biletleri sil
        silinecek_biletler = [
            b.bilet_id for b in self._biletler.values() if b.etkinlik_id == etkinlik_id
        ]
        for bid in silinecek_biletler:
            del self._biletler[bid]

        del self._etkinlikler[etkinlik_id]
        self.kaydet()
        return True

    def etkinlik_getir(self, etkinlik_id: int) -> Optional[Etkinlik]:
        return self._etkinlikler.get(etkinlik_id)

    def tum_etkinlikler(self) -> List[Etkinlik]:
        return sorted(self._etkinlikler.values(), key=lambda e: e.tarih)

    # ---------------- KATILIMCI CRUD ----------------

    def katilimci_ekle(self, ad: str, email: str) -> Katilimci:
        """Yeni katılımcı oluşturur. E-posta benzersiz olmalı."""
        email_lower = email.strip().lower()
        for k in self._katilimcilar.values():
            if k.email == email_lower:
                raise ValueError(f"Bu e-posta zaten kayıtlı: {email_lower}")

        katilimci = Katilimci(
            katilimci_id=self._sonraki_katilimci_id,
            ad=ad,
            email=email,
        )
        self._katilimcilar[katilimci.katilimci_id] = katilimci
        self._sonraki_katilimci_id += 1
        self.kaydet()
        return katilimci

    def katilimci_guncelle(
        self, katilimci_id: int, ad: str, email: str
    ) -> Katilimci:
        katilimci = self._katilimcilar.get(katilimci_id)
        if not katilimci:
            raise ValueError(f"Katılımcı bulunamadı (ID: {katilimci_id}).")

        email_lower = email.strip().lower()
        for k in self._katilimcilar.values():
            if k.katilimci_id != katilimci_id and k.email == email_lower:
                raise ValueError(f"Bu e-posta başka bir katılımcıya ait: {email_lower}")

        if not Katilimci._email_gecerli_mi(email):
            raise ValueError(f"Geçersiz e-posta formatı: {email}")

        katilimci.ad = ad.strip()
        katilimci.email = email_lower
        self.kaydet()
        return katilimci

    def katilimci_sil(self, katilimci_id: int) -> bool:
        """Katılımcıyı, biletlerini ve etkinlik kayıtlarını siler."""
        if katilimci_id not in self._katilimcilar:
            return False

        # Katılımcının biletlerini sil
        silinecek_biletler = [
            b.bilet_id
            for b in self._biletler.values()
            if b.katilimci_id == katilimci_id
        ]
        for bid in silinecek_biletler:
            del self._biletler[bid]

        # Etkinliklerden çıkar
        for etkinlik in self._etkinlikler.values():
            etkinlik.katilimci_cikar(katilimci_id)

        del self._katilimcilar[katilimci_id]
        self.kaydet()
        return True

    def katilimci_getir(self, katilimci_id: int) -> Optional[Katilimci]:
        return self._katilimcilar.get(katilimci_id)

    def tum_katilimcilar(self) -> List[Katilimci]:
        return sorted(self._katilimcilar.values(), key=lambda k: k.ad.lower())

    # ---------------- BILET / KAYIT ----------------

    def bilet_olustur(self, etkinlik_id: int, katilimci_id: int) -> Bilet:
        """
        Bir katılımcıyı etkinliğe kaydeder ve bilet oluşturur.
        Etkinlik.katilimci_ekle() ve Bilet.bilet_olustur() metodlarını
        koordine eder.
        """
        etkinlik = self._etkinlikler.get(etkinlik_id)
        if not etkinlik:
            raise ValueError(f"Etkinlik bulunamadı (ID: {etkinlik_id}).")

        katilimci = self._katilimcilar.get(katilimci_id)
        if not katilimci:
            raise ValueError(f"Katılımcı bulunamadı (ID: {katilimci_id}).")

        # Etkinliğe katılımcı ekle (kapasite ve duplikasyon kontrolü burada)
        etkinlik.katilimci_ekle(katilimci_id)

        # Factory metodu ile bilet üret
        bilet = Bilet.bilet_olustur(
            bilet_id=self._sonraki_bilet_id,
            etkinlik_id=etkinlik_id,
            katilimci_id=katilimci_id,
        )
        self._biletler[bilet.bilet_id] = bilet
        self._sonraki_bilet_id += 1
        self.kaydet()
        return bilet

    def bilet_iptal(self, bilet_id: int) -> bool:
        """Bileti iptal eder ve katılımcıyı etkinlikten çıkarır."""
        bilet = self._biletler.get(bilet_id)
        if not bilet:
            return False

        etkinlik = self._etkinlikler.get(bilet.etkinlik_id)
        if etkinlik:
            etkinlik.katilimci_cikar(bilet.katilimci_id)

        del self._biletler[bilet_id]
        self.kaydet()
        return True

    def bilet_getir(self, bilet_id: int) -> Optional[Bilet]:
        return self._biletler.get(bilet_id)

    def tum_biletler(self) -> List[Bilet]:
        return sorted(
            self._biletler.values(), key=lambda b: b.olusturma_tarihi, reverse=True
        )

    def etkinlik_biletleri(self, etkinlik_id: int) -> List[Bilet]:
        return [b for b in self._biletler.values() if b.etkinlik_id == etkinlik_id]

    # ---------------- RAPORLAR ----------------

    def katilim_raporu(self) -> List[dict]:
        """
        Her etkinlik için katılım raporu üretir.
        Returns: [{"etkinlik": Etkinlik, "katilim": int, "kapasite": int, "doluluk_yuzde": float, "katilimcilar": [Katilimci]}]
        """
        rapor = []
        for etkinlik in self.tum_etkinlikler():
            katilimcilar = [
                self._katilimcilar[kid]
                for kid in etkinlik.katilimcilar
                if kid in self._katilimcilar
            ]
            doluluk = (
                (etkinlik.katilimci_sayisi() / etkinlik.kapasite) * 100
                if etkinlik.kapasite
                else 0
            )
            rapor.append(
                {
                    "etkinlik": etkinlik,
                    "katilim": etkinlik.katilimci_sayisi(),
                    "kapasite": etkinlik.kapasite,
                    "doluluk_yuzde": round(doluluk, 1),
                    "katilimcilar": katilimcilar,
                }
            )
        return rapor

    def genel_istatistikler(self) -> dict:
        """Genel sistem istatistiklerini döner."""
        toplam_kapasite = sum(e.kapasite for e in self._etkinlikler.values())
        toplam_katilim = sum(
            e.katilimci_sayisi() for e in self._etkinlikler.values()
        )
        return {
            "toplam_etkinlik": len(self._etkinlikler),
            "toplam_katilimci": len(self._katilimcilar),
            "toplam_bilet": len(self._biletler),
            "toplam_kapasite": toplam_kapasite,
            "toplam_katilim": toplam_katilim,
            "genel_doluluk": (
                round((toplam_katilim / toplam_kapasite) * 100, 1)
                if toplam_kapasite
                else 0
            ),
        }
