"""
Diyalog pencereleri - Form modalları.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDateTimeEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt, QDateTime

from backend import VeriYoneticisi, Etkinlik, Katilimci


def _form_satiri(etiket_metni: str, alan_widget) -> QVBoxLayout:
    """Form etiketi + input widget'ını dikey olarak hizalı oluşturur."""
    layout = QVBoxLayout()
    layout.setSpacing(7)
    layout.setContentsMargins(0, 0, 0, 0)

    etiket = QLabel(etiket_metni)
    etiket.setObjectName("FormEtiket")

    alan_widget.setMinimumHeight(40)

    layout.addWidget(etiket)
    layout.addWidget(alan_widget)
    return layout


def _diyalog_butonlari(iptal_metin="İptal", kaydet_metin="Kaydet"):
    """Standart iptal + kaydet buton grubu."""
    iptal_btn = QPushButton(iptal_metin)
    iptal_btn.setObjectName("HayaletButon")
    iptal_btn.setFixedHeight(40)
    iptal_btn.setMinimumWidth(100)
    iptal_btn.setCursor(Qt.PointingHandCursor)

    kaydet_btn = QPushButton(kaydet_metin)
    kaydet_btn.setObjectName("PrimaryButon")
    kaydet_btn.setStyleSheet(
        "QPushButton { background-color: #a855f7; color: white; "
        "border: none; border-radius: 8px; "
        "padding-left: 18px; padding-right: 18px; "
        "font-size: 13px; font-weight: 600; } "
        "QPushButton:hover { background-color: #9333ea; }"
    )
    kaydet_btn.setFixedHeight(40)
    kaydet_btn.setMinimumWidth(120)
    kaydet_btn.setCursor(Qt.PointingHandCursor)

    return iptal_btn, kaydet_btn


