"""
Etkinlik sınıfı - Bir etkinliğin temel bilgilerini ve katılımcı yönetimini tutar.
"""
from datetime import datetime
from typing import List, Optional


class Etkinlik:
    """
    Bir etkinliği temsil eden sınıf.

    Attributes:
        etkinlik_id (int): Etkinliğin benzersiz kimliği
        ad (str): Etkinlik adı
        tarih (datetime): Etkinlik tarihi ve saati
        kapasite (int): Maksimum katılımcı sayısı
        katilimcilar (list): Etkinliğe kayıtlı katılımcı id listesi
    """

    def __init__(self, etkinlik_id: int, ad: str, tarih: datetime, kapasite: int):
        if not ad or not ad.strip():
            raise ValueError("Etkinlik adı boş olamaz.")
        if kapasite <= 0:
            raise ValueError("Kapasite pozitif bir sayı olmalıdır.")
        if not isinstance(tarih, datetime):
            raise TypeError("Tarih datetime tipinde olmalıdır.")

        self.etkinlik_id = etkinlik_id
        self.ad = ad.strip()
        self.tarih = tarih
        self.kapasite = kapasite
        self.katilimcilar: List[int] = []  # katilimci_id listesi

    def katilimci_ekle(self, katilimci_id: int) -> bool:
        """
        Etkinliğe yeni bir katılımcı ekler.

        Args:
            katilimci_id: Eklenecek katılımcının kimliği

        Returns:
            bool: Ekleme başarılı ise True

        Raises:
            ValueError: Kapasite dolmuşsa veya katılımcı zaten kayıtlıysa
        """
        if self.dolu_mu():
            raise ValueError(
                f"'{self.ad}' etkinliğinin kapasitesi dolmuştur ({self.kapasite}/{self.kapasite})."
            )
        if katilimci_id in self.katilimcilar:
            raise ValueError("Bu katılımcı etkinliğe zaten kayıtlı.")

        self.katilimcilar.append(katilimci_id)
        return True

    def katilimci_cikar(self, katilimci_id: int) -> bool:
        """Katılımcıyı etkinlikten çıkarır."""
        if katilimci_id in self.katilimcilar:
            self.katilimcilar.remove(katilimci_id)
            return True
        return False

    def dolu_mu(self) -> bool:
        """Etkinlik kapasitesinin dolup dolmadığını kontrol eder."""
        return len(self.katilimcilar) >= self.kapasite

    def kalan_kontenjan(self) -> int:
        """Kalan kontenjan sayısını döndürür."""
        return self.kapasite - len(self.katilimcilar)

    def katilimci_sayisi(self) -> int:
        """Mevcut katılımcı sayısını döndürür."""
        return len(self.katilimcilar)

    def to_dict(self) -> dict:
        """Etkinliği dict formatına dönüştürür (JSON serialization için)."""
        return {
            "etkinlik_id": self.etkinlik_id,
            "ad": self.ad,
            "tarih": self.tarih.isoformat(),
            "kapasite": self.kapasite,
            "katilimcilar": self.katilimcilar,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Etkinlik":
        """Dict'ten Etkinlik nesnesi oluşturur."""
        etkinlik = cls(
            etkinlik_id=data["etkinlik_id"],
            ad=data["ad"],
            tarih=datetime.fromisoformat(data["tarih"]),
            kapasite=data["kapasite"],
        )
        etkinlik.katilimcilar = data.get("katilimcilar", [])
        return etkinlik

    def __repr__(self) -> str:
        return f"Etkinlik(id={self.etkinlik_id}, ad='{self.ad}', {self.katilimci_sayisi()}/{self.kapasite})"
