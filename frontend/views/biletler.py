"""
Biletler Sayfası.
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
from frontend.widgets.bilesenler import HucreSarmalayici, ButonGrubu, BiletKodRozet
from frontend.widgets.diyaloglar import BiletOlusturDiyalog


class _BiletKodHucresi(QWidget):
    """Bilet kodu hücre sarmalayıcı."""

    def __init__(self, kod: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(0)
        layout.addWidget(BiletKodRozet(kod), 0, Qt.AlignVCenter)
        layout.addStretch()


class BiletlerSayfasi(QWidget):
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
        baslik = QLabel("Biletler")
        baslik.setObjectName("SayfaBaslik")
        alt = QLabel("Etkinliklere kayıtlı tüm biletler ve detayları.")
        alt.setObjectName("SayfaAltBaslik")
        baslik_l.addWidget(baslik)
        baslik_l.addWidget(alt)
        ust.addLayout(baslik_l)
        ust.addStretch()

        olustur_btn = QPushButton("✦   Bilet Oluştur")
        olustur_btn.setObjectName("BasariButon")
        olustur_btn.setStyleSheet(
            "QPushButton { background-color: #10d9a0; color: #032e22; "
            "border: none; border-radius: 8px; "
            "padding-left: 18px; padding-right: 18px; "
            "font-size: 13px; font-weight: 700; } "
            "QPushButton:hover { background-color: #06d6a0; }"
        )
        olustur_btn.setFixedHeight(42)
        olustur_btn.setMinimumWidth(170)
        olustur_btn.setCursor(Qt.PointingHandCursor)
        olustur_btn.clicked.connect(self._bilet_olustur)
        ust.addWidget(olustur_btn)

        ana.addLayout(ust)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("🔍   Bilet kodu, etkinlik veya katılımcı ara...")
        self.arama.setFixedHeight(42)
        self.arama.textChanged.connect(self.yenile)
        ana.addWidget(self.arama)

        self.tablo = QTableWidget(0, 5)
        self.tablo.setHorizontalHeaderLabels(
            ["Bilet Kodu", "Etkinlik", "Katılımcı", "Oluşturulma", "İşlem"]
        )
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Fixed)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.Fixed)
        self.tablo.setColumnWidth(0, 170)
        self.tablo.setColumnWidth(4, 130)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        biletler = self.vy.tum_biletler()

        satirlar = []
        for b in biletler:
            e = self.vy.etkinlik_getir(b.etkinlik_id)
            k = self.vy.katilimci_getir(b.katilimci_id)
            if not e or not k:
                continue
            metin = f"{b.kod} {e.ad} {k.ad} {k.email}".lower()
            if filtre and filtre not in metin:
                continue
            satirlar.append((b, e, k))

        self.tablo.setRowCount(len(satirlar))

        for satir, (b, e, k) in enumerate(satirlar):
            self.tablo.setCellWidget(satir, 0, _BiletKodHucresi(b.kod))

            etkinlik_item = QTableWidgetItem(e.ad)
            f = QFont()
            f.setWeight(QFont.DemiBold)
            etkinlik_item.setFont(f)
            self.tablo.setItem(satir, 1, etkinlik_item)

            kat_item = QTableWidgetItem(f"{k.ad}  ·  {k.email}")
            kat_item.setForeground(QColor("#8b8b9e"))
            self.tablo.setItem(satir, 2, kat_item)

            tarih_item = QTableWidgetItem(b.olusturma_tarihi.strftime("%d.%m.%Y %H:%M"))
            tarih_item.setForeground(QColor("#8b8b9e"))
            self.tablo.setItem(satir, 3, tarih_item)

            iptal_btn = QPushButton("İptal Et")
            iptal_btn.setObjectName("KucukTehlikeButon")
            iptal_btn.setFixedHeight(32)
            iptal_btn.setFixedWidth(86)
            iptal_btn.setCursor(Qt.PointingHandCursor)
            iptal_btn.clicked.connect(lambda _, bid=b.bilet_id: self._iptal(bid))

            self.tablo.setCellWidget(satir, 4, ButonGrubu([iptal_btn]))

            self.tablo.setRowHeight(satir, 56)

    def _bilet_olustur(self):
        if not self.vy.tum_etkinlikler():
            QMessageBox.warning(
                self, "Etkinlik Yok",
                "Önce en az bir etkinlik oluşturmanız gerekiyor.",
            )
            return
        if not self.vy.tum_katilimcilar():
            QMessageBox.warning(
                self, "Katılımcı Yok",
                "Önce en az bir katılımcı eklemeniz gerekiyor.",
            )
            return

        d = BiletOlusturDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _iptal(self, bilet_id: int):
        b = self.vy.bilet_getir(bilet_id)
        if not b:
            return

        cevap = QMessageBox.question(
            self,
            "Bileti İptal Et",
            f"'{b.kod}' kodlu bileti iptal etmek istediğinizden emin misiniz?\n\n"
            f"Katılımcı, etkinliğin kayıt listesinden çıkarılacaktır.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            self.vy.bilet_iptal(bilet_id)
            self.yenile()
            self.veri_degisti.emit()
