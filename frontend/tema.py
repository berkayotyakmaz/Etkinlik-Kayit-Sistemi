"""
EventHub Premium Dark Theme — Aurora gradient, neon accents.
"""

RENKLER = {
    # Çok katmanlı arka plan
    "bg_root": "#06060a",
    "bg_pane": "#0a0a12",
    "bg_card": "#11111c",
    "bg_card_elevated": "#171723",
    "bg_input": "#0c0c14",
    "bg_hover": "#1c1c2c",

    # Sınırlar
    "border": "#1f1f2e",
    "border_strong": "#2c2c44",
    "border_glow": "#3d2c5c",

    # Metin
    "text": "#f8f8fc",
    "text_strong": "#ffffff",
    "text_muted": "#8d8da3",
    "text_subtle": "#5a5a72",
    "text_dim": "#3a3a4d",

    # Aurora vurgu
    "accent": "#b265ff",
    "accent_2": "#ec4899",
    "accent_3": "#7c3aed",
    "accent_pale": "#c4b5fd",

    # Durum
    "success": "#10d9a0",
    "success_dim": "#0a8c68",
    "warning": "#fbbf24",
    "warning_dim": "#b8860b",
    "danger": "#f43f5e",
    "danger_dim": "#9f1239",
    "info": "#38bdf8",

    # Tablo
    "table_header": "#0d0d18",
    "table_row_hover": "#161624",
}


# Önemli renkler için kısayollar (gradient'lerde kullanılır)
ACC = RENKLER["accent"]
ACC2 = RENKLER["accent_2"]
ACC3 = RENKLER["accent_3"]


