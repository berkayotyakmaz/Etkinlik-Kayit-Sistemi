"""
Login Penceresi - Yetkisiz girişi engeller.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QLinearGradient,
    QRadialGradient,
    QPen,
    QBrush,
    QFont,
    QPainterPath,
)

from backend import AuthYoneticisi, Kullanici
from frontend.widgets.bilesenler import GlowLogo


class _AuroraPanel(QWidget):
    """Login penceresinin sol tarafı - büyük gradient brand panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(420)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # Ana gradient bg
        grad = QLinearGradient(0, 0, rect.width(), rect.height())
        grad.setColorAt(0.0, QColor("#1a1230"))
        grad.setColorAt(0.5, QColor("#2a1a4a"))
        grad.setColorAt(1.0, QColor("#15101e"))
        p.fillRect(rect, grad)

        # Sol üst mor halka
        glow1 = QRadialGradient(rect.width() * 0.2, rect.height() * 0.25, rect.height() * 0.7)
        c1 = QColor("#b265ff")
        c1.setAlpha(120)
        c2 = QColor("#b265ff")
        c2.setAlpha(0)
        glow1.setColorAt(0.0, c1)
        glow1.setColorAt(1.0, c2)
        p.fillRect(rect, glow1)

        # Sağ alt pembe halka
        glow2 = QRadialGradient(rect.width() * 0.85, rect.height() * 0.85, rect.height() * 0.6)
        c3 = QColor("#ec4899")
        c3.setAlpha(90)
        c4 = QColor("#ec4899")
        c4.setAlpha(0)
        glow2.setColorAt(0.0, c3)
        glow2.setColorAt(1.0, c4)
        p.fillRect(rect, glow2)

        # Dot grid
        nokta_renk = QColor(255, 255, 255, 18)
        p.setBrush(nokta_renk)
        p.setPen(Qt.NoPen)
        for x in range(30, rect.width(), 26):
            for y in range(30, rect.height(), 26):
                p.drawEllipse(QPointF(x, y), 0.9, 0.9)

        # Dekoratif dairesel çizgi (sağ alt)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(255, 255, 255, 25), 1))
        for r in [200, 280, 360]:
            p.drawEllipse(
                QPointF(rect.width() + 30, rect.height() + 30), r, r
            )

        # Tag
        tag_x, tag_y = 48, 56
        # Mor marker çizgisi
        p.setBrush(QColor("#b265ff"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(tag_x, tag_y - 3, 22, 3), 1.5, 1.5)

        # EVENTHUB tag - marker'ın yanında
        p.setPen(QColor("#c4b5fd"))
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.8)
        p.setFont(font)
        p.drawText(int(tag_x + 32), int(tag_y + 4), "EVENTHUB")

        # Büyük başlık - satır satır çizilsin
        baslik_satirlari = [
            "Etkinliklerini",
            "yönetmenin",
            "akıllı yolu.",
        ]
        font = QFont("Inter", 36, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.5)
        p.setFont(font)
        p.setPen(QColor("#ffffff"))
        baslik_y = 120
        for satir in baslik_satirlari:
            p.drawText(int(tag_x), int(baslik_y), satir)
            baslik_y += 48

        # Alt metin
        p.setPen(QColor("#c4b5fd"))
        font = QFont("Inter", 12)
        p.setFont(font)
        p.drawText(int(tag_x), int(baslik_y + 16), "Tek panelden etkinlik, katılımcı ve")
        p.drawText(int(tag_x), int(baslik_y + 36), "bilet operasyonlarını yönetin.")

        # Alt feature listesi
        ozellikler = [
            ("✦", "Gerçek zamanlı doluluk takibi"),
            ("◆", "Otomatik bilet oluşturma"),
            ("◊", "Detaylı katılım raporları"),
        ]

        ozellik_y = rect.height() - 220
        for ikon, metin in ozellikler:
            # İkon
            p.setPen(QColor("#b265ff"))
            font = QFont("Inter", 14, QFont.Bold)
            p.setFont(font)
            p.drawText(int(tag_x), int(ozellik_y + 18), ikon)

            # Metin
            p.setPen(QColor("#e9d5ff"))
            font = QFont("Inter", 11)
            p.setFont(font)
            p.drawText(int(tag_x + 28), int(ozellik_y + 18), metin)
            ozellik_y += 38

        # En altta footer
        p.setPen(QColor("#8d8da3"))
        font = QFont("Inter", 9)
        p.setFont(font)
        p.drawText(int(tag_x), int(rect.height() - 36), "© 2026 EventHub  ·  v1.0")


