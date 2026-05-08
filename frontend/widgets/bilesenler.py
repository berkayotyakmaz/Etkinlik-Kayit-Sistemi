"""
Premium custom-paint widget'lar.
"""
import math
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF, QPointF, QSize
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QLinearGradient,
    QRadialGradient,
    QConicalGradient,
    QPen,
    QBrush,
    QFont,
    QPainterPath,
    QPolygonF,
)


# ============================================================
# Renk yardımcıları
# ============================================================
ACC = QColor("#b265ff")
ACC2 = QColor("#ec4899")
ACC3 = QColor("#7c3aed")
SUCCESS = QColor("#10d9a0")
WARNING = QColor("#fbbf24")
DANGER = QColor("#f43f5e")
INFO = QColor("#38bdf8")

VARYANT_RENKLER = {
    "mor": (QColor("#b265ff"), QColor("#7c3aed")),
    "pembe": (QColor("#ec4899"), QColor("#db2777")),
    "mint": (QColor("#10d9a0"), QColor("#059669")),
    "amber": (QColor("#fbbf24"), QColor("#f59e0b")),
    "mavi": (QColor("#38bdf8"), QColor("#0284c7")),
}


# ============================================================
# GLOW LOGO — Aurora gradient diamond
# ============================================================
class GlowLogo(QWidget):
    """Sidebar'da kullanılan ışıltılı logo."""

    def __init__(self, boyut: int = 40, parent=None):
        super().__init__(parent)
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Glow halkası
        for i, alpha in enumerate([20, 35, 60]):
            r = w / 2 - 2 - i * 2
            col = QColor(ACC)
            col.setAlpha(alpha)
            p.setBrush(col)
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(w / 2, h / 2), r, r)

        # Aurora gradient elmas
        path = QPainterPath()
        cx, cy = w / 2, h / 2
        s = w * 0.32
        path.moveTo(cx, cy - s)
        path.lineTo(cx + s, cy)
        path.lineTo(cx, cy + s)
        path.lineTo(cx - s, cy)
        path.closeSubpath()

        grad = QLinearGradient(cx - s, cy - s, cx + s, cy + s)
        grad.setColorAt(0.0, ACC)
        grad.setColorAt(1.0, ACC2)
        p.setBrush(grad)
        p.setPen(Qt.NoPen)
        p.drawPath(path)

        # İç parlama
        path2 = QPainterPath()
        s2 = s * 0.45
        path2.moveTo(cx - s2 * 0.3, cy - s2)
        path2.lineTo(cx + s2 * 0.6, cy - s2 * 0.3)
        path2.lineTo(cx, cy + s2 * 0.2)
        path2.closeSubpath()

        glow = QColor(255, 255, 255, 90)
        p.setBrush(glow)
        p.drawPath(path2)