ANA_STIL = f"""
/* GENEL ============================================================ */
QWidget {{
    background-color: {RENKLER['bg_pane']};
    color: {RENKLER['text']};
    font-family: "Inter", "Segoe UI", "SF Pro Display", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {RENKLER['bg_root']};
}}

QToolTip {{
    background-color: {RENKLER['bg_card_elevated']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border_strong']};
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
}}

/* SIDEBAR ========================================================== */
#Sidebar {{
    background-color: {RENKLER['bg_root']};
    border-right: 1px solid {RENKLER['border']};
}}

#SidebarBaslik {{
    color: {RENKLER['text_strong']};
    font-size: 18px;
    font-weight: 800;
    background: transparent;
    border: none;
    letter-spacing: -0.4px;
}}

#SidebarAltBaslik {{
    color: {RENKLER['text_subtle']};
    font-size: 9px;
    background: transparent;
    border: none;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
}}

#MenuBaslik {{
    color: {RENKLER['text_dim']};
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    background: transparent;
    border: none;
}}

QPushButton#MenuButon {{
    background-color: transparent;
    color: {RENKLER['text_muted']};
    text-align: left;
    padding-left: 22px;
    padding-right: 22px;
    border: none;
    border-radius: 0;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#MenuButon:hover {{
    background-color: {RENKLER['bg_card']};
    color: {RENKLER['text']};
}}

QPushButton#MenuButon:checked {{
    background-color: {RENKLER['bg_card']};
    color: {RENKLER['text_strong']};
    font-weight: 700;
    border-left: 3px solid {ACC};
}}

#KullaniciKart {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 12px;
}}

#KullaniciKart QLabel {{
    background: transparent;
    border: none;
}}

#KullaniciAd {{
    color: {RENKLER['text']};
    font-weight: 700;
    font-size: 12px;
}}

#KullaniciDurum {{
    color: {RENKLER['text_subtle']};
    font-size: 10px;
    font-weight: 500;
}}

#PlanRozet {{
    background-color: rgba(178, 101, 255, 0.15);
    color: {ACC};
    border: 1px solid rgba(178, 101, 255, 0.3);
    border-radius: 5px;
    padding: 2px 7px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.8px;
}}

/* SAYFA BAŞLIKLARI ================================================ */
#SayfaBaslik {{
    color: {RENKLER['text_strong']};
    font-size: 28px;
    font-weight: 800;
    background: transparent;
    border: none;
    letter-spacing: -0.6px;
}}

#SayfaAltBaslik {{
    color: {RENKLER['text_muted']};
    font-size: 13px;
    background: transparent;
    border: none;
    font-weight: 400;
}}

/* HERO PANEL (Dashboard) ========================================== */
#HeroPanel {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border_strong']};
    border-radius: 18px;
}}

#HeroBaslik {{
    color: {RENKLER['text_strong']};
    font-size: 30px;
    font-weight: 800;
    background: transparent;
    border: none;
    letter-spacing: -0.7px;
}}

#HeroAltBaslik {{
    color: {RENKLER['text_muted']};
    font-size: 13px;
    background: transparent;
    border: none;
    font-weight: 400;
}}

#HeroVurgu {{
    color: {ACC};
    font-weight: 800;
    background: transparent;
    border: none;
}}

/* KARTLAR ========================================================= */
#Kart {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 16px;
}}

#Kart QLabel {{
    background: transparent;
    border: none;
}}

#KartBaslik {{
    color: {RENKLER['text_strong']};
    font-size: 16px;
    font-weight: 700;
    background: transparent;
    border: none;
    letter-spacing: -0.3px;
}}

#KartAltBaslik {{
    color: {RENKLER['text_muted']};
    font-size: 12px;
    background: transparent;
    border: none;
}}

/* BUTONLAR (varsayılan) =========================================== */
QPushButton {{
    background-color: {RENKLER['bg_hover']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border_strong']};
    padding-left: 16px;
    padding-right: 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: {RENKLER['border_strong']};
    border: 1px solid {RENKLER['border_glow']};
}}

QPushButton:disabled {{
    background-color: {RENKLER['bg_card']};
    color: {RENKLER['text_dim']};
    border: 1px solid {RENKLER['border']};
}}

QPushButton#IkincilButon {{
    background-color: {RENKLER['bg_card_elevated']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border_strong']};
}}

QPushButton#IkincilButon:hover {{
    background-color: {RENKLER['bg_hover']};
    border: 1px solid {ACC};
}}

QPushButton#HayaletButon {{
    background-color: transparent;
    color: {RENKLER['text_muted']};
    border: 1px solid {RENKLER['border']};
}}

QPushButton#HayaletButon:hover {{
    background-color: {RENKLER['bg_card']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border_strong']};
}}

QPushButton#TehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid rgba(244, 63, 94, 0.3);
}}

QPushButton#TehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: white;
    border: 1px solid {RENKLER['danger']};
}}

QPushButton#KucukIkincilButon {{
    background-color: {RENKLER['bg_card_elevated']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border_strong']};
    padding-left: 10px;
    padding-right: 10px;
    font-size: 12px;
    font-weight: 600;
}}

QPushButton#KucukIkincilButon:hover {{
    background-color: {RENKLER['bg_hover']};
    border: 1px solid {ACC};
}}

QPushButton#KucukTehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid rgba(244, 63, 94, 0.25);
    padding-left: 10px;
    padding-right: 10px;
    font-size: 12px;
    font-weight: 600;
}}

QPushButton#KucukTehlikeButon:hover {{
    background-color: rgba(244, 63, 94, 0.15);
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['danger']};
}}

/* FORM ALANLARI =================================================== */
QLineEdit, QSpinBox, QDateTimeEdit, QComboBox, QTextEdit {{
    background-color: {RENKLER['bg_input']};
    border: 1px solid {RENKLER['border']};
    border-radius: 9px;
    padding-left: 14px;
    padding-right: 14px;
    color: {RENKLER['text']};
    selection-background-color: {ACC};
    font-size: 13px;
}}

QLineEdit:focus, QSpinBox:focus, QDateTimeEdit:focus,
QComboBox:focus, QTextEdit:focus {{
    border: 1px solid {ACC};
    background-color: {RENKLER['bg_card']};
}}

QLineEdit:hover, QSpinBox:hover, QDateTimeEdit:hover,
QComboBox:hover, QTextEdit:hover {{
    border: 1px solid {RENKLER['border_strong']};
}}

#AramaInput {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    padding-left: 16px;
    padding-right: 16px;
    border-radius: 11px;
    font-size: 13px;
    font-weight: 500;
}}

#AramaInput:focus {{
    border: 1px solid {ACC};
    background-color: {RENKLER['bg_card_elevated']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDateTimeEdit::up-button, QDateTimeEdit::down-button {{
    background-color: transparent;
    border: none;
    width: 18px;
}}

QSpinBox::up-arrow, QDateTimeEdit::up-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid {RENKLER['text_muted']};
    width: 0;
    height: 0;
}}

QSpinBox::down-arrow, QDateTimeEdit::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_muted']};
    width: 0;
    height: 0;
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_muted']};
    margin-right: 12px;
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {RENKLER['bg_card_elevated']};
    border: 1px solid {RENKLER['border_strong']};
    border-radius: 9px;
    selection-background-color: {ACC};
    color: {RENKLER['text']};
    padding: 6px;
    outline: 0;
}}

QComboBox QAbstractItemView::item {{
    padding: 9px 11px;
    border-radius: 5px;
    min-height: 22px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {RENKLER['bg_hover']};
}}

QLabel#FormEtiket {{
    color: {RENKLER['text_muted']};
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    background: transparent;
    border: none;
}}

QCalendarWidget QWidget {{
    alternate-background-color: {RENKLER['bg_card_elevated']};
    background-color: {RENKLER['bg_card_elevated']};
    color: {RENKLER['text']};
}}

QCalendarWidget QToolButton {{
    color: {RENKLER['text']};
    background-color: transparent;
    padding: 6px;
    border-radius: 4px;
}}

QCalendarWidget QToolButton:hover {{
    background-color: {RENKLER['bg_hover']};
}}

QCalendarWidget QAbstractItemView:enabled {{
    color: {RENKLER['text']};
    background-color: {RENKLER['bg_card_elevated']};
    selection-background-color: {ACC};
    selection-color: white;
}}

QCalendarWidget QAbstractItemView:disabled {{
    color: {RENKLER['text_dim']};
}}

/* TABLOLAR ======================================================== */
QTableWidget {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 14px;
    gridline-color: transparent;
    color: {RENKLER['text']};
    selection-background-color: transparent;
    outline: 0;
}}

QTableWidget::item {{
    padding-left: 8px;
    padding-right: 8px;
    border: none;
    border-bottom: 1px solid {RENKLER['border']};
    background-color: transparent;
}}

QTableWidget::item:selected {{
    background-color: {RENKLER['bg_hover']};
    color: {RENKLER['text']};
}}

QTableWidget::item:hover {{
    background-color: {RENKLER['table_row_hover']};
}}

QHeaderView::section {{
    background-color: {RENKLER['table_header']};
    color: {RENKLER['text_subtle']};
    padding-top: 14px;
    padding-bottom: 14px;
    padding-left: 14px;
    padding-right: 14px;
    border: none;
    border-bottom: 1px solid {RENKLER['border']};
    font-weight: 800;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

QHeaderView::section:first {{
    border-top-left-radius: 14px;
}}

QHeaderView::section:last {{
    border-top-right-radius: 14px;
}}

QTableCornerButton::section {{
    background-color: {RENKLER['table_header']};
    border: none;
    border-top-left-radius: 14px;
}}

/* SCROLLBAR ======================================================= */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    border: none;
    margin: 4px 2px 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {RENKLER['border_strong']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ACC};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    border: none;
    margin: 2px 4px 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {RENKLER['border_strong']};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {ACC};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* DİYALOG ========================================================= */
QDialog {{
    background-color: {RENKLER['bg_pane']};
}}

QMessageBox {{
    background-color: {RENKLER['bg_card_elevated']};
}}

QMessageBox QLabel {{
    color: {RENKLER['text']};
    font-size: 13px;
    background: transparent;
    border: none;
}}

QMessageBox QPushButton {{
    min-width: 90px;
}}

/* ROZETLER ======================================================== */
QLabel#RozetBasari {{
    background-color: rgba(16, 217, 160, 0.12);
    color: {RENKLER['success']};
    border: 1px solid rgba(16, 217, 160, 0.35);
    border-radius: 11px;
    padding-left: 12px;
    padding-right: 12px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10px;
    font-weight: 800;
    min-width: 60px;
    max-height: 22px;
    letter-spacing: 1.2px;
}}

QLabel#RozetUyari {{
    background-color: rgba(251, 191, 36, 0.12);
    color: {RENKLER['warning']};
    border: 1px solid rgba(251, 191, 36, 0.35);
    border-radius: 11px;
    padding-left: 12px;
    padding-right: 12px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10px;
    font-weight: 800;
    min-width: 60px;
    max-height: 22px;
    letter-spacing: 1.2px;
}}

QLabel#RozetTehlike {{
    background-color: rgba(244, 63, 94, 0.12);
    color: {RENKLER['danger']};
    border: 1px solid rgba(244, 63, 94, 0.35);
    border-radius: 11px;
    padding-left: 12px;
    padding-right: 12px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10px;
    font-weight: 800;
    min-width: 60px;
    max-height: 22px;
    letter-spacing: 1.2px;
}}

QLabel#RozetNotr {{
    background-color: {RENKLER['bg_hover']};
    color: {RENKLER['text_muted']};
    border: 1px solid {RENKLER['border_strong']};
    border-radius: 11px;
    padding-left: 12px;
    padding-right: 12px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10px;
    font-weight: 800;
    min-width: 60px;
    max-height: 22px;
    letter-spacing: 1.2px;
}}

/* DİĞER =========================================================== */
QFrame#Ayirici {{
    background-color: {RENKLER['border']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}

QFrame#DikeyAyirici {{
    background-color: {RENKLER['border']};
    max-width: 1px;
    min-width: 1px;
    border: none;
}}
"""
