"""
Ana Pencere - Sidebar + içerik yığını.
"""
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QButtonGroup,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi
from frontend.tema import ANA_STIL
from frontend.widgets.bilesenler import GlowLogo, Avatar
from frontend.views.dashboard import DashboardSayfasi
from frontend.views.etkinlikler import EtkinliklerSayfasi
from frontend.views.katilimcilar import KatilimcilarSayfasi
from frontend.views.biletler import BiletlerSayfasi
from frontend.views.raporlar import RaporlarSayfasi


class AnaPencere(QMainWindow):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None):
        super().__init__()
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici

        self.setWindowTitle("EventHub — Etkinlik Kayıt Sistemi")
        self.setMinimumSize(1180, 740)
        self.resize(1380, 860)

        # Stil app seviyesinde uygulanır (main.py)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        merkez = QWidget()
        ana = QHBoxLayout(merkez)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        sidebar = self._sidebar_olustur()
        ana.addWidget(sidebar)

        # İçerik alanı
        icerik_sarici = QWidget()
        icerik_sarici.setStyleSheet("background-color: #0e0e14;")
        icerik_layout = QVBoxLayout(icerik_sarici)
        icerik_layout.setContentsMargins(0, 0, 0, 0)
        icerik_layout.setSpacing(0)

        self.yigin = QStackedWidget()

        self.sayfa_dashboard = DashboardSayfasi(self.vy)
        self.sayfa_etkinlikler = EtkinliklerSayfasi(self.vy)
        self.sayfa_katilimcilar = KatilimcilarSayfasi(self.vy)
        self.sayfa_biletler = BiletlerSayfasi(self.vy)
        self.sayfa_raporlar = RaporlarSayfasi(self.vy)

        # Veri değişimi cross-page
        self.sayfa_etkinlikler.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_katilimcilar.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_biletler.veri_degisti.connect(self._tumunu_yenile)

        self.yigin.addWidget(self.sayfa_dashboard)
        self.yigin.addWidget(self.sayfa_etkinlikler)
        self.yigin.addWidget(self.sayfa_katilimcilar)
        self.yigin.addWidget(self.sayfa_biletler)
        self.yigin.addWidget(self.sayfa_raporlar)

        icerik_layout.addWidget(self.yigin)

        ana.addWidget(icerik_sarici, 1)

        self.setCentralWidget(merkez)
        self.yigin.setCurrentIndex(0)

    def _sidebar_olustur(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(248)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 24, 0, 16)
        layout.setSpacing(0)

        # Logo
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(22, 0, 22, 0)
        logo_layout.setSpacing(12)

        logo_ikon = GlowLogo(40)

        logo_text_l = QVBoxLayout()
        logo_text_l.setSpacing(2)
        baslik = QLabel("EventHub")
        baslik.setObjectName("SidebarBaslik")
        alt = QLabel("ETKİNLİK SİSTEMİ")
        alt.setObjectName("SidebarAltBaslik")
        logo_text_l.addWidget(baslik)
        logo_text_l.addWidget(alt)

        logo_layout.addWidget(logo_ikon)
        logo_layout.addLayout(logo_text_l)
        logo_layout.addStretch()

        layout.addLayout(logo_layout)
        layout.addSpacing(32)

        # Menu - "Genel" grubu
        genel_baslik = QLabel("GENEL")
        genel_baslik.setObjectName("MenuBaslik")
        genel_baslik.setContentsMargins(22, 0, 22, 8)
        layout.addWidget(genel_baslik)

        self.buton_grubu = QButtonGroup(self)
        self.buton_grubu.setExclusive(True)

        self._menu_butonu_ekle(layout, "◇", "Kontrol Paneli", 0)

        layout.addSpacing(20)

        # "Yönetim" grubu
        yonetim_baslik = QLabel("YÖNETİM")
        yonetim_baslik.setObjectName("MenuBaslik")
        yonetim_baslik.setContentsMargins(22, 0, 22, 8)
        layout.addWidget(yonetim_baslik)

        self._menu_butonu_ekle(layout, "◈", "Etkinlikler", 1)
        self._menu_butonu_ekle(layout, "◉", "Katılımcılar", 2)
        self._menu_butonu_ekle(layout, "✦", "Biletler", 3)

        layout.addSpacing(20)

        # "Analiz" grubu
        analiz_baslik = QLabel("ANALİZ")
        analiz_baslik.setObjectName("MenuBaslik")
        analiz_baslik.setContentsMargins(22, 0, 22, 8)
        layout.addWidget(analiz_baslik)

        self._menu_butonu_ekle(layout, "◊", "Raporlar", 4)

        # İlk butonu seç
        self.buton_grubu.button(0).setChecked(True)

        layout.addStretch()

        # Kullanıcı kartı
        kart_sarici = QHBoxLayout()
        kart_sarici.setContentsMargins(16, 0, 16, 0)

        kullanici_kart = QFrame()
        kullanici_kart.setObjectName("KullaniciKart")

        kk_layout = QHBoxLayout(kullanici_kart)
        kk_layout.setContentsMargins(12, 12, 12, 12)
        kk_layout.setSpacing(11)

        # Aktif kullanıcı bilgilerini kullan
        if self.aktif_kullanici:
            ad_str = self.aktif_kullanici.ad
            rol_str = self.aktif_kullanici.rol.capitalize()
        else:
            ad_str = "Kullanıcı"
            rol_str = "Misafir"

        avatar = Avatar(ad_str, boyut=36)

        kullanici_bilgi = QVBoxLayout()
        kullanici_bilgi.setSpacing(2)
        kullanici_bilgi.setContentsMargins(0, 0, 0, 0)

        ust_satir = QHBoxLayout()
        ust_satir.setSpacing(8)
        ust_satir.setContentsMargins(0, 0, 0, 0)

        ad = QLabel(ad_str)
        ad.setObjectName("KullaniciAd")

        plan = QLabel("PRO")
        plan.setObjectName("PlanRozet")
        plan.setAlignment(Qt.AlignCenter)

        ust_satir.addWidget(ad)
        ust_satir.addWidget(plan)
        ust_satir.addStretch()

        durum = QLabel(rol_str)
        durum.setObjectName("KullaniciDurum")

        kullanici_bilgi.addLayout(ust_satir)
        kullanici_bilgi.addWidget(durum)

        kk_layout.addWidget(avatar)
        kk_layout.addLayout(kullanici_bilgi)
        kk_layout.addStretch()

        # Çıkış butonu
        cikis_btn = QPushButton("⎋")
        cikis_btn.setObjectName("CikisButon")
        cikis_btn.setFixedSize(30, 30)
        cikis_btn.setCursor(Qt.PointingHandCursor)
        cikis_btn.setToolTip("Çıkış yap")
        cikis_btn.setStyleSheet(
            "QPushButton { background-color: transparent; "
            "color: #8d8da3; border: 1px solid #2c2c44; "
            "border-radius: 6px; font-size: 14px; padding: 0; } "
            "QPushButton:hover { color: #f43f5e; "
            "border: 1px solid rgba(244, 63, 94, 0.4); "
            "background-color: rgba(244, 63, 94, 0.08); }"
        )
        cikis_btn.clicked.connect(self._cikis_yap)
        kk_layout.addWidget(cikis_btn, 0, Qt.AlignVCenter)

        kart_sarici.addWidget(kullanici_kart)
        layout.addLayout(kart_sarici)

        return sidebar

    def _cikis_yap(self):
        from PyQt5.QtWidgets import QMessageBox
        cevap = QMessageBox.question(
            self,
            "Çıkış Yap",
            "Oturumu kapatıp giriş ekranına dönmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            # Pencereyi kapat - main.py akışı sonlandırır
            # (basit yaklaşım: tam çıkış)
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()

    def _menu_butonu_ekle(self, layout, ikon: str, metin: str, indeks: int):
        btn = QPushButton(f"  {ikon}    {metin}")
        btn.setObjectName("MenuButon")
        btn.setCheckable(True)
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda _, i=indeks: self._sayfa_degistir(i))
        self.buton_grubu.addButton(btn, indeks)
        layout.addWidget(btn)

    def _sayfa_degistir(self, indeks: int):
        self.yigin.setCurrentIndex(indeks)
        sayfa = self.yigin.widget(indeks)
        if hasattr(sayfa, "yenile"):
            sayfa.yenile()

    def _tumunu_yenile(self):
        for i in range(self.yigin.count()):
            sayfa = self.yigin.widget(i)
            if hasattr(sayfa, "yenile"):
                sayfa.yenile()