class EtkinlikDiyalog(QDialog):
    """Etkinlik ekleme / düzenleme."""

    def __init__(self, vy: VeriYoneticisi, etkinlik: Etkinlik = None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.etkinlik = etkinlik
        self.duzenleme_modu = etkinlik is not None

        self.setWindowTitle(
            "Etkinlik Düzenle" if self.duzenleme_modu else "Yeni Etkinlik"
        )
        self.setMinimumWidth(480)
        self.setModal(True)

        self._arayuz_olustur()

        if self.duzenleme_modu:
            self._mevcut_verileri_yukle()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(32, 28, 32, 24)
        ana.setSpacing(20)

        # Başlık
        baslik = QLabel(
            "Etkinliği Düzenle" if self.duzenleme_modu else "Yeni Etkinlik Oluştur"
        )
        baslik.setObjectName("SayfaBaslik")
        ana.addWidget(baslik)

        alt = QLabel(
            "Etkinlik bilgilerini doldurun. Tüm alanlar zorunludur."
        )
        alt.setObjectName("SayfaAltBaslik")
        ana.addWidget(alt)

        # Form alanları
        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Örn: Python Workshop")
        self.ad_input.returnPressed.connect(self._kaydet)

        self.tarih_input = QDateTimeEdit()
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDateTime(QDateTime.currentDateTime().addDays(7))
        self.tarih_input.setDisplayFormat("dd.MM.yyyy  HH:mm")
        # Geçmişe set edilemez — kullanıcı bunu seçemesin
        self.tarih_input.setMinimumDateTime(QDateTime.currentDateTime())

        self.kapasite_input = QSpinBox()
        self.kapasite_input.setRange(1, 100000)
        self.kapasite_input.setValue(50)

        ana.addLayout(_form_satiri("Etkinlik Adı", self.ad_input))
        ana.addLayout(_form_satiri("Tarih ve Saat", self.tarih_input))
        ana.addLayout(_form_satiri("Kapasite", self.kapasite_input))

        ana.addStretch()

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn, kaydet_btn = _diyalog_butonlari(
            kaydet_metin="Güncelle" if self.duzenleme_modu else "Etkinliği Oluştur"
        )
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(kaydet_btn)

        ana.addLayout(btn_layout)

    def _mevcut_verileri_yukle(self):
        from datetime import datetime
        self.ad_input.setText(self.etkinlik.ad)

        # Geçmiş etkinlik: tarihi göster ama düzenlenemesin
        if self.etkinlik.tarih < datetime.now():
            self.tarih_input.setMinimumDateTime(QDateTime(self.etkinlik.tarih))
            self.tarih_input.setDateTime(QDateTime(self.etkinlik.tarih))
            self.tarih_input.setEnabled(False)
            self.tarih_input.setToolTip(
                "Geçmişte gerçekleşen etkinliğin tarihi değiştirilemez."
            )
        else:
            self.tarih_input.setDateTime(QDateTime(self.etkinlik.tarih))

        self.kapasite_input.setValue(self.etkinlik.kapasite)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        tarih = self.tarih_input.dateTime().toPyDateTime()
        kapasite = self.kapasite_input.value()

        if not ad:
            QMessageBox.warning(self, "Eksik Bilgi", "Etkinlik adı boş olamaz.")
            return

        try:
            if self.duzenleme_modu:
                self.vy.etkinlik_guncelle(
                    self.etkinlik.etkinlik_id, ad, tarih, kapasite
                )
            else:
                self.vy.etkinlik_ekle(ad, tarih, kapasite)
            self.accept()
        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Hata", str(e))


class KatilimciDiyalog(QDialog):
    """Katılımcı ekleme / düzenleme."""

    def __init__(
        self, vy: VeriYoneticisi, katilimci: Katilimci = None, parent=None
    ):
        super().__init__(parent)
        self.vy = vy
        self.katilimci = katilimci
        self.duzenleme_modu = katilimci is not None

        self.setWindowTitle(
            "Katılımcı Düzenle" if self.duzenleme_modu else "Yeni Katılımcı"
        )
        self.setMinimumWidth(480)
        self.setModal(True)

        self._arayuz_olustur()

        if self.duzenleme_modu:
            self._mevcut_verileri_yukle()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(32, 28, 32, 24)
        ana.setSpacing(20)

        baslik = QLabel(
            "Katılımcıyı Düzenle"
            if self.duzenleme_modu
            else "Yeni Katılımcı Ekle"
        )
        baslik.setObjectName("SayfaBaslik")
        ana.addWidget(baslik)

        alt = QLabel("E-posta adresi sistem genelinde benzersiz olmalıdır.")
        alt.setObjectName("SayfaAltBaslik")
        ana.addWidget(alt)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Örn: Beko Yılmaz")
        self.ad_input.returnPressed.connect(lambda: self.email_input.setFocus())

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ornek@domain.com")
        self.email_input.returnPressed.connect(self._kaydet)

        ana.addLayout(_form_satiri("Ad Soyad", self.ad_input))
        ana.addLayout(_form_satiri("E-posta", self.email_input))

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn, kaydet_btn = _diyalog_butonlari(
            kaydet_metin="Güncelle"
            if self.duzenleme_modu
            else "Katılımcıyı Ekle"
        )
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(kaydet_btn)

        ana.addLayout(btn_layout)

    def _mevcut_verileri_yukle(self):
        self.ad_input.setText(self.katilimci.ad)
        self.email_input.setText(self.katilimci.email)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        email = self.email_input.text().strip()

        if not ad:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad soyad boş olamaz.")
            self.ad_input.setFocus()
            return
        if not email:
            QMessageBox.warning(self, "Eksik Bilgi", "E-posta boş olamaz.")
            self.email_input.setFocus()
            return

        # Hızlı format kontrolü - kullanıcıya net mesaj
        if "@" not in email or "." not in email.split("@")[-1]:
            QMessageBox.warning(
                self, "Geçersiz E-posta",
                "Lütfen geçerli bir e-posta adresi girin.\n\n"
                "Örnek: ornek@domain.com"
            )
            self.email_input.setFocus()
            return

        try:
            if self.duzenleme_modu:
                self.vy.katilimci_guncelle(self.katilimci.katilimci_id, ad, email)
            else:
                self.vy.katilimci_ekle(ad, email)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
            self.email_input.setFocus()


class BiletOlusturDiyalog(QDialog):
    """Bilet oluşturma diyaloğu."""

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy

        self.setWindowTitle("Yeni Bilet Oluştur")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(32, 28, 32, 24)
        ana.setSpacing(20)

        baslik = QLabel("Yeni Bilet Oluştur")
        baslik.setObjectName("SayfaBaslik")
        ana.addWidget(baslik)

        alt = QLabel("Bir katılımcıyı bir etkinliğe kaydedin.")
        alt.setObjectName("SayfaAltBaslik")
        ana.addWidget(alt)

        self.etkinlik_combo = QComboBox()
        self._etkinlikleri_yukle()
        self.etkinlik_combo.currentIndexChanged.connect(self._bilgi_guncelle)

        self.katilimci_combo = QComboBox()
        self._katilimcilari_yukle()

        ana.addLayout(_form_satiri("Etkinlik", self.etkinlik_combo))
        ana.addLayout(_form_satiri("Katılımcı", self.katilimci_combo))

        # Bilgi kutusu
        self.bilgi_kutu = QFrame()
        self.bilgi_kutu.setStyleSheet(
            "background-color: rgba(168, 85, 247, 0.08); "
            "border: 1px solid rgba(168, 85, 247, 0.25); "
            "border-radius: 8px;"
        )
        bilgi_layout = QHBoxLayout(self.bilgi_kutu)
        bilgi_layout.setContentsMargins(14, 10, 14, 10)

        self.bilgi_lbl = QLabel("")
        self.bilgi_lbl.setStyleSheet(
            "color: #c4b5fd; font-size: 12px; background: transparent; border: none;"
        )
        self.bilgi_lbl.setWordWrap(True)
        bilgi_layout.addWidget(self.bilgi_lbl)

        ana.addWidget(self.bilgi_kutu)

        self._bilgi_guncelle()

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn = QPushButton("İptal")
        iptal_btn.setObjectName("HayaletButon")
        iptal_btn.setFixedHeight(40)
        iptal_btn.setMinimumWidth(100)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)

        olustur_btn = QPushButton("Bilet Oluştur")
        olustur_btn.setObjectName("BasariButon")
        olustur_btn.setStyleSheet(
            "QPushButton { background-color: #10d9a0; color: #032e22; "
            "border: none; border-radius: 8px; "
            "padding-left: 18px; padding-right: 18px; "
            "font-size: 13px; font-weight: 700; } "
            "QPushButton:hover { background-color: #06d6a0; }"
        )
        olustur_btn.setFixedHeight(40)
        olustur_btn.setMinimumWidth(140)
        olustur_btn.setCursor(Qt.PointingHandCursor)
        olustur_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(olustur_btn)

        ana.addLayout(btn_layout)

    def _etkinlikleri_yukle(self):
        self.etkinlik_combo.clear()
        for e in self.vy.tum_etkinlikler():
            etiket = (
                f"{e.ad}   ·   {e.tarih.strftime('%d.%m.%Y %H:%M')}   "
                f"·   {e.katilimci_sayisi()}/{e.kapasite}"
            )
            self.etkinlik_combo.addItem(etiket, e.etkinlik_id)

    def _katilimcilari_yukle(self):
        self.katilimci_combo.clear()
        for k in self.vy.tum_katilimcilar():
            self.katilimci_combo.addItem(f"{k.ad}   ·   {k.email}", k.katilimci_id)

    def _bilgi_guncelle(self):
        eid = self.etkinlik_combo.currentData()
        if eid is None:
            self.bilgi_lbl.setText("Önce bir etkinlik oluşturmalısınız.")
            return
        e = self.vy.etkinlik_getir(eid)
        if e:
            kalan = e.kalan_kontenjan()
            if kalan > 0:
                self.bilgi_lbl.setText(
                    f"Bu etkinlikte <b>{kalan}</b> kontenjan kaldı."
                )
            else:
                self.bilgi_lbl.setText(
                    "Bu etkinliğin kapasitesi dolmuştur."
                )

    def _kaydet(self):
        eid = self.etkinlik_combo.currentData()
        kid = self.katilimci_combo.currentData()

        if eid is None or kid is None:
            QMessageBox.warning(
                self, "Eksik Veri", "Lütfen etkinlik ve katılımcı seçin."
            )
            return

        try:
            bilet = self.vy.bilet_olustur(eid, kid)
            QMessageBox.information(
                self,
                "Bilet Oluşturuldu",
                f"Bilet başarıyla oluşturuldu.\n\nBilet Kodu: {bilet.kod}",
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
