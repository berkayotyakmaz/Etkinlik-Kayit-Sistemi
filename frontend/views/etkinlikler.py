"""
Etkinlikler Sayfası.
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
from PyQt5.QtGui import QFont

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    DolulukGosterge,
    Rozet,
    HucreSarmalayici,
    ButonGrubu,
)
from frontend.widgets.diyaloglar import EtkinlikDiyalog


class EtkinliklerSayfasi(QWidget):
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

        # Üst bar
        ust = QHBoxLayout()

        baslik_l = QVBoxLayout()
        baslik_l.setSpacing(4)
        baslik = QLabel("Etkinlikler")
        baslik.setObjectName("SayfaBaslik")
        alt = QLabel("Tüm etkinlikleri yönetin, kapasite ve katılım takibi yapın.")
        alt.setObjectName("SayfaAltBaslik")
        baslik_l.addWidget(baslik)
        baslik_l.addWidget(alt)

        ust.addLayout(baslik_l)
        ust.addStretch()

        ekle_btn = QPushButton("+   Yeni Etkinlik")
        ekle_btn.setObjectName("PrimaryButon")
        ekle_btn.setStyleSheet(
            "QPushButton { background-color: #a855f7; color: white; "
            "border: none; border-radius: 8px; "
            "padding-left: 18px; padding-right: 18px; "
            "font-size: 13px; font-weight: 600; } "
            "QPushButton:hover { background-color: #9333ea; }"
        )
        ekle_btn.setFixedHeight(42)
        ekle_btn.setMinimumWidth(160)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._etkinlik_ekle)
        ust.addWidget(ekle_btn)

        ana.addLayout(ust)

        # Arama
        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("🔍   Etkinlik ara...")
        self.arama.setFixedHeight(42)
        self.arama.textChanged.connect(self.yenile)
        ana.addWidget(self.arama)

        # Tablo
        self.tablo = QTableWidget(0, 6)
        self.tablo.setHorizontalHeaderLabels(
            ["ID", "Etkinlik", "Tarih", "Doluluk", "Durum", "İşlemler"]
        )
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Fixed)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        h.setSectionResizeMode(4, QHeaderView.Fixed)
        h.setSectionResizeMode(5, QHeaderView.Fixed)
        self.tablo.setColumnWidth(0, 70)
        self.tablo.setColumnWidth(3, 220)
        self.tablo.setColumnWidth(4, 120)
        self.tablo.setColumnWidth(5, 200)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        etkinlikler = [
            e for e in self.vy.tum_etkinlikler() if filtre in e.ad.lower()
        ]

        self.tablo.setRowCount(len(etkinlikler))

        for satir, e in enumerate(etkinlikler):
            id_item = QTableWidgetItem(f"  #{e.etkinlik_id}")
            id_item.setForeground(Qt.gray)
            self.tablo.setItem(satir, 0, id_item)

            ad_item = QTableWidgetItem(e.ad)
            f = QFont()
            f.setWeight(QFont.DemiBold)
            ad_item.setFont(f)
            self.tablo.setItem(satir, 1, ad_item)

            tarih_item = QTableWidgetItem(
                e.tarih.strftime("%d.%m.%Y  ·  %H:%M")
            )
            tarih_item.setForeground(Qt.gray)
            self.tablo.setItem(satir, 2, tarih_item)

            self.tablo.setCellWidget(
                satir,
                3,
                HucreSarmalayici(
                    DolulukGosterge(e.katilimci_sayisi(), e.kapasite)
                ),
            )

            if e.dolu_mu():
                rozet = Rozet("DOLU", "tehlike")
            elif e.kalan_kontenjan() <= max(1, e.kapasite * 0.2):
                rozet = Rozet("AZ KALDI", "uyari")
            else:
                rozet = Rozet("AÇIK", "basari")
            self.tablo.setCellWidget(satir, 4, HucreSarmalayici(rozet))

            duzen_btn = QPushButton("Düzenle")
            duzen_btn.setObjectName("KucukIkincilButon")
            duzen_btn.setFixedHeight(32)
            duzen_btn.setFixedWidth(86)
            duzen_btn.setCursor(Qt.PointingHandCursor)
            duzen_btn.clicked.connect(
                lambda _, eid=e.etkinlik_id: self._duzenle(eid)
            )

            sil_btn = QPushButton("Sil")
            sil_btn.setObjectName("KucukTehlikeButon")
            sil_btn.setFixedHeight(32)
            sil_btn.setFixedWidth(58)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.clicked.connect(lambda _, eid=e.etkinlik_id: self._sil(eid))

            self.tablo.setCellWidget(satir, 5, ButonGrubu([duzen_btn, sil_btn]))

            self.tablo.setRowHeight(satir, 64)

    def _etkinlik_ekle(self):
        d = EtkinlikDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _duzenle(self, etkinlik_id: int):
        e = self.vy.etkinlik_getir(etkinlik_id)
        if not e:
            return
        d = EtkinlikDiyalog(self.vy, etkinlik=e, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _sil(self, etkinlik_id: int):
        e = self.vy.etkinlik_getir(etkinlik_id)
        if not e:
            return

        cevap = QMessageBox.question(
            self,
            "Etkinliği Sil",
            f"'{e.ad}' etkinliğini silmek istediğinizden emin misiniz?\n\n"
            f"Bu etkinliğe ait {len(e.katilimcilar)} bilet de silinecektir.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            self.vy.etkinlik_sil(etkinlik_id)
            self.yenile()
            self.veri_degisti.emit()
