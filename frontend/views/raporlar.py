"""
Raporlar Sayfası - Etkinlik bazlı katılım raporu (ek özellik).
"""
import csv
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    Kart,
    MetricKarti,
    HucreSarmalayici,
)


class RaporlarSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(20)

        baslik_l = QVBoxLayout()
        baslik_l.setSpacing(4)
        baslik = QLabel("Raporlar")
        baslik.setObjectName("SayfaBaslik")
        alt = QLabel("Etkinlik bazlı katılım istatistikleri ve detaylı katılımcı listeleri.")
        alt.setObjectName("SayfaAltBaslik")
        baslik_l.addWidget(baslik)
        baslik_l.addWidget(alt)
        ana.addLayout(baslik_l)

        # Genel özet kartları
        grid = QGridLayout()
        grid.setSpacing(16)

        self.ozet_etkinlik = MetricKarti(
            "Toplam Etkinlik", "0", ikon="◈", renk="mor"
        )
        self.ozet_kapasite = MetricKarti(
            "Toplam Kapasite", "0", ikon="◇", renk="amber"
        )
        self.ozet_katilim = MetricKarti(
            "Toplam Katılım", "0", ikon="◉", renk="mint"
        )
        self.ozet_doluluk = MetricKarti(
            "Genel Doluluk", "%0", ikon="◊", renk="pembe"
        )

        grid.addWidget(self.ozet_etkinlik, 0, 0)
        grid.addWidget(self.ozet_kapasite, 0, 1)
        grid.addWidget(self.ozet_katilim, 0, 2)
        grid.addWidget(self.ozet_doluluk, 0, 3)
        ana.addLayout(grid)

        # Detay raporu
        detay_kart = Kart(
            "Etkinlik Detay Raporu", "Bir etkinlik seçin ve katılımcı listesini görüntüleyin."
        )

        # Seçim satırı
        secim_layout = QHBoxLayout()
        secim_layout.setSpacing(10)

        self.etkinlik_combo = QComboBox()
        self.etkinlik_combo.setFixedHeight(42)
        self.etkinlik_combo.currentIndexChanged.connect(self._detay_yukle)

        self.disa_aktar_btn = QPushButton("⬇   CSV Olarak İndir")
        self.disa_aktar_btn.setObjectName("IkincilButon")
        self.disa_aktar_btn.setFixedHeight(42)
        self.disa_aktar_btn.setMinimumWidth(170)
        self.disa_aktar_btn.setCursor(Qt.PointingHandCursor)
        self.disa_aktar_btn.clicked.connect(self._csv_disa_aktar)

        secim_layout.addWidget(self.etkinlik_combo, 1)
        secim_layout.addWidget(self.disa_aktar_btn)

        detay_kart.layout.addLayout(secim_layout)

        # Etkinlik özet bilgisi
        self.bilgi_kutu = QFrame()
        self.bilgi_kutu.setStyleSheet(
            "background-color: #1f1f2c; "
            "border: 1px solid #252531; "
            "border-radius: 10px;"
        )
        bk_layout = QHBoxLayout(self.bilgi_kutu)
        bk_layout.setContentsMargins(18, 14, 18, 14)
        bk_layout.setSpacing(28)

        self.bilgi_lbl = QLabel("")
        self.bilgi_lbl.setStyleSheet(
            "color: #f4f4f8; font-size: 13px; "
            "background: transparent; border: none;"
        )
        self.bilgi_lbl.setWordWrap(True)
        bk_layout.addWidget(self.bilgi_lbl)

        detay_kart.layout.addWidget(self.bilgi_kutu)

        # Katılımcı tablosu
        self.tablo = QTableWidget(0, 4)
        self.tablo.setHorizontalHeaderLabels(["#", "Ad Soyad", "E-posta", "Bilet Kodu"])
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
        self.tablo.setColumnWidth(0, 60)

        self.tablo.setMinimumHeight(280)
        detay_kart.layout.addWidget(self.tablo)

        ana.addWidget(detay_kart, 1)

    def _sahte_spark(self, deger: int, n: int = 12) -> list:
        import random
        random.seed(deger * 23 + n)
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
        self.ozet_etkinlik.deger_ayarla(stats["toplam_etkinlik"])
        self.ozet_etkinlik.spark_ayarla(self._sahte_spark(stats["toplam_etkinlik"]))

        self.ozet_kapasite.deger_ayarla(stats["toplam_kapasite"])
        self.ozet_kapasite.spark_ayarla(self._sahte_spark(stats["toplam_kapasite"], 14))

        self.ozet_katilim.deger_ayarla(stats["toplam_katilim"])
        self.ozet_katilim.spark_ayarla(self._sahte_spark(stats["toplam_katilim"], 12))

        self.ozet_doluluk.deger_ayarla(f"%{stats['genel_doluluk']}")
        self.ozet_doluluk.spark_ayarla(self._sahte_spark(int(stats["genel_doluluk"]), 12))

        # Combo
        self.etkinlik_combo.blockSignals(True)
        mevcut_id = self.etkinlik_combo.currentData()
        self.etkinlik_combo.clear()

        for e in self.vy.tum_etkinlikler():
            etiket = (
                f"{e.ad}   ·   {e.tarih.strftime('%d.%m.%Y %H:%M')}   "
                f"·   {e.katilimci_sayisi()}/{e.kapasite}"
            )
            self.etkinlik_combo.addItem(etiket, e.etkinlik_id)

        if mevcut_id is not None:
            idx = self.etkinlik_combo.findData(mevcut_id)
            if idx >= 0:
                self.etkinlik_combo.setCurrentIndex(idx)

        self.etkinlik_combo.blockSignals(False)
        self._detay_yukle()

    def _detay_yukle(self):
        eid = self.etkinlik_combo.currentData()
        if eid is None:
            self.bilgi_lbl.setText(
                "<span style='color:#8b8b9e'>Henüz hiç etkinlik bulunmuyor.</span>"
            )
            self.tablo.setRowCount(0)
            self.disa_aktar_btn.setEnabled(False)
            return

        e = self.vy.etkinlik_getir(eid)
        if not e:
            return

        self.disa_aktar_btn.setEnabled(True)

        doluluk = (e.katilimci_sayisi() / e.kapasite * 100) if e.kapasite else 0

        # Renkli özet metni
        self.bilgi_lbl.setText(
            f"<table cellpadding='0' cellspacing='0'><tr>"
            f"<td style='padding-right: 28px;'>"
            f"<span style='color:#8b8b9e; font-size:11px;'>TARİH</span><br>"
            f"<span style='color:#f4f4f8; font-weight:600; font-size:13px;'>"
            f"{e.tarih.strftime('%d.%m.%Y %H:%M')}</span></td>"
            f"<td style='padding-right: 28px;'>"
            f"<span style='color:#8b8b9e; font-size:11px;'>KATILIM</span><br>"
            f"<span style='color:#a855f7; font-weight:700; font-size:13px;'>"
            f"{e.katilimci_sayisi()}</span>"
            f"<span style='color:#8b8b9e;'> / {e.kapasite}</span></td>"
            f"<td style='padding-right: 28px;'>"
            f"<span style='color:#8b8b9e; font-size:11px;'>DOLULUK</span><br>"
            f"<span style='color:#10d9a0; font-weight:700; font-size:13px;'>"
            f"%{doluluk:.1f}</span></td>"
            f"<td>"
            f"<span style='color:#8b8b9e; font-size:11px;'>KALAN</span><br>"
            f"<span style='color:#f4f4f8; font-weight:700; font-size:13px;'>"
            f"{e.kalan_kontenjan()}</span></td>"
            f"</tr></table>"
        )

        biletler = self.vy.etkinlik_biletleri(eid)

        self.tablo.setRowCount(len(biletler))

        for satir, b in enumerate(biletler):
            k = self.vy.katilimci_getir(b.katilimci_id)
            if not k:
                continue

            sira_item = QTableWidgetItem(str(satir + 1))
            sira_item.setForeground(QColor("#8b8b9e"))
            sira_item.setTextAlignment(Qt.AlignCenter)
            self.tablo.setItem(satir, 0, sira_item)

            ad_item = QTableWidgetItem(k.ad)
            f = QFont()
            f.setWeight(QFont.DemiBold)
            ad_item.setFont(f)
            self.tablo.setItem(satir, 1, ad_item)

            email_item = QTableWidgetItem(k.email)
            email_item.setForeground(QColor("#8b8b9e"))
            self.tablo.setItem(satir, 2, email_item)

            kod_lbl = QLabel(b.kod)
            kod_lbl.setStyleSheet(
                "background-color: rgba(168, 85, 247, 0.12); "
                "color: #c4b5fd; "
                "border: 1px solid rgba(168, 85, 247, 0.3); "
                "border-radius: 6px; padding: 4px 10px; "
                "font-family: 'Consolas', monospace; "
                "font-size: 11px; font-weight: 700;"
            )
            kod_lbl.setAlignment(Qt.AlignCenter)
            self.tablo.setCellWidget(satir, 3, HucreSarmalayici(kod_lbl))

            self.tablo.setRowHeight(satir, 48)

    def _csv_disa_aktar(self):
        eid = self.etkinlik_combo.currentData()
        if eid is None:
            return
        e = self.vy.etkinlik_getir(eid)
        if not e:
            return

        guvenli_ad = "".join(
            c if c.isalnum() or c in " -_" else "_" for c in e.ad
        ).strip().replace(" ", "_")
        varsayilan = f"{guvenli_ad}_katilim_raporu.csv"

        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self, "CSV Dosyası Olarak Kaydet", varsayilan, "CSV Dosyaları (*.csv)"
        )
        if not dosya_yolu:
            return

        try:
            with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Etkinlik Adı", e.ad])
                writer.writerow(["Tarih", e.tarih.strftime("%d.%m.%Y %H:%M")])
                writer.writerow(["Kapasite", e.kapasite])
                writer.writerow(["Katılım", e.katilimci_sayisi()])
                writer.writerow([])
                writer.writerow(["#", "Ad Soyad", "E-posta", "Bilet Kodu", "Bilet Tarihi"])
                biletler = self.vy.etkinlik_biletleri(eid)
                for i, b in enumerate(biletler, start=1):
                    k = self.vy.katilimci_getir(b.katilimci_id)
                    if k:
                        writer.writerow([
                            i, k.ad, k.email, b.kod,
                            b.olusturma_tarihi.strftime("%d.%m.%Y %H:%M"),
                        ])

            QMessageBox.information(
                self, "Başarılı", f"Rapor başarıyla kaydedildi:\n{dosya_yolu}"
            )
        except Exception as ex:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{ex}")