# ============================================================
# HERO PANEL — Gradient'li dashboard üst paneli
# ============================================================
class HeroPanel(QFrame):
    """
    Dashboard'un üstünde duran büyük, etkileyici gradient panel.
    Sol: hoşgeldin metni, sağ: yaklaşan etkinlik özeti.
    """

    def __init__(
        self,
        baslik: str,
        alt_baslik: str,
        toplam_etkinlik: int = 0,
        toplam_katilim: int = 0,
        parent=None,
    ):
        super().__init__(parent)
        self.baslik = baslik
        self.alt_baslik = alt_baslik
        self.toplam_etkinlik = toplam_etkinlik
        self.toplam_katilim = toplam_katilim
        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def degerleri_ayarla(self, etkinlik: int, katilim: int):
        self.toplam_etkinlik = etkinlik
        self.toplam_katilim = katilim
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(0, 0, -1, -1)
        rrect = QRectF(rect)

        # Ana arka plan - aurora gradient
        path = QPainterPath()
        path.addRoundedRect(rrect, 18, 18)

        grad = QLinearGradient(0, 0, rect.width(), rect.height())
        grad.setColorAt(0.0, QColor("#1a1230"))
        grad.setColorAt(0.5, QColor("#1d1338"))
        grad.setColorAt(1.0, QColor("#15101e"))
        p.fillPath(path, grad)

        # Sol taraftaki büyük renk halkası
        p.save()
        p.setClipPath(path)

        big_grad = QRadialGradient(
            rect.width() * 0.15, rect.height() * 0.5, rect.height() * 1.3
        )
        c1 = QColor(ACC)
        c1.setAlpha(60)
        c2 = QColor(ACC)
        c2.setAlpha(0)
        big_grad.setColorAt(0.0, c1)
        big_grad.setColorAt(1.0, c2)
        p.fillRect(rect, big_grad)

        # Sağ üst pembe halka
        big_grad2 = QRadialGradient(
            rect.width() * 0.95, rect.height() * 0.1, rect.height() * 1.0
        )
        c3 = QColor(ACC2)
        c3.setAlpha(50)
        c4 = QColor(ACC2)
        c4.setAlpha(0)
        big_grad2.setColorAt(0.0, c3)
        big_grad2.setColorAt(1.0, c4)
        p.fillRect(rect, big_grad2)

        # Dekoratif noktalar (gridworld)
        nokta_renk = QColor(255, 255, 255, 12)
        p.setPen(Qt.NoPen)
        p.setBrush(nokta_renk)
        for x in range(40, rect.width(), 24):
            for y in range(20, rect.height(), 24):
                p.drawEllipse(QPointF(x, y), 0.7, 0.7)

        p.restore()

        # Kenarlık
        pen = QPen(QColor("#3d2c5c"), 1)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        # SOL TARAF - Metin
        # Üstte küçük marker
        marker_x = 32
        marker_y = 36
        p.setBrush(QColor(ACC))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(marker_x, marker_y - 4, 22, 3), 1.5, 1.5)

        # Tag
        p.setPen(QColor("#c4b5fd"))
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(int(marker_x + 30), int(marker_y), "EVENTHUB")

        # Başlık
        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 26, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        p.setFont(font)
        p.drawText(QRectF(28, 50, rect.width() * 0.6, 50), Qt.AlignLeft | Qt.AlignVCenter, self.baslik)

        # Alt başlık
        p.setPen(QColor("#a8a8c0"))
        font = QFont("Inter", 11)
        p.setFont(font)
        p.drawText(QRectF(28, 100, rect.width() * 0.55, 30), Qt.AlignLeft | Qt.AlignVCenter, self.alt_baslik)

        # SAĞ TARAF - mini istatistikler
        kutucuk_w = 160
        bos_w = 24
        sag_block_w = kutucuk_w * 2 + bos_w
        sag_x_start = rect.width() - sag_block_w - 28
        sag_y = 38

        # Etkinlik kutucuğu
        p.setPen(QColor("#c4b5fd"))
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        p.setFont(font)
        p.drawText(QRectF(sag_x_start, sag_y, kutucuk_w, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "TOPLAM ETKİNLİK")

        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 38, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.5)
        p.setFont(font)
        p.drawText(QRectF(sag_x_start, sag_y + 24, kutucuk_w, 50),
                   Qt.AlignLeft | Qt.AlignVCenter, str(self.toplam_etkinlik))

        # Dikey ayraç
        ayrac_x = sag_x_start + kutucuk_w + bos_w / 2
        p.setPen(QPen(QColor("#3d2c5c"), 1))
        p.drawLine(int(ayrac_x), sag_y - 4, int(ayrac_x), sag_y + 70)

        # Katılım kutucuğu
        sag_x2 = sag_x_start + kutucuk_w + bos_w
        p.setPen(QColor("#fbcfe8"))
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        p.setFont(font)
        p.drawText(QRectF(sag_x2, sag_y, kutucuk_w, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "TOPLAM KATILIM")

        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 38, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.5)
        p.setFont(font)
        p.drawText(QRectF(sag_x2, sag_y + 24, kutucuk_w, 50),
                   Qt.AlignLeft | Qt.AlignVCenter, str(self.toplam_katilim))

        # Alt çizgi - dekoratif
        cizgi_y = rect.height() - 32
        p.setPen(QColor("#3d2c5c"))
        p.drawLine(28, cizgi_y, rect.width() - 28, cizgi_y)

        # Alt sol metin
        p.setPen(QColor("#8d8da3"))
        font = QFont("Inter", 10)
        p.setFont(font)
        p.drawText(28, int(cizgi_y + 20), "Hoş geldin Beko, sistemde her şey yolunda.")

        # Alt sağ - durum
        durum_text = "Aktif sistem  ·  Otomatik kayıt"
        font = QFont("Inter", 10)
        p.setFont(font)
        text_w = p.fontMetrics().horizontalAdvance(durum_text)

        # Sağ kenardan başla, durum metnini sağa yasla
        durum_x = rect.width() - text_w - 28
        nokta_x = durum_x - 12
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#10d9a0"))
        p.drawEllipse(QPointF(nokta_x, cizgi_y + 16), 3, 3)

        p.setPen(QColor("#8d8da3"))
        p.drawText(int(durum_x), int(cizgi_y + 20), durum_text)


