"""
Katılımcılar Sayfası.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import HucreSarmalayici, ButonGrubu, Rozet, Avatar
from frontend.widgets.diyaloglar import KatilimciDiyalog


class _AvatarHucresi(QWidget):
    """Avatar + ad/email birleşik hücre."""

    def __init__(self, ad: str, email: str, kid: int, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(14)

        layout.addWidget(Avatar(ad, boyut=38))

        bilgi = QVBoxLayout()
        bilgi.setSpacing(2)
        bilgi.setContentsMargins(0, 0, 0, 0)

        ad_lbl = QLabel(ad)
        ad_lbl.setStyleSheet(
            "color: #f4f4f8; font-weight: 600; font-size: 13px; "
            "background: transparent; border: none;"
        )

        meta_lbl = QLabel(f"#{kid}  ·  {email}")
        meta_lbl.setStyleSheet(
            "color: #8b8b9e; font-size: 11px; "
            "background: transparent; border: none;"
        )

        bilgi.addWidget(ad_lbl)
        bilgi.addWidget(meta_lbl)

        layout.addLayout(bilgi)
        layout.addStretch()


class KatilimcilarSayfasi(QWidget):
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(20)

        ust = QHBoxLayout()
        baslik_l = QVBoxLayout()
        baslik_l.setSpacing(4)
        baslik = QLabel("Katılımcılar")
        baslik.setObjectName("SayfaBaslik")
        alt = QLabel("Sisteme kayıtlı tüm katılımcılar.")
        alt.setObjectName("SayfaAltBaslik")
        baslik_l.addWidget(baslik)
        baslik_l.addWidget(alt)
        ust.addLayout(baslik_l)
        ust.addStretch()

        ekle_btn = QPushButton("+   Yeni Katılımcı")
        ekle_btn.setObjectName("PrimaryButon")
        ekle_btn.setStyleSheet(
            "QPushButton { background-color: #a855f7; color: white; "
            "border: none; border-radius: 8px; "
            "padding-left: 18px; padding-right: 18px; "
            "font-size: 13px; font-weight: 600; } "
            "QPushButton:hover { background-color: #9333ea; }"
        )
        ekle_btn.setFixedHeight(42)
        ekle_btn.setMinimumWidth(170)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._ekle)
        ust.addWidget(ekle_btn)

        ana.addLayout(ust)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("🔍   İsim veya e-posta ara...")
        self.arama.setFixedHeight(42)
        self.arama.textChanged.connect(self.yenile)
        ana.addWidget(self.arama)

        self.tablo = QTableWidget(0, 3)
        self.tablo.setHorizontalHeaderLabels(["Katılımcı", "Bilet Sayısı", "İşlemler"])
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.Fixed)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        self.tablo.setColumnWidth(1, 140)
        self.tablo.setColumnWidth(2, 200)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        katilimcilar = [
            k
            for k in self.vy.tum_katilimcilar()
            if filtre in k.ad.lower() or filtre in k.email.lower()
        ]

        bilet_sayilari = {}
        for b in self.vy.tum_biletler():
            bilet_sayilari[b.katilimci_id] = bilet_sayilari.get(b.katilimci_id, 0) + 1

        self.tablo.setRowCount(len(katilimcilar))

        for satir, k in enumerate(katilimcilar):
            self.tablo.setCellWidget(
                satir, 0, _AvatarHucresi(k.ad, k.email, k.katilimci_id)
            )

            bilet_sayisi = bilet_sayilari.get(k.katilimci_id, 0)
            rozet = Rozet(
                f"{bilet_sayisi} BİLET",
                "basari" if bilet_sayisi > 0 else "notr",
            )
            self.tablo.setCellWidget(satir, 1, HucreSarmalayici(rozet))

            duzen_btn = QPushButton("Düzenle")
            duzen_btn.setObjectName("KucukIkincilButon")
            duzen_btn.setFixedHeight(32)
            duzen_btn.setFixedWidth(86)
            duzen_btn.setCursor(Qt.PointingHandCursor)
            duzen_btn.clicked.connect(
                lambda _, kid=k.katilimci_id: self._duzenle(kid)
            )

            sil_btn = QPushButton("Sil")
            sil_btn.setObjectName("KucukTehlikeButon")
            sil_btn.setFixedHeight(32)
            sil_btn.setFixedWidth(58)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.clicked.connect(lambda _, kid=k.katilimci_id: self._sil(kid))

            self.tablo.setCellWidget(satir, 2, ButonGrubu([duzen_btn, sil_btn]))

            self.tablo.setRowHeight(satir, 56)

    def _ekle(self):
        d = KatilimciDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _duzenle(self, katilimci_id: int):
        k = self.vy.katilimci_getir(katilimci_id)
        if not k:
            return
        d = KatilimciDiyalog(self.vy, katilimci=k, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _sil(self, katilimci_id: int):
        k = self.vy.katilimci_getir(katilimci_id)
        if not k:
            return

        cevap = QMessageBox.question(
            self,
            "Katılımcıyı Sil",
            f"'{k.ad}' kişisini silmek istediğinizden emin misiniz?\n\n"
            f"Bu kişiye ait tüm biletler de silinecektir.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            self.vy.katilimci_sil(katilimci_id)
            self.yenile()
            self.veri_degisti.emit()
