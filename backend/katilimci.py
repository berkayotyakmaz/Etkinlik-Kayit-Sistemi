"""
Katılımcı sınıfı - Etkinliklere kayıt olan kişileri temsil eder.
"""
import re


class Katilimci:
    """
    Bir katılımcıyı temsil eden sınıf.

    Attributes:
        katilimci_id (int): Katılımcının benzersiz kimliği
        ad (str): Katılımcının adı soyadı
        email (str): Katılımcının e-posta adresi
    """

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def __init__(self, katilimci_id: int, ad: str, email: str):
        if not ad or not ad.strip():
            raise ValueError("Katılımcı adı boş olamaz.")
        if not self._email_gecerli_mi(email):
            raise ValueError(f"Geçersiz e-posta formatı: {email}")

        self.katilimci_id = katilimci_id
        self.ad = ad.strip()
        self.email = email.strip().lower()

    @staticmethod
    def _email_gecerli_mi(email: str) -> bool:
        """E-posta adresinin formatını doğrular."""
        if not email or not isinstance(email, str):
            return False
        return bool(Katilimci.EMAIL_REGEX.match(email.strip()))

    def to_dict(self) -> dict:
        """Katılımcıyı dict formatına dönüştürür."""
        return {
            "katilimci_id": self.katilimci_id,
            "ad": self.ad,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Katilimci":
        """Dict'ten Katılımcı nesnesi oluşturur."""
        return cls(
            katilimci_id=data["katilimci_id"],
            ad=data["ad"],
            email=data["email"],
        )

    def __repr__(self) -> str:
        return f"Katilimci(id={self.katilimci_id}, ad='{self.ad}', email='{self.email}')"