class LoginPenceresi(QDialog):
    """Login dialog. exec_() döndüğünde self.dogrulanan_kullanici dolu olur."""

    def __init__(self, auth: AuthYoneticisi, parent=None):
        super().__init__(parent)
        self.auth = auth
        self.dogrulanan_kullanici: Kullanici | None = None

        self.setWindowTitle("EventHub — Giriş")
        self.setFixedSize(900, 600)
        self.setModal(True)

        # Çerçevesiz gibi görünsün ama Qt'nin çerçevesi kalsın
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        # SOL: aurora panel
        ana.addWidget(_AuroraPanel())

        # SAĞ: form alanı
        sag = QFrame()
        sag.setStyleSheet("background-color: #0a0a12;")
        sag_layout = QVBoxLayout(sag)
        sag_layout.setContentsMargins(56, 48, 56, 48)
        sag_layout.setSpacing(0)

        # Üst: logo + isim
        ust_satir = QHBoxLayout()
        ust_satir.setSpacing(12)
        logo = GlowLogo(36)
        marka = QLabel("EventHub")
        marka.setStyleSheet(
            "color: #ffffff; font-size: 18px; font-weight: 800; "
            "background: transparent; border: none; letter-spacing: -0.3px;"
        )
        ust_satir.addWidget(logo)
        ust_satir.addWidget(marka)
        ust_satir.addStretch()
        sag_layout.addLayout(ust_satir)
        sag_layout.addSpacing(56)

        # Başlık
        baslik = QLabel("Hoş Geldin")
        baslik.setStyleSheet(
            "color: #ffffff; font-size: 30px; font-weight: 800; "
            "background: transparent; border: none; letter-spacing: -0.6px;"
        )
        sag_layout.addWidget(baslik)

        alt_baslik = QLabel("Devam etmek için hesabına giriş yap.")
        alt_baslik.setStyleSheet(
            "color: #8d8da3; font-size: 13px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(alt_baslik)
        sag_layout.addSpacing(36)

        # Form etiketi 1
        sag_layout.addWidget(self._etiket("KULLANICI ADI"))
        sag_layout.addSpacing(7)

        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("kullanıcı adınızı girin")
        self.kul_input.setFixedHeight(46)
        self.kul_input.setStyleSheet(self._input_stil())
        self.kul_input.returnPressed.connect(lambda: self.sifre_input.setFocus())
        sag_layout.addWidget(self.kul_input)
        sag_layout.addSpacing(20)

        # Form etiketi 2
        sag_layout.addWidget(self._etiket("ŞİFRE"))
        sag_layout.addSpacing(7)

        # Şifre + göster butonu
        sifre_sarici = QHBoxLayout()
        sifre_sarici.setSpacing(0)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("••••••••")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setFixedHeight(46)
        self.sifre_input.setStyleSheet(self._input_stil())
        self.sifre_input.returnPressed.connect(self._giris_yap)
        sifre_sarici.addWidget(self.sifre_input)

        sag_layout.addLayout(sifre_sarici)
        sag_layout.addSpacing(14)

        # Göster checkbox + ipucu
        alt_satir = QHBoxLayout()

        self.goster_chk = QCheckBox("Şifreyi göster")
        self.goster_chk.setStyleSheet(
            "QCheckBox { color: #8d8da3; font-size: 12px; "
            "background: transparent; border: none; spacing: 8px; }"
            "QCheckBox::indicator { width: 14px; height: 14px; "
            "border: 1px solid #2c2c44; border-radius: 3px; "
            "background-color: #11111c; }"
            "QCheckBox::indicator:checked { background-color: #b265ff; "
            "border: 1px solid #b265ff; }"
        )
        self.goster_chk.toggled.connect(self._sifre_goster)
        alt_satir.addWidget(self.goster_chk)
        alt_satir.addStretch()

        sag_layout.addLayout(alt_satir)
        sag_layout.addSpacing(28)

        # Hata satırı (gizli başlangıç)
        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: rgba(244, 63, 94, 0.1); "
            "color: #f43f5e; "
            "border: 1px solid rgba(244, 63, 94, 0.3); "
            "border-radius: 8px; padding: 10px 14px; "
            "font-size: 12px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        sag_layout.addWidget(self.hata_lbl)

        # Giriş butonu
        self.giris_btn = QPushButton("Giriş Yap")
        self.giris_btn.setFixedHeight(48)
        self.giris_btn.setCursor(Qt.PointingHandCursor)
        self.giris_btn.setStyleSheet(
            "QPushButton { background-color: #b265ff; color: white; "
            "border: none; border-radius: 10px; "
            "font-size: 14px; font-weight: 700; letter-spacing: 0.3px; } "
            "QPushButton:hover { background-color: #9333ea; } "
            "QPushButton:pressed { background-color: #7e22ce; }"
        )
        self.giris_btn.clicked.connect(self._giris_yap)
        sag_layout.addWidget(self.giris_btn)
        sag_layout.addSpacing(16)

        # İpucu - varsayılan kullanıcı
        ipucu = QLabel(
            "<span style='color:#5a5a72;'>Varsayılan giriş:</span>  "
            "<span style='color:#c4b5fd; font-weight:600;'>admin</span>  "
            "<span style='color:#5a5a72;'>/</span>  "
            "<span style='color:#c4b5fd; font-weight:600;'>admin123</span>"
        )
        ipucu.setStyleSheet(
            "background-color: #11111c; "
            "border: 1px solid #1f1f2e; "
            "border-radius: 8px; padding: 12px 14px; "
            "font-size: 12px;"
        )
        ipucu.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(ipucu)

        sag_layout.addStretch()

        ana.addWidget(sag, 1)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #8d8da3; font-size: 10px; font-weight: 700; "
            "letter-spacing: 1.2px; background: transparent; border: none;"
        )
        return lbl

    def _input_stil(self) -> str:
        return (
            "QLineEdit { background-color: #11111c; "
            "border: 1px solid #2c2c44; border-radius: 10px; "
            "padding: 0 16px; color: #f8f8fc; font-size: 14px; "
            "selection-background-color: #b265ff; } "
            "QLineEdit:focus { border: 1px solid #b265ff; "
            "background-color: #171723; } "
            "QLineEdit:hover { border: 1px solid #3d2c5c; }"
        )

    def _sifre_goster(self, checked: bool):
        self.sifre_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )

    def _hata_goster(self, mesaj: str):
        self.hata_lbl.setText(f"⚠  {mesaj}")
        self.hata_lbl.setVisible(True)

    def _hata_gizle(self):
        self.hata_lbl.setVisible(False)

    def _giris_yap(self):
        kul = self.kul_input.text().strip()
        sifre = self.sifre_input.text()

        if not kul:
            self._hata_goster("Kullanıcı adı boş olamaz.")
            self.kul_input.setFocus()
            return
        if not sifre:
            self._hata_goster("Şifre boş olamaz.")
            self.sifre_input.setFocus()
            return

        kullanici = self.auth.dogrula(kul, sifre)
        if kullanici is None:
            self._hata_goster("Kullanıcı adı veya şifre hatalı.")
            self.sifre_input.clear()
            self.sifre_input.setFocus()
            return

        # Başarılı
        self.dogrulanan_kullanici = kullanici
        self.accept()