# ============================================================
# METRIC KARTI — Custom paint, mini sparkline'lı
# ============================================================
class MetricKarti(QFrame):
    """
    Üst köşede ikon, ortada büyük rakam, altta mini sparkline grafik.
    Aşağı sağa fark/trend rozeti.
    """

    def __init__(
        self,
        etiket: str,
        deger: str = "0",
        ikon: str = "◆",
        renk: str = "mor",
        trend: str = "",
        spark: list = None,
        parent=None,
    ):
        super().__init__(parent)
        self.etiket = etiket
        self.deger = deger
        self.ikon = ikon
        self.renk = renk
        self.trend = trend
        self.spark = spark or []
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def deger_ayarla(self, yeni: str):
        self.deger = str(yeni)
        self.update()

    def trend_ayarla(self, trend: str):
        self.trend = trend
        self.update()

    def spark_ayarla(self, veriler: list):
        self.spark = veriler
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(0, 0, -1, -1)
        rrect = QRectF(rect)

        renk_basla, renk_bitir = VARYANT_RENKLER.get(self.renk, VARYANT_RENKLER["mor"])

        # Ana arka plan
        path = QPainterPath()
        path.addRoundedRect(rrect, 16, 16)
        p.fillPath(path, QColor("#11111c"))

        # Üst gradient şerit
        p.save()
        p.setClipPath(path)

        # Sol üstte renk halkası
        glow = QRadialGradient(rect.width() * 0.85, -30, 200)
        c1 = QColor(renk_basla)
        c1.setAlpha(45)
        c2 = QColor(renk_basla)
        c2.setAlpha(0)
        glow.setColorAt(0.0, c1)
        glow.setColorAt(1.0, c2)
        p.fillRect(rect, glow)

        # İnce çapraz çizgi (dekoratif)
        cizgi_renk = QColor(255, 255, 255, 8)
        p.setPen(QPen(cizgi_renk, 1))
        for i in range(-rect.height(), rect.width(), 14):
            p.drawLine(i, rect.height(), i + rect.height(), 0)

        p.restore()

        # Kenarlık
        p.setPen(QPen(QColor("#1f1f2e"), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        # ÜST: ikon kutusu + etiket
        ikon_boyut = 40
        ikon_x, ikon_y = 20, 18

        # Ikon arka planı (gradient)
        ikon_path = QPainterPath()
        ikon_path.addRoundedRect(QRectF(ikon_x, ikon_y, ikon_boyut, ikon_boyut), 10, 10)

        ikon_grad = QLinearGradient(ikon_x, ikon_y, ikon_x + ikon_boyut, ikon_y + ikon_boyut)
        c_start = QColor(renk_basla)
        c_start.setAlpha(50)
        c_end = QColor(renk_bitir)
        c_end.setAlpha(20)
        ikon_grad.setColorAt(0.0, c_start)
        ikon_grad.setColorAt(1.0, c_end)
        p.fillPath(ikon_path, ikon_grad)

        # Ikon çerçevesi
        p.setPen(QPen(QColor(renk_basla.red(), renk_basla.green(), renk_basla.blue(), 80), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(ikon_path)

        # Ikon harfi
        p.setPen(renk_basla)
        font = QFont("Inter", 16, QFont.Bold)
        p.setFont(font)
        p.drawText(QRectF(ikon_x, ikon_y, ikon_boyut, ikon_boyut), Qt.AlignCenter, self.ikon)

        # Etiket
        p.setPen(QColor("#8d8da3"))
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(int(ikon_x + ikon_boyut + 14), int(ikon_y + 16), self.etiket.upper())

        # Trend
        if self.trend:
            p.setPen(SUCCESS if "+" in self.trend or "%" in self.trend else QColor("#8d8da3"))
            font = QFont("Inter", 10, QFont.Bold)
            p.setFont(font)
            p.drawText(int(ikon_x + ikon_boyut + 14), int(ikon_y + 34), self.trend)

        # ORTA: büyük rakam
        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 38, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -2)
        p.setFont(font)
        p.drawText(QRectF(20, 70, rect.width() - 40, 50), Qt.AlignLeft | Qt.AlignVCenter, str(self.deger))

        # ALT: sparkline grafik
        if self.spark and len(self.spark) > 1:
            spark_y = rect.height() - 36
            spark_h = 24
            spark_w = rect.width() - 40
            spark_x = 20

            mn, mx = min(self.spark), max(self.spark)
            rng = max(mx - mn, 1)
            adim = spark_w / (len(self.spark) - 1)

            noktalar = []
            for i, v in enumerate(self.spark):
                norm = (v - mn) / rng
                x = spark_x + i * adim
                y = spark_y + spark_h - norm * spark_h
                noktalar.append(QPointF(x, y))

            # Dolgu alanı
            fill_path = QPainterPath()
            fill_path.moveTo(QPointF(spark_x, spark_y + spark_h))
            for pt in noktalar:
                fill_path.lineTo(pt)
            fill_path.lineTo(QPointF(spark_x + spark_w, spark_y + spark_h))
            fill_path.closeSubpath()

            fill_grad = QLinearGradient(0, spark_y, 0, spark_y + spark_h)
            cf1 = QColor(renk_basla)
            cf1.setAlpha(80)
            cf2 = QColor(renk_basla)
            cf2.setAlpha(0)
            fill_grad.setColorAt(0.0, cf1)
            fill_grad.setColorAt(1.0, cf2)
            p.fillPath(fill_path, fill_grad)

            # Çizgi
            line_pen = QPen(renk_basla, 2)
            line_pen.setCapStyle(Qt.RoundCap)
            line_pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(line_pen)
            p.setBrush(Qt.NoBrush)
            for i in range(len(noktalar) - 1):
                p.drawLine(noktalar[i], noktalar[i + 1])

            # Son nokta vurgusu
            son = noktalar[-1]
            p.setBrush(QColor("#11111c"))
            p.setPen(QPen(renk_basla, 2))
            p.drawEllipse(son, 4, 4)


# ============================================================
# DAİRESEL GAUGE — Doluluk yüzde göstergesi
# ============================================================
class DairesselGauge(QWidget):
    """Dairesel doluluk göstergesi."""

    def __init__(self, deger: int = 0, etiket: str = "Doluluk", boyut: int = 140, parent=None):
        super().__init__(parent)
        self.deger = deger  # 0-100
        self.etiket = etiket
        self.setFixedSize(boyut, boyut)

    def deger_ayarla(self, deger: int):
        self.deger = max(0, min(100, deger))
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        margin = 12
        rect = QRectF(margin, margin, w - margin * 2, h - margin * 2)

        # Arka plan halkası
        pen_bg = QPen(QColor("#1f1f2e"), 8)
        pen_bg.setCapStyle(Qt.RoundCap)
        p.setPen(pen_bg)
        p.setBrush(Qt.NoBrush)
        p.drawArc(rect, 90 * 16, -360 * 16)

        # Renk seç
        if self.deger >= 90:
            renk = DANGER
        elif self.deger >= 70:
            renk = WARNING
        else:
            renk = SUCCESS

        # Aktif yay
        if self.deger > 0:
            pen_fg = QPen(renk, 8)
            pen_fg.setCapStyle(Qt.RoundCap)
            p.setPen(pen_fg)
            yay = int(-self.deger / 100 * 360 * 16)
            p.drawArc(rect, 90 * 16, yay)

        # Ortada metin
        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 22, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, f"%{self.deger}")

        # Etiket
        p.setPen(QColor("#8d8da3"))
        font = QFont("Inter", 8, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        p.setFont(font)
        p.drawText(QRectF(0, h - 26, w, 16), Qt.AlignCenter, self.etiket.upper())


# ============================================================
# KARTLAR
# ============================================================
class Kart(QFrame):
    """Genel amaçlı kart container."""

    def __init__(self, baslik: str = None, alt_baslik: str = None, parent=None):
        super().__init__(parent)
        self.setObjectName("Kart")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 22, 24, 22)
        self.layout.setSpacing(18)

        if baslik:
            baslik_layout = QVBoxLayout()
            baslik_layout.setSpacing(4)
            baslik_layout.setContentsMargins(0, 0, 0, 0)

            self.baslik_lbl = QLabel(baslik)
            self.baslik_lbl.setObjectName("KartBaslik")
            baslik_layout.addWidget(self.baslik_lbl)

            if alt_baslik:
                self.alt_baslik_lbl = QLabel(alt_baslik)
                self.alt_baslik_lbl.setObjectName("KartAltBaslik")
                baslik_layout.addWidget(self.alt_baslik_lbl)

            self.layout.addLayout(baslik_layout)


# ============================================================
# DOLULUK GÖSTERGESİ — Yatay progress bar (tablolarda)
# ============================================================
class DolulukGosterge(QWidget):
    """Yatay doluluk barı — gradient'li ve daha şık."""

    def __init__(self, mevcut: int, kapasite: int, parent=None):
        super().__init__(parent)
        self.mevcut = mevcut
        self.kapasite = kapasite
        self.setMinimumWidth(180)
        self.setFixedHeight(38)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        yuzde = (self.mevcut / self.kapasite * 100) if self.kapasite else 0
        yuzde = max(0, min(100, yuzde))

        # Renk
        if yuzde >= 90:
            renk = DANGER
        elif yuzde >= 70:
            renk = WARNING
        else:
            renk = SUCCESS

        # ÜST: metin satırı
        # Sol: oran
        p.setPen(QColor("#f8f8fc"))
        font = QFont("Inter", 11, QFont.Bold)
        p.setFont(font)
        p.drawText(QRectF(0, 0, w * 0.5, 16), Qt.AlignLeft | Qt.AlignVCenter, f"{self.mevcut}")

        # Sol2: /kapasite
        p.setPen(QColor("#5a5a72"))
        font = QFont("Inter", 11)
        p.setFont(font)
        adlar_w = p.fontMetrics().horizontalAdvance(str(self.mevcut))
        p.drawText(QRectF(adlar_w + 4, 0, w * 0.5, 16), Qt.AlignLeft | Qt.AlignVCenter, f"/ {self.kapasite}")

        # Sağ: yüzde
        p.setPen(renk)
        font = QFont("Inter", 10, QFont.Bold)
        p.setFont(font)
        p.drawText(QRectF(0, 0, w, 16), Qt.AlignRight | Qt.AlignVCenter, f"%{yuzde:.0f}")

        # ALT: bar
        bar_y = 22
        bar_h = 6
        bar_w = w

        # Track
        track_path = QPainterPath()
        track_path.addRoundedRect(QRectF(0, bar_y, bar_w, bar_h), bar_h / 2, bar_h / 2)
        p.fillPath(track_path, QColor("#1c1c2c"))

        # Fill
        fill_w = bar_w * yuzde / 100
        if fill_w > 0:
            fill_path = QPainterPath()
            fill_path.addRoundedRect(QRectF(0, bar_y, fill_w, bar_h), bar_h / 2, bar_h / 2)

            grad = QLinearGradient(0, bar_y, fill_w, bar_y)
            c1 = QColor(renk)
            c2 = QColor(renk)
            c2.setAlpha(180)
            grad.setColorAt(0.0, c2)
            grad.setColorAt(1.0, c1)
            p.fillPath(fill_path, grad)


# ============================================================
# AVATAR
# ============================================================
class Avatar(QWidget):
    """Renkli baş harf avatarı."""

    PALETLER = [
        (QColor("#b265ff"), QColor("#7c3aed")),
        (QColor("#10d9a0"), QColor("#059669")),
        (QColor("#fbbf24"), QColor("#f59e0b")),
        (QColor("#ec4899"), QColor("#db2777")),
        (QColor("#38bdf8"), QColor("#0284c7")),
        (QColor("#f43f5e"), QColor("#e11d48")),
    ]

    def __init__(self, ad: str, boyut: int = 36, parent=None):
        super().__init__(parent)
        self.ad = ad.strip()
        self.bas_harf = self.ad[0].upper() if self.ad else "?"
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        c1, c2 = self.PALETLER[hash(self.ad) % len(self.PALETLER)]

        # Glow
        glow = QRadialGradient(w / 2, h / 2, w / 2)
        c_glow = QColor(c1)
        c_glow.setAlpha(60)
        glow.setColorAt(0.5, c_glow)
        c_glow2 = QColor(c1)
        c_glow2.setAlpha(0)
        glow.setColorAt(1.0, c_glow2)
        p.setBrush(glow)
        p.setPen(Qt.NoPen)
        p.drawEllipse(2, 2, w - 4, h - 4)

        # Ana daire
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, c1)
        grad.setColorAt(1.0, c2)
        p.setBrush(grad)
        p.setPen(Qt.NoPen)
        p.drawEllipse(4, 4, w - 8, h - 8)

        # Üst parlama
        upper = QRadialGradient(w / 2, h * 0.3, w * 0.4)
        ug1 = QColor(255, 255, 255, 80)
        ug2 = QColor(255, 255, 255, 0)
        upper.setColorAt(0.0, ug1)
        upper.setColorAt(1.0, ug2)
        p.setBrush(upper)
        p.drawEllipse(4, 4, w - 8, h - 8)

        # Harf
        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", int(w * 0.42), QFont.Bold)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.bas_harf)


# ============================================================
# BİLET KOD ROZETİ
# ============================================================
class BiletKodRozet(QWidget):
    """Mor gradient bilet kodu rozeti."""

    def __init__(self, kod: str, parent=None):
        super().__init__(parent)
        self.kod = kod
        font = QFont("Consolas", 11, QFont.Bold)
        fm = self._fm = font
        self.setFixedSize(150, 28)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(2, 2, -2, -2)
        rrect = QRectF(rect)

        path = QPainterPath()
        path.addRoundedRect(rrect, 7, 7)

        # Gradient bg
        grad = QLinearGradient(0, 0, rect.width(), 0)
        c1 = QColor(178, 101, 255, 35)
        c2 = QColor(236, 72, 153, 35)
        grad.setColorAt(0.0, c1)
        grad.setColorAt(1.0, c2)
        p.fillPath(path, grad)

        # Border
        p.setPen(QPen(QColor(178, 101, 255, 100), 1))
        p.drawPath(path)

        # Sol süs daire
        p.setBrush(QColor("#b265ff"))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(rect.left() + 11, rect.center().y()), 2.5, 2.5)

        # Kod metin
        p.setPen(QColor("#e9d5ff"))
        font = QFont("Consolas", 10, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
        p.setFont(font)
        p.drawText(
            QRectF(rect.left() + 22, rect.top(), rect.width() - 30, rect.height()),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.kod,
        )


# ============================================================
# Yardımcı sarmalayıcılar
# ============================================================
class Rozet(QLabel):
    """Renkli pill rozet."""

    OBJECT_NAMES = {
        "basari": "RozetBasari",
        "uyari": "RozetUyari",
        "tehlike": "RozetTehlike",
        "notr": "RozetNotr",
    }

    def __init__(self, metin: str, tip: str = "basari", parent=None):
        super().__init__(metin, parent)
        self.setObjectName(self.OBJECT_NAMES.get(tip, "RozetNotr"))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(22)


class HucreSarmalayici(QWidget):
    """Tablo hücresi içine widget yerleştirmek için ortalanmış sarmalayıcı."""

    def __init__(self, icerik: QWidget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(0)
        layout.addWidget(icerik, 0, Qt.AlignVCenter)


class ButonGrubu(QWidget):
    """Tablo hücresinde birden fazla buton."""

    def __init__(self, butonlar: list, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)
        for b in butonlar:
            layout.addWidget(b)
        layout.addStretch()


class Ayirici(QFrame):
    """1px ayırıcı."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Ayirici")
