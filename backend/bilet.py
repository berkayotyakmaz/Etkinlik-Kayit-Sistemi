"""
Bilet sınıfı - Bir katılımcının bir etkinliğe kaydını temsil eder.
"""
from datetime import datetime
import uuid


class Bilet:
    """
    Bir bileti temsil eden sınıf. Etkinlik ile katılımcıyı birleştirir.

    Attributes:
        bilet_id (int): Biletin benzersiz kimliği
        etkinlik_id (int): Bağlı olduğu etkinliğin kimliği
        katilimci_id (int): Bilet sahibi katılımcının kimliği
        kod (str): Bilet üzerindeki benzersiz kod (BLT-XXXXXXXX)
        olusturma_tarihi (datetime): Biletin oluşturulduğu tarih
    """

    def __init__(
        self,
        bilet_id: int,
        etkinlik_id: int,
        katilimci_id: int,
        kod: str = None,
        olusturma_tarihi: datetime = None,
    ):
        self.bilet_id = bilet_id
        self.etkinlik_id = etkinlik_id
        self.katilimci_id = katilimci_id
        self.kod = kod if kod else self._kod_uret()
        self.olusturma_tarihi = olusturma_tarihi if olusturma_tarihi else datetime.now()

    @staticmethod
    def _kod_uret() -> str:
        """Benzersiz bilet kodu üretir."""
        return f"BLT-{uuid.uuid4().hex[:8].upper()}"

    @classmethod
    def bilet_olustur(
        cls, bilet_id: int, etkinlik_id: int, katilimci_id: int
    ) -> "Bilet":
        """
        Yeni bir bilet oluşturur (factory metodu).

        Args:
            bilet_id: Yeni biletin kimliği
            etkinlik_id: Etkinlik kimliği
            katilimci_id: Katılımcı kimliği

        Returns:
            Bilet: Oluşturulan bilet nesnesi
        """
        return cls(
            bilet_id=bilet_id,
            etkinlik_id=etkinlik_id,
            katilimci_id=katilimci_id,
        )

    def to_dict(self) -> dict:
        return {
            "bilet_id": self.bilet_id,
            "etkinlik_id": self.etkinlik_id,
            "katilimci_id": self.katilimci_id,
            "kod": self.kod,
            "olusturma_tarihi": self.olusturma_tarihi.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Bilet":
        return cls(
            bilet_id=data["bilet_id"],
            etkinlik_id=data["etkinlik_id"],
            katilimci_id=data["katilimci_id"],
            kod=data["kod"],
            olusturma_tarihi=datetime.fromisoformat(data["olusturma_tarihi"]),
        )

    def __repr__(self) -> str:
        return f"Bilet(id={self.bilet_id}, kod={self.kod}, etkinlik={self.etkinlik_id}, katilimci={self.katilimci_id})"
