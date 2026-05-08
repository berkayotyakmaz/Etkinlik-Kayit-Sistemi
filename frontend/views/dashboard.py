"""
Dashboard / Kontrol Paneli - Premium tasarım.
"""
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    HeroPanel,
    MetricKarti,
    DairesselGauge,
    Kart,
    DolulukGosterge,
    Rozet,
    HucreSarmalayici,
)


class DashboardSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(20)

        # ─── HERO PANEL ────────────────────────────────────────────
        self.hero = HeroPanel(
            "Kontrol Paneli",
            "Etkinliklerini, katılımcılarını ve biletlerini tek bakışta yönet.",
        )
        ana.addWidget(self.hero)

        # ─── METRIC GRID ───────────────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(16)

        self.kart_etkinlik = MetricKarti(
            "Etkinlik", "0", ikon="◈", renk="mor", trend="aktif sistem"
        )
        self.kart_katilimci = MetricKarti(
            "Katılımcı", "0", ikon="◉", renk="mint", trend="kayıtlı"
        )
        self.kart_bilet = MetricKarti(
            "Bilet", "0", ikon="✦", renk="amber", trend="oluşturulan"
        )
        self.kart_doluluk = MetricKarti(
            "Doluluk", "%0", ikon="◊", renk="pembe", trend="genel oran"
        )

        grid.addWidget(self.kart_etkinlik, 0, 0)
        grid.addWidget(self.kart_katilimci, 0, 1)
        grid.addWidget(self.kart_bilet, 0, 2)
        grid.addWidget(self.kart_doluluk, 0, 3)

        ana.addLayout(grid)

        # ─── ALT BÖLÜM: gauge + tablo ─────────────────────────────
        alt = QHBoxLayout()
        alt.setSpacing(16)

        # Sol: gauge kartı
        self.gauge_kart = self._gauge_karti_olustur()
        alt.addWidget(self.gauge_kart, 0)

        # Sağ: tablo
        tablo_kart = Kart(
            "Yaklaşan Etkinlikler",
            "Bugünden sonra düzenlenecek ilk etkinlikler.",
        )

        self.tablo = QTableWidget(0, 4)
        self.tablo.setHorizontalHeaderLabels(["Etkinlik", "Tarih", "Doluluk", "Durum"])
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        self.tablo.setColumnWidth(2, 220)
        self.tablo.setColumnWidth(3, 110)

        self.tablo.setMinimumHeight(330)
        tablo_kart.layout.addWidget(self.tablo)

        alt.addWidget(tablo_kart, 1)

        ana.addLayout(alt, 1)

    def _gauge_karti_olustur(self) -> QFrame:
        kart = QFrame()
        kart.setObjectName("Kart")
        kart.setFixedWidth(280)

        layout = QVBoxLayout(kart)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        baslik = QLabel("Sistem Durumu")
        baslik.setObjectName("KartBaslik")
        alt_baslik = QLabel("Genel kapasite kullanımı")
        alt_baslik.setObjectName("KartAltBaslik")
        layout.addWidget(baslik)
        layout.addWidget(alt_baslik)

        layout.addStretch()

        # Gauge ortalanmış
        gauge_sarici = QHBoxLayout()
        self.gauge = DairesselGauge(0, "GENEL DOLULUK", 160)
        gauge_sarici.addStretch()
        gauge_sarici.addWidget(self.gauge)
        gauge_sarici.addStretch()
        layout.addLayout(gauge_sarici)

        layout.addStretch()

        # Alt mini istatistikler
        self.alt_kapasite = QLabel("Toplam Kapasite: 0")
        self.alt_kapasite.setStyleSheet(
            "color: #8d8da3; font-size: 11px; background: transparent; border: none;"
        )
        self.alt_katilim = QLabel("Aktif Katılım: 0")
        self.alt_katilim.setStyleSheet(
            "color: #b265ff; font-size: 11px; font-weight: 600; background: transparent; border: none;"
        )
        layout.addWidget(self.alt_kapasite)
        layout.addWidget(self.alt_katilim)

        return kart

    def _sahte_spark(self, deger: int, n: int = 12) -> list:
        """Veri yokken estetik için rastgele sparkline."""
        random.seed(deger * 17 + n)
        if deger == 0:
            return [0] * n
        veri = []
        son = max(1, deger // 2)
        for _ in range(n):
            son += random.randint(-2, 3)
            son = max(0, son)
            veri.append(son)
        veri.append(deger)
        return veri

    def yenile(self):
        stats = self.vy.genel_istatistikler()

        # Hero
        self.hero.degerleri_ayarla(stats["toplam_etkinlik"], stats["toplam_katilim"])

        # Metric kartlar
        self.kart_etkinlik.deger_ayarla(stats["toplam_etkinlik"])
        self.kart_etkinlik.spark_ayarla(self._sahte_spark(stats["toplam_etkinlik"]))

        self.kart_katilimci.deger_ayarla(stats["toplam_katilimci"])
        self.kart_katilimci.spark_ayarla(self._sahte_spark(stats["toplam_katilimci"], 10))

        self.kart_bilet.deger_ayarla(stats["toplam_bilet"])
        self.kart_bilet.spark_ayarla(self._sahte_spark(stats["toplam_bilet"], 14))

        self.kart_doluluk.deger_ayarla(f"%{stats['genel_doluluk']}")
        self.kart_doluluk.spark_ayarla(self._sahte_spark(int(stats["genel_doluluk"]), 12))

        # Gauge
        self.gauge.deger_ayarla(int(stats["genel_doluluk"]))
        self.alt_kapasite.setText(f"Toplam Kapasite: {stats['toplam_kapasite']}")
        self.alt_katilim.setText(f"Aktif Katılım: {stats['toplam_katilim']}")

        # Tablo
        etkinlikler = [
            e for e in self.vy.tum_etkinlikler() if e.tarih >= datetime.now()
        ][:6]

        self.tablo.setRowCount(len(etkinlikler) if etkinlikler else 1)

        if not etkinlikler:
            bos = QTableWidgetItem("  Yaklaşan etkinlik bulunmuyor.")
            bos.setForeground(QColor("#5a5a72"))
            self.tablo.setSpan(0, 0, 1, 4)
            self.tablo.setItem(0, 0, bos)
            self.tablo.setRowHeight(0, 80)
            return

        for satir, e in enumerate(etkinlikler):
            ad_item = QTableWidgetItem("  " + e.ad)
            f = QFont("Inter")
            f.setBold(True)
            ad_item.setFont(f)
            self.tablo.setItem(satir, 0, ad_item)

            tarih_item = QTableWidgetItem(e.tarih.strftime("%d.%m.%Y  ·  %H:%M"))
            tarih_item.setForeground(QColor("#8d8da3"))
            self.tablo.setItem(satir, 1, tarih_item)

            self.tablo.setCellWidget(
                satir, 2, HucreSarmalayici(DolulukGosterge(e.katilimci_sayisi(), e.kapasite))
            )

            if e.dolu_mu():
                rozet = Rozet("DOLU", "tehlike")
            elif e.kalan_kontenjan() <= max(1, e.kapasite * 0.2):
                rozet = Rozet("AZ KALDI", "uyari")
            else:
                rozet = Rozet("AÇIK", "basari")
            self.tablo.setCellWidget(satir, 3, HucreSarmalayici(rozet))

            self.tablo.setRowHeight(satir, 60)
