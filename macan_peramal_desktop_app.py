#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Project: Macan Peramal
Slogan: "Menjelajahi Jejak Takdir dalam Kearifan Nusantara"
Copyright: © 2026 Macan Angkasa
Description: A modern Indonesian mystical, cultural wisdom, and Primbon
             exploration application crafted using Python and PySide6.
================================================================================
"""

import sys
import os
import json
import random
import datetime
from typing import Dict, List, Tuple, Any, Optional

# Import PySide6 Core, Gui, and Widgets modules
from PySide6.QtCore import (
    Qt, QSize, QTimer, QPoint, QRectF, QPropertyAnimation, 
    QEasingCurve, Signal, Slot, QObject, QDate
)
from PySide6.QtGui import (
    QPainter, QColor, QRadialGradient, QLinearGradient, QFont, 
    QPen, QBrush, QPixmap, QIcon, QPainterPath, QPolygonF,
    QTextDocument, QFontDatabase, QAction
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QLineEdit, QComboBox, 
    QDateEdit, QTextBrowser, QTableWidget, QTableWidgetItem, 
    QHeaderView, QFileDialog, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QGridLayout, QProgressBar, QMessageBox
)

# ==============================================================================
# GLOBAL LOCALIZATION & TRANSLATIONS DATABASE
# ==============================================================================
TRANSLATIONS = {
    "id": {
        "app_title": "Macan Peramal",
        "app_slogan": "Menjelajahi Jejak Takdir dalam Kearifan Nusantara",
        "copyright": "© 2026 Macan Angkasa. Hak Cipta Dilindungi.",
        "dashboard": "Beranda",
        "name_analysis": "Analisa Nama",
        "birth_analysis": "Analisa Kelahiran",
        "compatibility": "Kecocokan Pasangan",
        "numerology": "Pusat Numerologi",
        "dream_interpreter": "Tafsir Mimpi",
        "primbon_encyclopedia": "Ensiklopedia Primbon",
        "calendar": "Kalender Spiritual",
        "daily_fortune": "Ramalan Harian",
        "lucky_day": "Hari Keberuntungan",
        "settings": "Pengaturan",
        "quick_tools": "Pintasan Ramalan",
        "energy_meter": "Meteran Energi Spiritual",
        "crystal_orb_desc": "Ketuk bola kristal mistis untuk menyerap energi hari ini...",
        "calculate": "Hitung Ramalan",
        "reset": "Mulai Ulang",
        "name_input_placeholder": "Masukkan nama lengkap Anda...",
        "birth_date": "Tanggal Lahir",
        "analyze_btn": "Analisa Jejak Takdir",
        "save_history": "Simpan Riwayat",
        "export_pdf": "Ekspor Laporan (HTML)",
        "language_select": "Pilih Bahasa",
        "theme_select": "Tema Estetika",
        "active_lang": "Bahasa Aktif",
        "history_saved": "Riwayat berhasil disimpan secara mistis!",
        "history_cleared": "Seluruh riwayat ramalan telah disucikan.",
        "search": "Cari...",
        "category": "Kategori",
        "couple": "Pasangan",
        "friendship": "Persahabatan",
        "business": "Rekan Bisnis",
        "analyze_compat": "Analisa Kecocokan",
        "compatibility_score": "Skor Kompatibilitas",
        "weton_calc": "Perhitungan Weton Jawa",
        "destiny_num": "Angka Takdir",
        "life_path_num": "Angka Jalan Hidup",
        "soul_urge_num": "Angka Hasrat Jiwa",
        "personality_num": "Angka Kepribadian",
        "weton_neptu": "Jumlah Neptu",
        "spiritual_element": "Elemen Spiritual",
        "career_rec": "Rekomendasi Karier",
        "character_traits": "Sifat & Karakter",
        "fortune_desc": "Prediksi Rezeki",
        "search_dream": "Masukkan kata kunci mimpi Anda...",
        "dream_not_found": "Mimpi Anda belum tercatat di kitab primbon kami. Hubungi tetua adat.",
        "daily_msg": "Pesan Mistis Hari Ini",
        "weekly_msg": "Ramalan Pekan Ini",
        "monthly_msg": "Arah Rezeki Bulan Ini",
        "choose_activity": "Pilih Rencana Kegiatan",
        "find_lucky_days": "Cari Hari Baik",
        "lucky_days_result": "Hari Baik yang Direkomendasikan",
        "clear_history": "Sapu Bersih Riwayat",
        "export_success": "Laporan mistis Anda berhasil diekspor ke: ",
    },
    "en": {
        "app_title": "Macan Peramal",
        "app_slogan": "Exploring Destiny through Archipelago Wisdom",
        "copyright": "© 2026 Macan Angkasa. All Rights Reserved.",
        "dashboard": "Dashboard",
        "name_analysis": "Name Analysis",
        "birth_analysis": "Birth Analysis",
        "compatibility": "Compatibility",
        "numerology": "Numerology Center",
        "dream_interpreter": "Dream Oracle",
        "primbon_encyclopedia": "Primbon Encyclopedia",
        "calendar": "Spiritual Calendar",
        "daily_fortune": "Daily Fortune",
        "lucky_day": "Lucky Day Finder",
        "settings": "Settings",
        "quick_tools": "Quick Fortune Shortcuts",
        "energy_meter": "Spiritual Energy Meter",
        "crystal_orb_desc": "Tap the mystical crystal orb to absorb today's cosmic energy...",
        "calculate": "Analyze Destiny",
        "reset": "Reset",
        "name_input_placeholder": "Enter your full name...",
        "birth_date": "Birth Date",
        "analyze_btn": "Analyze Footprints of Destiny",
        "save_history": "Save History",
        "export_pdf": "Export Report (HTML)",
        "language_select": "Choose Language",
        "theme_select": "Aesthetic Theme",
        "active_lang": "Active Language",
        "history_saved": "History has been mystically saved!",
        "history_cleared": "All forecast history has been purified.",
        "search": "Search...",
        "category": "Category",
        "couple": "Romantic Partner",
        "friendship": "Friendship",
        "business": "Business Partner",
        "analyze_compat": "Analyze Harmony",
        "compatibility_score": "Compatibility Score",
        "weton_calc": "Javanese Weton Calculation",
        "destiny_num": "Destiny Number",
        "life_path_num": "Life Path Number",
        "soul_urge_num": "Soul Urge Number",
        "personality_num": "Personality Number",
        "weton_neptu": "Neptu Total",
        "spiritual_element": "Spiritual Element",
        "career_rec": "Career Recommendation",
        "character_traits": "Character & Personality",
        "fortune_desc": "Fortune Prediction",
        "search_dream": "Enter keyword of your dream...",
        "dream_not_found": "Your dream is not yet written in our cosmic archive.",
        "daily_msg": "Mystic Insight of the Day",
        "weekly_msg": "Weekly Outlook",
        "monthly_msg": "Monthly Fortune Flow",
        "choose_activity": "Choose Planned Activity",
        "find_lucky_days": "Find Auspicious Days",
        "lucky_days_result": "Recommended Favorable Days",
        "clear_history": "Purge History Data",
        "export_success": "Your mystic report has been successfully exported to: ",
    }
}

# ==============================================================================
# GLOBAL STYLING (QSS)
# ==============================================================================
MYSTIC_THEME_QSS = """
QMainWindow {
    background-color: #0B0816;
}

QWidget {
    color: #E2E1E6;
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
    font-size: 13px;
}

QFrame#SidebarFrame {
    background-color: #110B24;
    border-right: 1px solid #2B1B4D;
}

QFrame#TitleBarFrame {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #110B24, stop:1 #0B0816);
    border-bottom: 1px solid #251842;
}

QFrame#ContentFrame {
    background-color: #07040F;
}

/* Card design mimicking ancient manuscripts & glowing high tech magic */
QFrame.MysticCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #140F2D, stop:1 #0D0A20);
    border: 1px solid #351C5E;
    border-radius: 12px;
}

QFrame.MysticCard:hover {
    border: 1px solid #6A329F;
}

/* Mystic Title */
QLabel#AppNameLabel {
    color: #FFD700;
    font-size: 19px;
    font-weight: bold;
    letter-spacing: 2px;
}

QLabel#AppSloganLabel {
    color: #8C84A9;
    font-size: 10px;
    font-style: italic;
}

/* ScrollBar Styling */
QScrollBar:vertical {
    border: none;
    background: #0B0816;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #4E2C7E;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #8E44AD;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Styled text widgets */
QLineEdit {
    background-color: #1A1235;
    border: 1px solid #432A70;
    border-radius: 6px;
    padding: 8px;
    color: #FFFFFF;
    selection-background-color: #8E44AD;
}
QLineEdit:focus {
    border: 1px solid #A259FF;
}

QComboBox {
    background-color: #1A1235;
    border: 1px solid #432A70;
    border-radius: 6px;
    padding: 6px 12px;
    color: #FFFFFF;
    min-width: 120px;
}
QComboBox:focus {
    border: 1px solid #A259FF;
}
QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
}

QDateEdit {
    background-color: #1A1235;
    border: 1px solid #432A70;
    border-radius: 6px;
    padding: 6px;
    color: #FFFFFF;
}

QTextBrowser {
    background-color: #0E0921;
    border: 1px solid #2B1B4D;
    border-radius: 8px;
    padding: 12px;
    color: #D2CFDF;
    line-height: 1.6;
}

/* Buttons */
QPushButton.MysticButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6C33A3, stop:1 #491E74);
    border: 1px solid #8B4AD4;
    border-radius: 6px;
    color: #F8F7FF;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton.MysticButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8442C4, stop:1 #5B278D);
    border: 1px solid #FFD700;
}
QPushButton.MysticButton:pressed {
    background: #391559;
}

QPushButton.GoldButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D4AF37, stop:1 #996515);
    border: 1px solid #FFD700;
    border-radius: 6px;
    color: #0F0921;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton.GoldButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFE494, stop:1 #B27B1E);
}

QPushButton.DestructiveButton {
    background-color: #4D1A25;
    border: 1px solid #992D41;
    border-radius: 6px;
    color: #FFA5A5;
    padding: 8px 16px;
}
QPushButton.DestructiveButton:hover {
    background-color: #731F32;
    border-color: #FF708C;
}

/* Navigation Buttons */
QPushButton.NavButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: #A39BBD;
    text-align: left;
    padding: 10px 15px;
    font-weight: 500;
    font-size: 13px;
}
QPushButton.NavButton:hover {
    background-color: rgba(138, 43, 226, 0.15);
    color: #FFFFFF;
}
QPushButton.NavButton:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(142, 68, 173, 0.35), stop:1 rgba(11, 8, 22, 0.1));
    border-left: 3px solid #FFD700;
    color: #FFD700;
}

/* Header Text */
QLabel.MysticSectionTitle {
    color: #FFD700;
    font-size: 20px;
    font-weight: bold;
    letter-spacing: 1px;
}

QLabel.MysticSubTitle {
    color: #B19FFC;
    font-size: 13px;
}

/* Custom Table Widget */
QTableWidget {
    background-color: #120C29;
    border: 1px solid #2E1B51;
    border-radius: 8px;
    gridline-color: #241442;
    color: #E2E1E6;
}
QTableWidget::item {
    padding: 10px;
}
QTableWidget::item:selected {
    background-color: #4E2280;
}
QHeaderView::section {
    background-color: #1A1238;
    color: #FFD700;
    padding: 8px;
    border: 1px solid #2E1B51;
    font-weight: bold;
}
"""

# ==============================================================================
# LOCALIZED TRANSLATION MANAGER (SINGLETON)
# ==============================================================================
class LanguageManager(QObject):
    language_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._current_lang = "id"  # Default Indonesian
        
    @property
    def current_language(self) -> str:
        return self._current_lang
        
    def set_language(self, lang: str):
        if lang in ["id", "en"] and lang != self._current_lang:
            self._current_lang = lang
            self.language_changed.emit(lang)
            
    def get(self, key: str) -> str:
        return TRANSLATIONS[self._current_lang].get(key, key)

lang_mgr = LanguageManager()

# ==============================================================================
# PHYSICS-BASED FLOATING PARTICLE BACKGROUND
# ==============================================================================
class MysticParticleWidget(QWidget):
    """
    Simulates floating cosmic energy and stardust particles as an
    atmospheric dark background overlay.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(33)  # Roughly 30 FPS
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.init_particles()
        
    def init_particles(self):
        self.particles = []
        num_particles = min(50, max(15, int(self.width() * self.height() / 15000)))
        for _ in range(num_particles):
            self.particles.append({
                "x": random.uniform(0, self.width()),
                "y": random.uniform(0, self.height()),
                "size": random.uniform(1.0, 3.5),
                "speed_y": random.uniform(-0.8, -0.2),
                "speed_x": random.uniform(-0.3, 0.3),
                "color": random.choice([
                    QColor(138, 43, 226, random.randint(60, 160)),  # Mystic Violet
                    QColor(0, 191, 255, random.randint(50, 140)),   # Deep Celestial Sky Blue
                    QColor(255, 215, 0, random.randint(40, 110))    # Celestial Gold Dust
                ]),
                "pulse": random.uniform(0.0, 2 * 3.1415),
                "pulse_speed": random.uniform(0.02, 0.08)
            })
            
    def update_particles(self):
        for p in self.particles:
            p["y"] += p["speed_y"]
            p["x"] += p["speed_x"]
            p["pulse"] += p["pulse_speed"]
            
            # Reset particle when it floats off the top boundary
            if p["y"] < -10:
                p["y"] = self.height() + 10
                p["x"] = random.uniform(0, self.width())
            if p["x"] < -10:
                p["x"] = self.width() + 10
            elif p["x"] > self.width() + 10:
                p["x"] = -10
                
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Transparent background allowing standard widgets underneath to render
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
        
        for p in self.particles:
            # Pulsing alpha intensity
            alpha_scale = (abs(random.uniform(-0.1, 0.1)) + 0.5) + 0.5 * (1.0 + (p["pulse"] % 3.1415))
            alpha_val = max(10, min(255, int(p["color"].alpha() * alpha_scale)))
            
            color = QColor(p["color"].red(), p["color"].green(), p["color"].blue(), alpha_val)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            
            # Draw particle
            painter.drawEllipse(QRectF(p["x"], p["y"], p["size"], p["size"]))


# ==============================================================================
# ANIMATED GLOWING CRYSTAL ORB WIDGET
# ==============================================================================
class MysticCrystalOrb(QWidget):
    """
    An interactive custom-drawn widget showing a gorgeous rotating, pulsing,
    and glowing mystical crystal orb. Responds to clicks with energy ripples.
    """
    orb_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 220)
        self.angle = 0.0
        self.pulse = 0.0
        self.ripple_radius = 0.0
        self.ripple_active = False
        
        # Animations
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_step)
        self.timer.start(20) # Smooth 50 FPS
        
    def animate_step(self):
        self.angle += 0.8
        if self.angle >= 360.0:
            self.angle = 0.0
            
        self.pulse += 0.04
        if self.pulse >= 2 * 3.1415:
            self.pulse = 0.0
            
        if self.ripple_active:
            self.ripple_radius += 4.5
            if self.ripple_radius > 120.0:
                self.ripple_active = False
                self.ripple_radius = 0.0
                
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.ripple_active = True
            self.ripple_radius = 20.0
            self.orb_clicked.emit()
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2.0
        center_y = height / 2.0
        radius = min(width, height) / 3.0
        
        # Pulsing scale helper
        pulse_scale = 1.0 + 0.04 * (1.0 + (self.pulse % 3.1415))
        current_radius = radius * pulse_scale
        
        # 1. Ripple Effect (Expanding shockwave)
        if self.ripple_active:
            ripple_pen = QPen(QColor(255, 215, 0, int(255 * (1.0 - (self.ripple_radius / 120.0)))), 2.5)
            painter.setPen(ripple_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPoint(center_x, center_y), self.ripple_radius + current_radius, self.ripple_radius + current_radius)
            
        # 2. Outer Celestial Glowing Ring
        painter.setPen(Qt.NoPen)
        outer_gradient = QRadialGradient(center_x, center_y, current_radius * 1.5)
        outer_gradient.setColorAt(0.0, QColor(138, 43, 226, 40))
        outer_gradient.setColorAt(0.6, QColor(0, 191, 255, 15))
        outer_gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(outer_gradient))
        painter.drawEllipse(QPoint(center_x, center_y), current_radius * 1.5, current_radius * 1.5)
        
        # 3. Rotating Constellation Dots & Lines (Astrological Ring)
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle)
        
        gold_pen = QPen(QColor(218, 165, 32, 120), 1, Qt.DashLine)
        painter.setPen(gold_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QRectF(-current_radius * 1.2, -current_radius * 1.2, current_radius * 2.4, current_radius * 2.4))
        
        # Small orbiting planetary runes / circles
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 215, 0, 200)))
        painter.drawEllipse(QRectF(-current_radius * 1.2 - 4, -4, 8, 8))
        painter.drawEllipse(QRectF(current_radius * 1.2 - 4, -4, 8, 8))
        
        painter.setBrush(QBrush(QColor(138, 43, 226, 220)))
        painter.drawEllipse(QRectF(-4, -current_radius * 1.2 - 4, 8, 8))
        painter.drawEllipse(QRectF(-4, current_radius * 1.2 - 4, 8, 8))
        painter.restore()
        
        # 4. Main Crystal Orb Body
        orb_gradient = QRadialGradient(center_x - current_radius * 0.25, center_y - current_radius * 0.25, current_radius)
        orb_gradient.setColorAt(0.0, QColor(255, 255, 255, 250))      # Hot white core
        orb_gradient.setColorAt(0.15, QColor(230, 200, 255, 220))   # Soft violet glow
        orb_gradient.setColorAt(0.4, QColor(138, 43, 226, 170))     # Cosmic Purple
        orb_gradient.setColorAt(0.75, QColor(30, 9, 81, 230))       # Dark Violet Deep
        orb_gradient.setColorAt(1.0, QColor(10, 4, 30, 255))        # Edge shadow
        
        painter.setBrush(QBrush(orb_gradient))
        painter.setPen(QPen(QColor(218, 165, 32, 150), 1.5))        # Subtle Gold Outline
        painter.drawEllipse(QPoint(center_x, center_y), current_radius, current_radius)
        
        # 5. Inner Magic Rune / Core Spark
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(-self.angle * 0.5)
        painter.setPen(Qt.NoPen)
        # Translucent overlay reflecting the ancient "Javanese Sun" or "Mala"
        painter.setBrush(QBrush(QColor(255, 255, 255, 45)))
        for i in range(4):
            painter.rotate(45)
            painter.drawRect(QRectF(-current_radius*0.4, -current_radius*0.05, current_radius*0.8, current_radius*0.1))
        painter.restore()
        
        # 6. Upper Surface Specular Reflection Highlight (Glass Effect)
        specular_gradient = QLinearGradient(0, center_y - current_radius, 0, center_y)
        specular_gradient.setColorAt(0.0, QColor(255, 255, 255, 180))
        specular_gradient.setColorAt(0.8, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(specular_gradient))
        painter.setPen(Qt.NoPen)
        
        spec_rect = QRectF(center_x - current_radius * 0.7, 
                           center_y - current_radius * 0.9, 
                           current_radius * 1.4, 
                           current_radius * 0.8)
        painter.drawEllipse(spec_rect)


# ==============================================================================
# CALCULATION ENGINES (WETON, NUMEROLOGY, AUSPICIOUS DAYS)
# ==============================================================================
class DestinyEngine:
    @staticmethod
    def calculate_weton(birth_date: datetime.date) -> Dict[str, Any]:
        """
        Calculates Javanese Weton (combination of Day and 5-day Pasaran)
        based on exact reference starting from 17 August 1945 (Friday Kliwon).
        """
        # Base Reference: Friday Kliwon
        ref_date = datetime.date(1945, 8, 17)
        delta_days = (birth_date - ref_date).days
        
        # 7-day Cycle index
        # 17 Aug 1945 was Friday. Let's align 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
        day_names_id = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        day_names_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        day_idx = (4 + delta_days) % 7
        
        # 5-day Cycle index
        # 17 Aug 1945 was Kliwon. Align: 0=Legi, 1=Pahing, 2=Pon, 3=Wage, 4=Kliwon
        pasaran_names_id = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
        pasaran_idx = (4 + delta_days) % 5
        
        # Neptu calculation value mappings
        neptu_day = {"Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9, "Minggu": 5}
        neptu_pasaran = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
        
        day_id = day_names_id[day_idx]
        day_en = day_names_en[day_idx]
        pasaran = pasaran_names_id[pasaran_idx]
        
        n_day = neptu_day[day_id]
        n_pas = neptu_pasaran[pasaran]
        neptu_total = n_day + n_pas
        
        # Assign Spiritual Element & General Characteristic depending on Neptu
        if neptu_total in [7, 8, 9]:
            elem_id, elem_en = "Bumi / Tanah", "Earth / Ground"
            trait_id = "Memiliki sifat 'Bumi': Kokoh, penyabar, pendiam, namun keras kepala jika terusik."
            trait_en = "Possesses 'Earth' qualities: Solid, highly patient, quiet, yet stubborn when triggered."
            career_id = "Pertanian, Konstruksi, Properti, Pengrajin Seni."
            career_en = "Agriculture, Construction, Real Estate, Craftsmanship."
        elif neptu_total in [10, 11, 12]:
            elem_id, elem_en = "Angin / Udara", "Wind / Air"
            trait_id = "Memiliki sifat 'Angin': Komunikatif, dinamis, pandai bergaul, namun mudah bimbang."
            trait_en = "Possesses 'Wind' qualities: Highly communicative, dynamic, friendly, but easily swayed."
            career_id = "Pemasaran, Hubungan Masyarakat, Media, Perjalanan/Wisata."
            career_en = "Marketing, Public Relations, Journalism, Travel/Tourism."
        elif neptu_total in [13, 14, 15]:
            elem_id, elem_en = "Api", "Fire"
            trait_id = "Memiliki sifat 'Api': Berjiwa pemimpin, mandiri, ambisius, setia kawan, emosional."
            trait_en = "Possesses 'Fire' qualities: Natural leader, independent, ambitious, loyal, highly passionate."
            career_id = "Politik, Militer, Wirausaha, Hukum."
            career_en = "Politics, Military, Entrepreneurship, Law."
        else: # 16, 17, 18
            elem_id, elem_en = "Samudra / Air", "Water / Ocean"
            trait_id = "Memiliki sifat 'Samudra': Spiritualitas tinggi, bijaksana, berwibawa besar, pendengar ulung."
            trait_en = "Possesses 'Ocean' qualities: High spiritual affinity, wise, deeply authoritative, excellent listener."
            career_id = "Konselor spiritual, Filsuf, Peneliti, Edukasi Akademis."
            career_en = "Spiritual Guide, Philosopher, Researcher, Academic Education."
            
        return {
            "day_id": day_id,
            "day_en": day_en,
            "pasaran": pasaran,
            "neptu_day": n_day,
            "neptu_pasaran": n_pas,
            "neptu_total": neptu_total,
            "element_id": elem_id,
            "element_en": elem_en,
            "traits_id": trait_id,
            "traits_en": trait_en,
            "career_id": career_id,
            "career_en": career_en
        }

    @staticmethod
    def calculate_numerology(name: str, birth_date: datetime.date) -> Dict[str, Any]:
        """
        Calculates Pythagorean Numerology: Life Path, Destiny, Soul Urge, and Personality.
        """
        # Life Path Number
        day_str = str(birth_date.day)
        month_str = str(birth_date.month)
        year_str = str(birth_date.year)
        
        def reduce_number(num_str: str, master_check: bool = True) -> int:
            while len(num_str) > 1:
                val = sum(int(digit) for digit in num_str if digit.isdigit())
                if master_check and val in [11, 22, 33]:
                    return val
                num_str = str(val)
            return int(num_str) if num_str else 1
            
        total_date_str = day_str + month_str + year_str
        life_path = reduce_number(total_date_str)
        
        # Pythagorean Name Letter Mappings
        pythag_map = {
            'A':1, 'J':1, 'S':1,
            'B':2, 'K':2, 'T':2,
            'C':3, 'L':3, 'U':3,
            'D':4, 'M':4, 'V':4,
            'E':5, 'N':5, 'W':5,
            'F':6, 'O':6, 'X':6,
            'G':7, 'P':7, 'Y':7,
            'H':8, 'Q':8, 'Z':8,
            'I':9, 'R':9
        }
        
        cleaned_name = "".join(char.upper() for char in name if char.isalpha())
        
        all_vals = []
        vowel_vals = []
        consonant_vals = []
        
        for char in cleaned_name:
            val = pythag_map.get(char, 0)
            if val > 0:
                all_vals.append(val)
                if char in "AEIOU":
                    vowel_vals.append(val)
                else:
                    consonant_vals.append(val)
                    
        destiny_num = reduce_number(str(sum(all_vals)), master_check=True)
        soul_urge_num = reduce_number(str(sum(vowel_vals)), master_check=True)
        personality_num = reduce_number(str(sum(consonant_vals)), master_check=True)
        
        # Master number fallback to standard reduction if empty name
        if not cleaned_name:
            destiny_num = 1
            soul_urge_num = 1
            personality_num = 1
            
        # Rich per-number descriptions (ID & EN)
        NUM_DESC_ID = {
            1: {
                "title": "Sang Pelopor",
                "desc": "Angka 1 melambangkan kepemimpinan, kemandirian, dan tekad baja. Anda adalah jiwa pelopor yang lahir untuk membuka jalan baru. Karakter: ambisius, percaya diri, inovatif. Hindari sifat dominan yang berlebihan.",
                "lucky_color": "Merah & Emas",
                "lucky_gem": "Rubi",
                "best_day": "Minggu & Senin",
                "challenge": "Belajar mendengar dan berkolaborasi dengan orang lain."
            },
            2: {
                "title": "Sang Diplomat",
                "desc": "Angka 2 melambangkan keharmonisan, kepekaan, dan kerja sama tim. Anda berbakat sebagai mediator dan penyeimbang konflik. Karakter: empatik, sabar, penyayang, artistik. Hindari sifat terlalu bergantung pada pendapat orang.",
                "lucky_color": "Putih & Silver",
                "lucky_gem": "Mutiara",
                "best_day": "Senin & Jumat",
                "challenge": "Membangun kepercayaan diri tanpa bergantung pada validasi eksternal."
            },
            3: {
                "title": "Sang Seniman Kosmik",
                "desc": "Angka 3 memancarkan kreativitas, keceriaan, dan ekspresi diri yang kuat. Anda adalah jiwa kreatif yang mampu menyebarkan kebahagiaan kepada semua orang. Karakter: ekspresif, optimis, berbakat seni dan komunikasi.",
                "lucky_color": "Kuning & Ungu",
                "lucky_gem": "Amethyst",
                "best_day": "Rabu & Sabtu",
                "challenge": "Menjaga fokus dan disiplin agar bakat termanifestasi secara optimal."
            },
            4: {
                "title": "Sang Arsitek Kehidupan",
                "desc": "Angka 4 melambangkan ketekunan, keteraturan, dan pondasi yang kokoh. Anda adalah pembangun sejati yang bekerja dengan metodis dan sistematis. Karakter: disiplin, dapat diandalkan, pekerja keras, praktis.",
                "lucky_color": "Hijau Tua & Coklat Tanah",
                "lucky_gem": "Giok Hijau",
                "best_day": "Kamis & Sabtu",
                "challenge": "Belajar fleksibel dan terbuka terhadap perubahan yang tak terduga."
            },
            5: {
                "title": "Sang Petualang Sejati",
                "desc": "Angka 5 memancarkan kebebasan, petualangan, dan adaptabilitas luar biasa. Anda lahir untuk mengeksplorasi dunia dan memecah batas konvensional. Karakter: dinamis, penuh rasa ingin tahu, fleksibel, karismatik.",
                "lucky_color": "Biru Turquoise & Abu-abu",
                "lucky_gem": "Aquamarine",
                "best_day": "Rabu & Jumat",
                "challenge": "Menjaga komitmen dan menghindari gaya hidup tidak stabil."
            },
            6: {
                "title": "Sang Penjaga Harmoni",
                "desc": "Angka 6 melambangkan tanggung jawab, cinta kasih, dan keharmonisan keluarga. Anda adalah jiwa pengasuh yang selalu hadir untuk orang-orang tercinta. Karakter: peduli, protektif, penuh kasih, berbakat seni dan dekorasi.",
                "lucky_color": "Biru Tua & Rose Gold",
                "lucky_gem": "Safir Biru",
                "best_day": "Jumat & Selasa",
                "challenge": "Belajar melepas perfeksionisme dan menerima ketidaksempurnaan dengan ikhlas."
            },
            7: {
                "title": "Sang Pencari Kebenaran",
                "desc": "Angka 7 memancarkan intelektualisme, spiritualitas, dan pencarian makna terdalam. Anda adalah jiwa mistis yang selalu lapar akan pengetahuan dan kebijaksanaan. Karakter: analitis, intuitif, misterius, mandiri secara spiritual.",
                "lucky_color": "Ungu Gelap & Putih",
                "lucky_gem": "Ametis Gelap",
                "best_day": "Sabtu & Senin",
                "challenge": "Membuka diri untuk hubungan emosional yang lebih dalam dan hangat."
            },
            8: {
                "title": "Sang Pembangun Kekuasaan",
                "desc": "Angka 8 melambangkan ambisi duniawi, kekuatan materi, dan kemampuan eksekusi yang dahsyat. Anda lahir untuk mengelola kekayaan, memimpin organisasi besar, dan meninggalkan warisan abadi. Karakter: tegas, berambisi, berwibawa.",
                "lucky_color": "Hitam & Emas",
                "lucky_gem": "Onyx Hitam",
                "best_day": "Sabtu & Kamis",
                "challenge": "Menyeimbangkan pencapaian materi dengan kepuasan batin dan kasih sayang."
            },
            9: {
                "title": "Sang Filantropis Universal",
                "desc": "Angka 9 adalah angka tertinggi siklus, melambangkan belas kasih universal, kebijaksanaan, dan pengabdian kepada sesama. Anda adalah jiwa yang telah matang dan memiliki misi mulia menerangi dunia. Karakter: altruistik, bijaksana, humanis.",
                "lucky_color": "Merah Tua & Emas Tua",
                "lucky_gem": "Garnet",
                "best_day": "Selasa & Kamis",
                "challenge": "Belajar menetapkan batasan yang sehat agar tidak kelelahan memberikan kepada orang lain."
            },
            11: {
                "title": "Angka Master: Sang Penerang Jiwa",
                "desc": "Angka Master 11 adalah angka pencerah spiritual tertinggi. Anda memiliki intuisi yang melampaui batas manusia biasa, kepekaan luar biasa terhadap energi sekitar, dan potensi menjadi pemimpin spiritual atau seniman visioner kaliber dunia.",
                "lucky_color": "Putih Suci & Silver",
                "lucky_gem": "Berlian Putih",
                "best_day": "Senin & Jumat",
                "challenge": "Mengelola sensitivitas ekstrem agar tidak berubah menjadi kecemasan dan overthinking."
            },
            22: {
                "title": "Angka Master: Sang Arsitek Agung",
                "desc": "Angka Master 22 adalah angka potensi tertinggi — 'The Master Builder'. Anda mampu mewujudkan impian terbesar menjadi kenyataan nyata di dunia fisik. Karakter: visioner, pragmatis, berjiwa besar, mampu memimpin perubahan peradaban.",
                "lucky_color": "Emas Tua & Merah Tua",
                "lucky_gem": "Ruby Merah",
                "best_day": "Kamis & Minggu",
                "challenge": "Menjaga kerendahan hati di tengah potensi pencapaian yang luar biasa."
            },
            33: {
                "title": "Angka Master: Sang Guru Agung",
                "desc": "Angka Master 33 adalah angka paling langka dan paling mulia — 'The Master Teacher'. Anda lahir dengan misi suci menjadi guru, penyembuh, atau pemimpin spiritual yang membawa transformasi mendalam bagi ribuan bahkan jutaan jiwa.",
                "lucky_color": "Emas & Putih Suci",
                "lucky_gem": "Berlian & Safir",
                "best_day": "Jumat & Senin",
                "challenge": "Menemukan keseimbangan antara pengabdian total kepada dunia dan perawatan diri pribadi."
            }
        }

        NUM_DESC_EN = {
            1: {
                "title": "The Pioneer",
                "desc": "Number 1 symbolizes leadership, independence, and iron will. You are a pioneering soul born to forge new paths. Traits: ambitious, confident, innovative. Guard against excessive dominance.",
                "lucky_color": "Red & Gold",
                "lucky_gem": "Ruby",
                "best_day": "Sunday & Monday",
                "challenge": "Learning to listen and collaborate with others."
            },
            2: {
                "title": "The Diplomat",
                "desc": "Number 2 symbolizes harmony, sensitivity, and teamwork. You are gifted as a mediator and conflict balancer. Traits: empathetic, patient, loving, artistic. Guard against excessive dependence on others' opinions.",
                "lucky_color": "White & Silver",
                "lucky_gem": "Pearl",
                "best_day": "Monday & Friday",
                "challenge": "Building self-confidence without relying on external validation."
            },
            3: {
                "title": "The Cosmic Artist",
                "desc": "Number 3 radiates creativity, joy, and strong self-expression. You are a creative soul who spreads happiness. Traits: expressive, optimistic, talented in arts and communication.",
                "lucky_color": "Yellow & Purple",
                "lucky_gem": "Amethyst",
                "best_day": "Wednesday & Saturday",
                "challenge": "Maintaining focus and discipline to fully manifest your talents."
            },
            4: {
                "title": "The Life Architect",
                "desc": "Number 4 symbolizes perseverance, order, and solid foundations. You are a true builder who works methodically. Traits: disciplined, reliable, hardworking, practical.",
                "lucky_color": "Dark Green & Earth Brown",
                "lucky_gem": "Green Jade",
                "best_day": "Thursday & Saturday",
                "challenge": "Learning flexibility and openness toward unexpected change."
            },
            5: {
                "title": "The True Adventurer",
                "desc": "Number 5 radiates freedom, adventure, and extraordinary adaptability. You are born to explore and break conventional limits. Traits: dynamic, curious, flexible, charismatic.",
                "lucky_color": "Turquoise Blue & Gray",
                "lucky_gem": "Aquamarine",
                "best_day": "Wednesday & Friday",
                "challenge": "Maintaining commitment and avoiding an unstable lifestyle."
            },
            6: {
                "title": "The Harmony Guardian",
                "desc": "Number 6 symbolizes responsibility, love, and family harmony. You are a nurturing soul always present for loved ones. Traits: caring, protective, loving, gifted in art and decoration.",
                "lucky_color": "Dark Blue & Rose Gold",
                "lucky_gem": "Blue Sapphire",
                "best_day": "Friday & Tuesday",
                "challenge": "Learning to release perfectionism and embrace imperfection with grace."
            },
            7: {
                "title": "The Truth Seeker",
                "desc": "Number 7 radiates intellectualism, spirituality, and the pursuit of deepest meaning. You are a mystical soul always hungry for knowledge and wisdom. Traits: analytical, intuitive, mysterious, spiritually independent.",
                "lucky_color": "Deep Purple & White",
                "lucky_gem": "Dark Amethyst",
                "best_day": "Saturday & Monday",
                "challenge": "Opening yourself to deeper and warmer emotional connections."
            },
            8: {
                "title": "The Power Builder",
                "desc": "Number 8 symbolizes worldly ambition, material strength, and powerful execution abilities. You are born to manage wealth, lead great organizations, and leave an enduring legacy. Traits: decisive, ambitious, authoritative.",
                "lucky_color": "Black & Gold",
                "lucky_gem": "Black Onyx",
                "best_day": "Saturday & Thursday",
                "challenge": "Balancing material achievements with inner satisfaction and genuine love."
            },
            9: {
                "title": "The Universal Philanthropist",
                "desc": "Number 9 is the highest number in the cycle, symbolizing universal compassion, wisdom, and service to others. You are a matured soul with a noble mission to illuminate the world. Traits: altruistic, wise, humanitarian.",
                "lucky_color": "Dark Red & Antique Gold",
                "lucky_gem": "Garnet",
                "best_day": "Tuesday & Thursday",
                "challenge": "Learning to set healthy boundaries to avoid exhaustion from constant giving."
            },
            11: {
                "title": "Master Number: The Soul Illuminator",
                "desc": "Master Number 11 is the highest spiritual enlightenment number. You possess intuition beyond ordinary human capacity, extraordinary sensitivity to surrounding energies, and the potential to become a world-class spiritual leader or visionary artist.",
                "lucky_color": "Pure White & Silver",
                "lucky_gem": "White Diamond",
                "best_day": "Monday & Friday",
                "challenge": "Managing extreme sensitivity before it transforms into anxiety and overthinking."
            },
            22: {
                "title": "Master Number: The Grand Architect",
                "desc": "Master Number 22 holds the highest potential — 'The Master Builder'. You can manifest the grandest visions into concrete reality. Traits: visionary, pragmatic, great-spirited, capable of leading civilizational change.",
                "lucky_color": "Antique Gold & Dark Red",
                "lucky_gem": "Red Ruby",
                "best_day": "Thursday & Sunday",
                "challenge": "Maintaining humility amid extraordinary achievement potential."
            },
            33: {
                "title": "Master Number: The Supreme Teacher",
                "desc": "Master Number 33 is the rarest and most noble — 'The Master Teacher'. You are born with a sacred mission to be a teacher, healer, or spiritual leader bringing profound transformation to thousands or even millions of souls.",
                "lucky_color": "Gold & Pure White",
                "lucky_gem": "Diamond & Sapphire",
                "best_day": "Friday & Monday",
                "challenge": "Finding balance between total devotion to the world and personal self-care."
            }
        }

        lp_desc_id = NUM_DESC_ID.get(life_path, NUM_DESC_ID[9])
        lp_desc_en = NUM_DESC_EN.get(life_path, NUM_DESC_EN[9])
        dest_desc_id = NUM_DESC_ID.get(destiny_num, NUM_DESC_ID[1])
        dest_desc_en = NUM_DESC_EN.get(destiny_num, NUM_DESC_EN[1])
        soul_desc_id = NUM_DESC_ID.get(soul_urge_num, NUM_DESC_ID[1])
        soul_desc_en = NUM_DESC_EN.get(soul_urge_num, NUM_DESC_EN[1])

        return {
            "life_path": life_path,
            "destiny": destiny_num,
            "soul_urge": soul_urge_num,
            "personality": personality_num,
            "lucky_nums": [life_path, destiny_num, (life_path + destiny_num) % 9 or 9],
            "lp_desc_id": lp_desc_id,
            "lp_desc_en": lp_desc_en,
            "dest_desc_id": dest_desc_id,
            "dest_desc_en": dest_desc_en,
            "soul_desc_id": soul_desc_id,
            "soul_desc_en": soul_desc_en,
        }

    @staticmethod
    def calculate_compatibility(p1_name: str, p1_date: datetime.date, 
                                p2_name: str, p2_date: datetime.date) -> Dict[str, Any]:
        """
        Calculates relationship compatibility using combined Javanese Weton neptu
        rules and Numerology Life Path intersections.
        """
        weton1 = DestinyEngine.calculate_weton(p1_date)
        weton2 = DestinyEngine.calculate_weton(p2_date)
        
        num1 = DestinyEngine.calculate_numerology(p1_name, p1_date)
        num2 = DestinyEngine.calculate_numerology(p2_name, p2_date)
        
        total_neptu = weton1["neptu_total"] + weton2["neptu_total"]
        weton_mod = total_neptu % 8
        
        # Javanese Weton compatibility classifications (The Remainder / Sisa)
        weton_cats_id = {
            1: ("PEGAT", "Berisiko menghadapi tantangan ekonomi atau dinamika komunikasi, namun tangguh menghadapi badai hidup jika tekun."),
            2: ("RATU", "Sangat serasi, dihormati lingkungan sekitar, dilingkupi kemakmuran, dan menjadi teladan keluarga."),
            3: ("JODOH", "Pasangan sejati (soulmates). Sangat cocok, harmonis, saling melengkapi kekurangan satu sama lain."),
            4: ("TOPO", "Mengalami cobaan di masa-masa awal, tetapi akan sukses besar dan bahagia luar biasa di hari tua."),
            5: ("TINARI", "Dianugerahi rezeki berlimpah, perjalanan hidup menyenangkan, dan mudah mendapatkan jalan keluar dari masalah."),
            6: ("PADU", "Sering berdebat pada hal kecil, namun ikatan emosi sangat kuat dan tidak akan pernah terpisahkan."),
            7: ("SUJANAN", "Hubungan spiritual tinggi, penuh petualangan, diuji loyalitas, tetapi melahirkan keturunan yang cerdas."),
            0: ("PESTHI", "Kehidupan rumah tangga rukun, tenang, tenteram, damai tanpa hambatan berarti hingga maut memisahkan.")
        }
        
        weton_cats_en = {
            1: ("PEGAT (Struggle)", "Might encounter early adjustments in communication or finance, but stays highly resilient if joint effort is applied."),
            2: ("RATU (Royalty)", "Exceedingly harmonious, widely respected by peers, surrounded by prosperity and domestic stability."),
            3: ("JODOH (Soulmates)", "True spiritual partners. Effortlessly aligned, perfectly balancing each other's gaps."),
            4: ("TOPO (Ascetic)", "May face early tests, transitioning into supreme success and absolute serenity in later ages."),
            5: ("TINARI (Bountiful)", "Blessed with uninterrupted material flow, rich travel journeys, and persistent problem-solving luck."),
            6: ("PADU (Dynamic)", "Prone to light arguments, but core emotional ties are deeply set. Highly passionate."),
            7: ("SUJANAN (Tested)", "Strong spiritual attachment, highly adventurous, occasional tests of loyalty but produces bright successors."),
            0: ("PESTHI (Serene)", "Exceptionally peaceful, steady, and tranquil lifestyle together through all seasons of life.")
        }
        
        cat_id, desc_id = weton_cats_id[weton_mod]
        cat_en, desc_en = weton_cats_en[weton_mod]
        
        # Compatibility Scoring algorithm (Percentage)
        base_score = 60
        # Weton contribution
        weton_score_map = {1: 15, 2: 35, 3: 40, 4: 25, 5: 35, 6: 20, 7: 20, 0: 40}
        base_score += weton_score_map[weton_mod]
        
        # Numerology overlap adjustments
        num_diff = abs((num1["life_path"] % 9 or 9) - (num2["life_path"] % 9 or 9))
        if num_diff == 0:
            base_score += 15 # Soul mates
        elif num_diff in [3, 6]:
            base_score += 10 # Harmonious
        else:
            base_score -= 5  # Opposites but attractive
            
        final_score = max(45, min(99, base_score))
        
        return {
            "score": final_score,
            "category_id": cat_id,
            "category_en": cat_en,
            "desc_id": desc_id,
            "desc_en": desc_en,
            "p1_weton": f"{weton1['day_id']} {weton1['pasaran']}",
            "p2_weton": f"{weton2['day_id']} {weton2['pasaran']}",
            "p1_neptu": weton1["neptu_total"],
            "p2_neptu": weton2["neptu_total"]
        }


# ==============================================================================
# DATABASES: PRIMBON & DREAMS
# ==============================================================================
ENCYCLOPEDIA_DATA = [
    # ── TANDA ALAM / NATURAL SIGNS ─────────────────────────────────────────────
    {
        "cat_id": "Tanda Alam", "cat_en": "Natural Signs",
        "title_id": "Firasat Telinga Berdenging", "title_en": "Ringing Ear Signals",
        "desc_id": "Telinga kanan berdenging di pagi hari menandakan akan menerima sanjungan atau kabar baik dari kerabat dekat. Di malam hari menandakan akan ada tamu membawa berkah. Telinga kiri berdenging siang hari pertanda ada yang merindukan Anda dari jauh.",
        "desc_en": "Ringing in the right ear in the morning signifies upcoming praise or good news from close family. At night, it hints at unexpected guests bringing prosperity. Left ear ringing at noon means someone far away is thinking of you fondly."
    },
    {
        "cat_id": "Tanda Alam", "cat_en": "Natural Signs",
        "title_id": "Burung Hantu Berbunyi di Malam Hari", "title_en": "Owl Crying at Night",
        "desc_id": "Suara burung hantu (burung gagak) di malam hari di sekitar rumah merupakan tanda peringatan dari alam gaib agar penghuni rumah lebih berhati-hati. Cepat bersedekah dan perbanyak doa perlindungan.",
        "desc_en": "The sound of an owl near the home at night is a warning from the spirit realm for the household to be more cautious. Giving charity and increasing protective prayers is strongly advised."
    },
    {
        "cat_id": "Tanda Alam", "cat_en": "Natural Signs",
        "title_id": "Cicak Jatuh di Atas Kepala", "title_en": "Gecko Falling on Your Head",
        "desc_id": "Cicak jatuh di kepala merupakan pertanda rezeki berlimpah dan keberuntungan besar sedang dalam perjalanan menuju hidup Anda. Beberapa versi primbon menyebut ini sebagai tanda amanah besar yang segera dipercayakan.",
        "desc_en": "A gecko falling on your head signals abundant fortune and great luck heading your way. Some versions of primbon describe this as a sign that a significant responsibility or trust will soon be given to you."
    },
    {
        "cat_id": "Tanda Alam", "cat_en": "Natural Signs",
        "title_id": "Kucing Menangis di Depan Pintu", "title_en": "Cat Crying at the Door",
        "desc_id": "Kucing menangis atau mengeong terus-menerus di depan pintu rumah dipercaya sebagai pertanda ada makhluk gaib yang mencoba masuk atau ada anggota keluarga yang akan mengalami musibah. Segera bacakan doa tolak bala.",
        "desc_en": "A cat crying or meowing persistently at the door is believed to signal a spirit trying to enter or a family member may soon face misfortune. Reciting protective prayers is recommended immediately."
    },
    {
        "cat_id": "Tanda Alam", "cat_en": "Natural Signs",
        "title_id": "Bintang Jatuh di Tengah Malam", "title_en": "Falling Star at Midnight",
        "desc_id": "Melihat bintang jatuh di tengah malam buta bukan hanya pertanda untuk meminta harapan. Dalam primbon Jawa kuno, ini adalah momen langka ketika gerbang langit terbuka sesaat — doa yang dipanjatkan dengan sepenuh hati di saat itu memiliki kekuatan spiritual berlipat ganda.",
        "desc_en": "Witnessing a falling star at midnight is not merely a moment to make a wish. In ancient Javanese primbon, this is a rare moment when the celestial gate briefly opens — prayers offered sincerely at that moment carry multiplied spiritual power."
    },
    # ── PRANATA MANGSA / COSMIC SEASONS ──────────────────────────────────────
    {
        "cat_id": "Pranata Mangsa", "cat_en": "Cosmic Season",
        "title_id": "Kasa (Kartika) – Musim Pertama", "title_en": "Kasa (Kartika) – First Season",
        "desc_id": "Dimulai pertengahan Juni–awal Agustus. Ditandai dedaunan berguguran dan angin dingin. Waktu yang pas untuk merencanakan awal baru atau menanam akar spiritual yang kuat.",
        "desc_en": "Starts mid-June to early August. Marked by falling leaves and cold wind. Optimal for planning new beginnings or establishing deep spiritual foundations."
    },
    {
        "cat_id": "Pranata Mangsa", "cat_en": "Cosmic Season",
        "title_id": "Karo (Pusa) – Musim Kedua", "title_en": "Karo (Pusa) – Second Season",
        "desc_id": "Berlangsung awal Agustus–pertengahan September. Masa kering memuncak, angin panas bertiup. Hindari konfrontasi dan pertengkaran. Saatnya memperkuat kesabaran batin dan menabung energi untuk panen mendatang.",
        "desc_en": "Runs early August to mid-September. Peak dry season with hot winds. Avoid confrontations. A time for strengthening inner patience and saving energy for the upcoming harvest."
    },
    {
        "cat_id": "Pranata Mangsa", "cat_en": "Cosmic Season",
        "title_id": "Katelu (Manggasri) – Musim Ketiga", "title_en": "Katelu (Manggasri) – Third Season",
        "desc_id": "Pertengahan September–Oktober. Tanda-tanda awal musim penghujan mulai terasa. Waktu yang sangat baik untuk memulai usaha baru, membangun rumah, atau mengikat janji.",
        "desc_en": "Mid-September to October. Early signs of the rainy season appear. An excellent time to start new businesses, build homes, or make significant vows."
    },
    {
        "cat_id": "Pranata Mangsa", "cat_en": "Cosmic Season",
        "title_id": "Kawolu (Jita) – Musim Kedelapan", "title_en": "Kawolu (Jita) – Eighth Season",
        "desc_id": "Pertengahan Januari–Februari. Musim paling lebat hujannya. Saat ideal untuk introspeksi diri mendalam, menulis rencana hidup jangka panjang, dan memperkuat ikatan keluarga.",
        "desc_en": "Mid-January to February. The wettest season. Ideal for deep self-reflection, writing long-term life plans, and strengthening family bonds."
    },
    # ── FIRASAT TUBUH / BODY SENSATIONS ─────────────────────────────────────
    {
        "cat_id": "Firasat Tubuh", "cat_en": "Body Sensations",
        "title_id": "Kedutan Mata Kanan Atas", "title_en": "Right Upper Eyelid Twitching",
        "desc_id": "Menandakan Anda akan mendapatkan rezeki tak terduga atau bertemu kembali dengan kawan lama yang membawa peluang bisnis luar biasa. Jaga mood positif sepanjang hari.",
        "desc_en": "Signifies unexpected financial fortune or reuniting with an old friend carrying outstanding opportunities. Maintain a positive disposition throughout the day."
    },
    {
        "cat_id": "Firasat Tubuh", "cat_en": "Body Sensations",
        "title_id": "Kedutan Mata Kiri Bawah", "title_en": "Left Lower Eyelid Twitching",
        "desc_id": "Pertanda akan menangis atau mengalami kesedihan dalam waktu dekat. Primbon menyarankan agar memperbanyak doa dan bersabar menghadapi ujian yang akan datang.",
        "desc_en": "A sign that tears or sadness may come in the near future. Primbon advises increasing prayer and preparing patience for incoming trials."
    },
    {
        "cat_id": "Firasat Tubuh", "cat_en": "Body Sensations",
        "title_id": "Telapak Tangan Kanan Gatal", "title_en": "Right Palm Itching",
        "desc_id": "Telapak tangan kanan gatal adalah pertanda uang atau rezeki sedang menghampiri Anda. Akan ada pemasukan tak terduga, hadiah, atau pemberian dari seseorang yang tidak disangka.",
        "desc_en": "An itching right palm is a sign that money or prosperity is approaching. An unexpected income, gift, or reward from someone may arrive soon."
    },
    {
        "cat_id": "Firasat Tubuh", "cat_en": "Body Sensations",
        "title_id": "Telapak Tangan Kiri Gatal", "title_en": "Left Palm Itching",
        "desc_id": "Telapak tangan kiri gatal justru pertanda akan ada pengeluaran atau kebutuhan mendadak yang menguras kantong. Bijak-bijaklah dalam mengelola keuangan di hari-hari ini.",
        "desc_en": "An itching left palm forewarns of upcoming expenses or sudden financial needs. Exercise prudence in managing finances during these days."
    },
    {
        "cat_id": "Firasat Tubuh", "cat_en": "Body Sensations",
        "title_id": "Cegukan Tiba-Tiba", "title_en": "Sudden Hiccupping",
        "desc_id": "Dalam keyakinan primbon, cegukan tiba-tiba berarti ada orang yang sedang membicarakan nama Anda. Jika ingin mengetahui siapa, sebutkan nama-nama orang satu per satu — saat cegukan berhenti, itulah orangnya.",
        "desc_en": "In primbon belief, sudden hiccupping means someone is talking about you. To identify who, recite the names of people one by one — when the hiccup stops, that is the person thinking of you."
    },
    {
        "cat_id": "Firasat Tubuh", "cat_en": "Body Sensations",
        "title_id": "Kuping Panas Tiba-Tiba", "title_en": "Sudden Ear Warmth / Burning",
        "desc_id": "Telinga terasa panas tiba-tiba merupakan tanda seseorang sedang membahas Anda dengan emosi kuat, bisa berupa pujian berapi-api atau kemarahan. Tetaplah tenang dan jangan bereaksi berlebihan.",
        "desc_en": "A sudden burning sensation in the ears signals that someone is passionately talking about you — either with intense praise or strong anger. Stay calm and avoid overreacting."
    },
    # ── AURA / SPIRITUAL AURA ────────────────────────────────────────────────
    {
        "cat_id": "Aura", "cat_en": "Spiritual Aura",
        "title_id": "Warna Aura Emas Purba", "title_en": "Ancient Gold Aura",
        "desc_id": "Aura emas melambangkan kepemimpinan spiritual, integritas tanpa batas, dan kekuatan batin untuk menyembuhkan trauma masa lalu. Orang beraura emas secara alami disukai khalayak luas dan memiliki karisma pemimpin sejati.",
        "desc_en": "A golden aura symbolizes spiritual leadership, boundless integrity, and inner strength to heal past wounds. People with golden auras are naturally popular and carry the charisma of a true leader."
    },
    {
        "cat_id": "Aura", "cat_en": "Spiritual Aura",
        "title_id": "Warna Aura Ungu Mistis", "title_en": "Mystical Purple Aura",
        "desc_id": "Aura ungu menandakan kemampuan intuisi dan kepekaan spiritual yang sangat tinggi. Orang beraura ungu sering memiliki kemampuan merasakan hal-hal gaib, mimpi-mimpi profetik, dan koneksi kuat dengan alam leluhur.",
        "desc_en": "A purple aura indicates highly developed intuition and spiritual sensitivity. People with purple auras often perceive supernatural phenomena, experience prophetic dreams, and maintain strong connections with ancestral realms."
    },
    {
        "cat_id": "Aura", "cat_en": "Spiritual Aura",
        "title_id": "Warna Aura Putih Bersih", "title_en": "Pure White Aura",
        "desc_id": "Aura putih bersih adalah aura paling langka dan mulia. Melambangkan kemurnian jiwa sejati, ketulusan hati, kedekatan dengan Sang Pencipta, dan seringkali dimiliki oleh para wali, pertapa, atau individu yang telah melewati cobaan berat dengan penuh keikhlasan.",
        "desc_en": "A pure white aura is the rarest and most noble of all auras. It symbolizes true soul purity, sincere heart, closeness to the Divine Creator, and is often found in saints, hermits, or those who have passed great trials with absolute sincerity."
    },
    {
        "cat_id": "Aura", "cat_en": "Spiritual Aura",
        "title_id": "Warna Aura Merah Menyala", "title_en": "Blazing Red Aura",
        "desc_id": "Aura merah memancarkan energi yang kuat, semangat juang tinggi, dan vitalitas fisik yang luar biasa. Namun aura ini juga bisa menandakan amarah terpendam, tekanan emosi, atau konflik yang belum terselesaikan. Meditasi dan olahraga rutin sangat dianjurkan.",
        "desc_en": "A blazing red aura radiates intense energy, high fighting spirit, and extraordinary physical vitality. However, it can also indicate suppressed anger, emotional pressure, or unresolved conflict. Meditation and regular exercise are strongly advised."
    },
    {
        "cat_id": "Aura", "cat_en": "Spiritual Aura",
        "title_id": "Warna Aura Hijau Zamrud", "title_en": "Emerald Green Aura",
        "desc_id": "Aura hijau melambangkan penyembuhan, keseimbangan, dan keharmonisan dengan alam semesta. Orang beraura hijau memiliki bakat alami sebagai penyembuh, konselor, atau pemimpin komunitas yang dicintai dan dipercaya banyak orang.",
        "desc_en": "A green aura symbolizes healing, balance, and harmony with the universe. Those with green auras have natural gifts as healers, counselors, or beloved community leaders trusted by many."
    },
    # ── WETON & NEPTU KHUSUS / SPECIAL WETON ────────────────────────────────
    {
        "cat_id": "Weton Istimewa", "cat_en": "Special Weton",
        "title_id": "Jumat Kliwon – Weton Paling Sakral", "title_en": "Friday Kliwon – The Most Sacred Weton",
        "desc_id": "Jumat Kliwon adalah kombinasi weton paling sakral dalam kalender Jawa. Konon malam Jumat Kliwon adalah saat tirai antara alam nyata dan alam gaib menipis. Ini saat yang paling kuat untuk berdoa, bertapa, bersedekah, dan memohon pertolongan leluhur. Orang lahir Jumat Kliwon dikaruniai kekuatan batin luar biasa.",
        "desc_en": "Friday Kliwon is the most sacred weton combination in the Javanese calendar. It is said the veil between the physical and spirit realms grows thin on this night. It is the most powerful time for prayer, fasting, charity, and seeking ancestral guidance. Those born on Friday Kliwon are blessed with extraordinary inner spiritual power."
    },
    {
        "cat_id": "Weton Istimewa", "cat_en": "Special Weton",
        "title_id": "Selasa Kliwon – Weton Pejuang", "title_en": "Tuesday Kliwon – The Warrior Weton",
        "desc_id": "Selasa Kliwon dipercaya sebagai weton para ksatria dan pejuang. Mereka yang lahir pada weton ini memiliki tekad baja, keberanian luar biasa, dan jiwa kepemimpinan yang sangat kuat. Namun perlu menjaga temperamen agar tidak mudah terpancing emosi.",
        "desc_en": "Tuesday Kliwon is believed to be the weton of warriors and knights. Those born on this weton possess iron resolve, extraordinary courage, and a very strong leadership spirit. However, managing their temperament to avoid being easily provoked emotionally is essential."
    },
    {
        "cat_id": "Weton Istimewa", "cat_en": "Special Weton",
        "title_id": "Rabu Wage – Weton Para Seniman", "title_en": "Wednesday Wage – The Artist Weton",
        "desc_id": "Rabu Wage adalah weton yang banyak melahirkan seniman, penulis, musisi, dan jiwa-jiwa kreatif berbakat. Mereka memiliki imajinasi yang melimpah dan kemampuan mengekspresikan perasaan mendalam melalui berbagai media seni.",
        "desc_en": "Wednesday Wage is a weton that births many artists, writers, musicians, and creatively gifted souls. They possess overflowing imagination and the ability to express deep feelings through various artistic media."
    },
    {
        "cat_id": "Weton Istimewa", "cat_en": "Special Weton",
        "title_id": "Kamis Pahing – Weton Pedagang Sukses", "title_en": "Thursday Pahing – The Merchant Weton",
        "desc_id": "Kamis Pahing menghasilkan individu dengan naluri bisnis yang sangat tajam. Mereka berbakat dalam dunia perdagangan, negosiasi, dan membangun jaringan relasi yang luas. Rezeki mereka umumnya mengalir deras dari dunia usaha dan investasi.",
        "desc_en": "Thursday Pahing produces individuals with very sharp business instincts. They are gifted in commerce, negotiation, and building broad relationship networks. Their prosperity generally flows strongly from the world of business and investment."
    },
    # ── LARANGAN & PANTANGAN / TABOOS ───────────────────────────────────────
    {
        "cat_id": "Pantangan Adat", "cat_en": "Traditional Taboos",
        "title_id": "Pantangan Memotong Kuku di Malam Hari", "title_en": "Taboo: Cutting Nails at Night",
        "desc_id": "Dalam tradisi Jawa kuno, memotong kuku di malam hari dipercaya dapat mempersingkat umur atau mengundang kehadiran roh jahat. Kebiasaan ini diperkirakan bermula dari zaman pra-modern saat tidak ada penerangan memadai, sehingga praktis berbahaya pula secara fisik.",
        "desc_en": "In ancient Javanese tradition, cutting nails at night is believed to shorten one's life or invite evil spirits. This custom likely originated in pre-modern times when adequate lighting was absent, making it physically dangerous as well."
    },
    {
        "cat_id": "Pantangan Adat", "cat_en": "Traditional Taboos",
        "title_id": "Pantangan Bersiul di Dalam Rumah", "title_en": "Taboo: Whistling Indoors",
        "desc_id": "Bersiul di dalam rumah terutama pada malam hari dipercaya dapat memanggil makhluk gaib atau mengundang nasib buruk. Primbon menyarankan agar kegiatan bersiul dilakukan di luar ruangan dan bukan saat matahari telah terbenam.",
        "desc_en": "Whistling inside the house, especially at night, is believed to summon supernatural beings or invite misfortune. Primbon suggests that whistling should be done outdoors and not after sunset."
    },
    {
        "cat_id": "Pantangan Adat", "cat_en": "Traditional Taboos",
        "title_id": "Pantangan Duduk di Depan Pintu", "title_en": "Taboo: Sitting at the Doorway",
        "desc_id": "Duduk di ambang pintu diyakini akan menghambat rezeki masuk ke dalam rumah. Pintu adalah jalur energi utama, dan menutupnya dengan tubuh sendiri akan memblokir aliran keberuntungan dari luar.",
        "desc_en": "Sitting in a doorway is believed to block prosperity from entering the home. The door is a main energy pathway, and blocking it with one's body will obstruct the flow of luck from outside."
    },
    {
        "cat_id": "Pantangan Adat", "cat_en": "Traditional Taboos",
        "title_id": "Pantangan Menyapu Malam Hari", "title_en": "Taboo: Sweeping at Night",
        "desc_id": "Menyapu lantai setelah Maghrib dipercaya akan menyapu keluar rezeki dari dalam rumah. Itu sebabnya para sesepuh menganjurkan seluruh kegiatan bersih-bersih dilakukan sebelum sore hari agar energi positif dan rezeki tetap terjaga di dalam rumah.",
        "desc_en": "Sweeping the floor after the Maghrib prayer (dusk) is believed to sweep out the household's fortune. That is why elders advise completing all cleaning before the afternoon so that positive energy and prosperity remain inside the home."
    },
    # ── RITUAL & TRADISI / RITUALS ───────────────────────────────────────────
    {
        "cat_id": "Ritual Nusantara", "cat_en": "Archipelago Rituals",
        "title_id": "Selamatan – Syukur Bersama", "title_en": "Selamatan – Communal Thanksgiving",
        "desc_id": "Selamatan adalah tradisi ritual makan bersama yang diadakan untuk merayakan momen penting seperti kelahiran, pernikahan, kematian, atau pindah rumah. Tujuannya untuk mengundang berkah, keselamatan, dan perlindungan dari segala gangguan gaib bagi seluruh anggota komunitas.",
        "desc_en": "Selamatan is a ritual communal meal tradition held to celebrate important milestones such as births, weddings, deaths, or moving to a new home. Its purpose is to invite blessings, safety, and protection from all supernatural disturbances for the entire community."
    },
    {
        "cat_id": "Ritual Nusantara", "cat_en": "Archipelago Rituals",
        "title_id": "Tirakatan – Lelaku Spiritual Malam Hari", "title_en": "Tirakatan – Night Spiritual Discipline",
        "desc_id": "Tirakatan adalah praktik menahan hawa nafsu (bisa berupa puasa, tidak tidur, atau meditasi) selama satu malam penuh, biasanya dilakukan pada malam-malam sakral seperti 17 Agustus, Jumat Kliwon, atau sebelum hajat besar. Tujuannya menjernihkan batin dan memperkuat permohonan kepada Yang Maha Kuasa.",
        "desc_en": "Tirakatan is the practice of restraining desires (fasting, staying awake, or meditating) for a full night, usually done on sacred nights like August 17th, Friday Kliwon, or before major life events. Its purpose is to purify the inner self and strengthen one's supplication to the Almighty."
    },
    {
        "cat_id": "Ritual Nusantara", "cat_en": "Archipelago Rituals",
        "title_id": "Kenduri Arwah – Mendoakan Leluhur", "title_en": "Kenduri Arwah – Honoring Ancestors",
        "desc_id": "Kenduri Arwah adalah tradisi selamatan yang khusus ditujukan untuk mendoakan arwah leluhur yang telah meninggal dunia. Biasanya dilaksanakan pada hari ke-3, ke-7, ke-40, ke-100, dan ke-1000 setelah kematian, serta setiap malam Jumat. Kepercayaan ini meyakini bahwa doa keturunan yang hidup masih bisa sampai dan memberikan ketenangan bagi arwah.",
        "desc_en": "Kenduri Arwah is a selamatan tradition specifically intended to pray for the souls of deceased ancestors. Usually held on the 3rd, 7th, 40th, 100th, and 1000th day after death, as well as every Thursday evening. The belief holds that prayers from living descendants can still reach and bring peace to departed souls."
    },
    # ── SHIO TIONGHOA-NUSANTARA / CHINESE-ARCHIPELAGO ZODIAC ────────────────
    {
        "cat_id": "Shio & Zodiak", "cat_en": "Shio & Zodiac",
        "title_id": "Shio Macan – Si Raja Hutan", "title_en": "Tiger Shio – King of the Forest",
        "desc_id": "Shio Macan dilahirkan pada tahun: 1926, 1938, 1950, 1962, 1974, 1986, 1998, 2010, 2022. Karakternya: berani, karismatik, penuh semangat, dan pantang menyerah. Mereka pemimpin alami namun perlu mengendalikan sifat impulsif. Hoki terbaik di bulan ke-1, 3, dan 7.",
        "desc_en": "Tiger Shio years: 1926, 1938, 1950, 1962, 1974, 1986, 1998, 2010, 2022. Character: brave, charismatic, spirited, and relentless. They are natural leaders who must control impulsive tendencies. Best luck in months 1, 3, and 7."
    },
    {
        "cat_id": "Shio & Zodiak", "cat_en": "Shio & Zodiac",
        "title_id": "Shio Naga – Makhluk Paling Beruntung", "title_en": "Dragon Shio – The Luckiest Creature",
        "desc_id": "Shio Naga dilahirkan pada tahun: 1928, 1940, 1952, 1964, 1976, 1988, 2000, 2012, 2024. Karakternya: penuh visi, berwibawa, ambisius, dan dikaruniai keberuntungan alami yang luar biasa. Mereka berbakat menjadi pemimpin dan inovator yang mengubah dunia.",
        "desc_en": "Dragon Shio years: 1928, 1940, 1952, 1964, 1976, 1988, 2000, 2012, 2024. Character: visionary, authoritative, ambitious, and naturally blessed with extraordinary luck. They are gifted to become world-changing leaders and innovators."
    },
    {
        "cat_id": "Shio & Zodiak", "cat_en": "Shio & Zodiac",
        "title_id": "Shio Kuda – Si Jiwa Bebas", "title_en": "Horse Shio – The Free Spirit",
        "desc_id": "Shio Kuda dilahirkan pada tahun: 1930, 1942, 1954, 1966, 1978, 1990, 2002, 2014, 2026. Karakternya: energetik, cerdas, suka kebebasan, dan sangat mandiri. Mereka berbakat dalam perjalanan, eksplorasi, dan pekerjaan yang tidak terikat rutin.",
        "desc_en": "Horse Shio years: 1930, 1942, 1954, 1966, 1978, 1990, 2002, 2014, 2026. Character: energetic, intelligent, freedom-loving, and very independent. They excel in travel, exploration, and roles that are not bound by routine."
    },
    # ── KEJAWEN / JAVANESE MYSTICISM ─────────────────────────────────────────
    {
        "cat_id": "Kejawen", "cat_en": "Javanese Mysticism",
        "title_id": "Konsep Memayu Hayuning Bawana", "title_en": "Memayu Hayuning Bawana Concept",
        "desc_id": "Memayu Hayuning Bawana adalah filosofi Jawa tertinggi yang bermakna 'memperindah keindahan dunia'. Ini adalah tugas mulia setiap manusia Jawa: untuk menjaga keharmonisan alam, masyarakat, dan diri sendiri. Hidup bukan hanya untuk kepentingan diri sendiri, melainkan untuk mempercantik semesta.",
        "desc_en": "Memayu Hayuning Bawana is the highest Javanese philosophy meaning 'beautifying the beauty of the world'. It is the noble duty of every Javanese person: to maintain harmony in nature, society, and the self. Life is not just for personal gain, but to beautify the universe."
    },
    {
        "cat_id": "Kejawen", "cat_en": "Javanese Mysticism",
        "title_id": "Konsep Sangkan Paraning Dumadi", "title_en": "Sangkan Paraning Dumadi Concept",
        "desc_id": "Sangkan Paraning Dumadi bermakna 'dari mana asal dan ke mana tujuan segala yang ada'. Ini adalah pertanyaan terdalam dalam filsafat Kejawen tentang asal-usul manusia dari Tuhan dan kembalinya jiwa kepada sumber semesta. Hidup adalah perjalanan spiritual untuk mengenal diri sejati.",
        "desc_en": "Sangkan Paraning Dumadi means 'from where all things come and where they are destined'. This is the deepest question in Kejawen philosophy regarding humanity's origin from God and the soul's return to the universal source. Life is a spiritual journey to know the true self."
    },
    {
        "cat_id": "Kejawen", "cat_en": "Javanese Mysticism",
        "title_id": "Empat Nafsu Manusia (Sedulur Papat)", "title_en": "Four Human Desires (Sedulur Papat)",
        "desc_id": "Dalam Kejawen, manusia memiliki empat saudara gaib (sedulur papat): Kakang Kawah (air ketuban), Ari-ari (plasenta), Getih (darah), dan Puser (tali pusar). Keempat saudara ini menjadi penjaga spiritual seumur hidup. Menghormati dan merawat keempatnya melalui doa dan laku batin adalah kunci keselamatan jiwa.",
        "desc_en": "In Kejawen, a person has four spiritual siblings (sedulur papat): Kakang Kawah (amniotic fluid), Ari-ari (placenta), Getih (blood), and Puser (umbilical cord). These four siblings serve as lifelong spiritual guardians. Honoring and nurturing all four through prayer and inner discipline is the key to soul safety."
    },
]

DREAM_DATA = [
    # ── SPIRITUAL ──────────────────────────────────────────────────────────────
    {
        "cat_id": "Spiritual", "cat_en": "Spiritual",
        "keywords": ["harimau", "macan", "tiger", "putih", "white"],
        "title_id": "Bermimpi Bertemu Harimau Putih", "title_en": "Dreaming of a White Tiger",
        "desc_id": "Anda sedang dijaga oleh khodam leluhur yang sangat kuat. Ini isyarat bahwa derajat sosial atau kewibawaan Anda akan meningkat pesat dalam waktu dekat. Jika harimau itu berbicara, perhatikan kata-katanya sebagai pesan leluhur.",
        "desc_en": "You are currently guarded by a very powerful ancestral spirit. This signals that your social rank and influence will rise rapidly. If the tiger speaks, pay close attention as its words carry ancestral messages."
    },
    {
        "cat_id": "Spiritual", "cat_en": "Spiritual",
        "keywords": ["masjid", "gereja", "candi", "temple", "church", "mosque", "ibadah"],
        "title_id": "Bermimpi Berada di Tempat Ibadah", "title_en": "Dreaming of Being in a Place of Worship",
        "desc_id": "Mimpi berada di masjid, gereja, atau candi yang terang benderang adalah pertanda jiwa Anda sedang dibersihkan dan mendapat bimbingan spiritual. Saatnya memperkuat hubungan dengan Yang Maha Kuasa.",
        "desc_en": "Dreaming of being in a brightly lit mosque, church, or temple signals that your soul is being cleansed and spiritually guided. It is time to deepen your connection with the Almighty."
    },
    {
        "cat_id": "Spiritual", "cat_en": "Spiritual",
        "keywords": ["cahaya", "sinar", "light", "kilat", "aurora"],
        "title_id": "Bermimpi Melihat Cahaya Terang", "title_en": "Dreaming of Bright Light",
        "desc_id": "Cahaya terang dalam mimpi adalah simbol pencerahan, kebenaran, dan bimbingan ilahi. Mimpi ini menandakan Anda akan menemukan jalan keluar dari kebingungan atau masalah yang selama ini menghantui.",
        "desc_en": "Bright light in a dream is a symbol of enlightenment, truth, and divine guidance. This dream signals that you will find a way out of confusion or problems that have been haunting you."
    },
    {
        "cat_id": "Spiritual", "cat_en": "Spiritual",
        "keywords": ["air suci", "wudhu", "mandi", "sungai jernih", "holy water", "river"],
        "title_id": "Bermimpi Mandi di Sungai Jernih", "title_en": "Dreaming of Bathing in Clear River",
        "desc_id": "Mandi di air jernih atau melakukan wudhu dalam mimpi menandakan jiwa Anda sedang dalam proses penyucian diri yang mendalam. Dosa-dosa akan diampuni dan aura negatif sedang dibersihkan oleh kekuatan alam semesta.",
        "desc_en": "Bathing in clear water or performing ablution in a dream signals that your soul is undergoing profound purification. Sins will be forgiven and negative aura is being cleansed by universal forces."
    },
    # ── REZEKI / WEALTH ────────────────────────────────────────────────────────
    {
        "cat_id": "Rezeki", "cat_en": "Wealth",
        "keywords": ["ular", "snake", "digigit", "bite", "emas", "golden"],
        "title_id": "Bermimpi Digigit Ular Emas", "title_en": "Dreaming of Golden Snake Bite",
        "desc_id": "Bagi yang lajang, merupakan pertanda jodoh sudah sangat dekat. Bagi yang sudah menikah, melambangkan datangnya rezeki yang mengalir tiada henti seperti sungai di musim hujan.",
        "desc_en": "For singles, this indicates your soulmate is near. For married individuals, it symbolizes continuous flows of financial prosperity like a river in the rainy season."
    },
    {
        "cat_id": "Rezeki", "cat_en": "Wealth",
        "keywords": ["uang", "money", "harta", "koin", "gold", "coin", "duit"],
        "title_id": "Bermimpi Menemukan Uang Bertumpuk", "title_en": "Dreaming of Finding Piles of Money",
        "desc_id": "Menemukan uang dalam jumlah banyak dalam mimpi merupakan pertanda sangat baik. Ini menandakan rezeki tak terduga akan datang dalam waktu dekat, bisa berupa bonus, warisan, hadiah, atau kesempatan bisnis yang sangat menguntungkan.",
        "desc_en": "Finding large amounts of money in a dream is a very positive omen. It signals unexpected fortune arriving soon — a bonus, inheritance, gift, or highly lucrative business opportunity."
    },
    {
        "cat_id": "Rezeki", "cat_en": "Wealth",
        "keywords": ["sawah", "panen", "harvest", "ladang", "kebun", "field"],
        "title_id": "Bermimpi Panen di Sawah Subur", "title_en": "Dreaming of Harvesting Fertile Fields",
        "desc_id": "Mimpi memanen padi atau hasil kebun yang melimpah adalah simbol keberhasilan usaha yang selama ini dirintis. Semua kerja keras Anda akan berbuah manis. Saat yang tepat untuk memperluas usaha atau investasi.",
        "desc_en": "Dreaming of harvesting abundant rice or garden produce symbolizes the success of efforts you have been building. All your hard work will bear sweet fruit. A perfect time to expand your business or investments."
    },
    {
        "cat_id": "Rezeki", "cat_en": "Wealth",
        "keywords": ["ikan", "fish", "nelayan", "kolam", "pond", "laut"],
        "title_id": "Bermimpi Menangkap Banyak Ikan", "title_en": "Dreaming of Catching Many Fish",
        "desc_id": "Menangkap ikan dalam jumlah banyak dalam mimpi merupakan pertanda rezeki berlimpah dan target-target besar dalam kehidupan akan mudah tercapai. Primbon Jawa mengatakan ini adalah salah satu mimpi paling menguntungkan.",
        "desc_en": "Catching many fish in a dream is a sign of abundant prosperity and major life targets that will be easily achieved. Javanese primbon states this is one of the most fortunate dreams possible."
    },
    # ── PERINGATAN / WARNING ───────────────────────────────────────────────────
    {
        "cat_id": "Peringatan", "cat_en": "Warning",
        "keywords": ["terbang", "fly", "angkasa", "langit", "sky"],
        "title_id": "Bermimpi Terbang ke Angkasa", "title_en": "Dreaming of Flying High",
        "desc_id": "Pertanda hasrat kebebasan Anda sangat tinggi. Jika terbang dengan lancar, karir akan meningkat pesat. Namun jika tiba-tiba jatuh, waspada terhadap rencana yang terlalu ambisius tanpa perhitungan matang.",
        "desc_en": "Indicates your desire for freedom is very high. Smooth flying signals rapid career growth. But if you suddenly fall, beware of overly ambitious plans without careful consideration."
    },
    {
        "cat_id": "Peringatan", "cat_en": "Warning",
        "keywords": ["gigi", "tanggal", "copot", "teeth", "fall", "lepas"],
        "title_id": "Bermimpi Gigi Tanggal atau Copot", "title_en": "Dreaming of Falling Teeth",
        "desc_id": "Mimpi gigi tanggal atau copot adalah salah satu mimpi peringatan yang paling umum. Ini menandakan akan ada berita buruk, kehilangan orang tersayang, atau tantangan berat yang segera datang. Segera perbanyak doa dan sedekah.",
        "desc_en": "Dreaming of falling teeth is one of the most common warning dreams. It signals incoming bad news, loss of a loved one, or a severe challenge approaching. Increase prayers and charitable giving immediately."
    },
    {
        "cat_id": "Peringatan", "cat_en": "Warning",
        "keywords": ["api", "kebakaran", "fire", "bakar", "asap", "smoke"],
        "title_id": "Bermimpi Rumah Terbakar", "title_en": "Dreaming of House on Fire",
        "desc_id": "Rumah terbakar dalam mimpi bisa bermakna ganda. Jika api terang benderang tanpa asap hitam, pertanda akan ada perubahan besar menuju kemajuan. Namun jika disertai asap hitam dan kepanikan, ini adalah peringatan akan konflik keluarga serius.",
        "desc_en": "A burning house in a dream has dual meanings. If the fire is bright without black smoke, it signals great transformative changes ahead. But if accompanied by black smoke and panic, it warns of serious family conflicts."
    },
    {
        "cat_id": "Peringatan", "cat_en": "Warning",
        "keywords": ["dikejar", "chase", "lari", "run", "hantu", "ghost", "monster"],
        "title_id": "Bermimpi Dikejar Makhluk Gelap", "title_en": "Dreaming of Being Chased by Dark Entity",
        "desc_id": "Dikejar dalam mimpi oleh makhluk yang tidak dikenal menggambarkan adanya tekanan batin, ketakutan yang belum terselesaikan, atau masalah yang selama ini Anda hindari. Saatnya menghadapi rasa takut tersebut dengan keberanian dan kejujuran diri.",
        "desc_en": "Being chased in a dream by an unknown entity reflects inner pressure, unresolved fears, or problems you have been avoiding. It is time to face those fears with courage and self-honesty."
    },
    {
        "cat_id": "Peringatan", "cat_en": "Warning",
        "keywords": ["banjir", "flood", "air bah", "tenggelam", "drown"],
        "title_id": "Bermimpi Banjir Besar", "title_en": "Dreaming of a Great Flood",
        "desc_id": "Mimpi banjir besar menandakan emosi yang meluap dan situasi di luar kendali. Ini adalah peringatan agar Anda lebih bijak mengelola keuangan dan hubungan sosial sebelum 'kebanjiran' masalah di dunia nyata.",
        "desc_en": "Dreaming of a great flood signals overflowing emotions and situations beyond your control. It is a warning to manage your finances and social relationships more wisely before being 'flooded' with real-world problems."
    },
    # ── KEBERUNTUNGAN / LUCK ───────────────────────────────────────────────────
    {
        "cat_id": "Keberuntungan", "cat_en": "Luck",
        "keywords": ["keris", "pusaka", "heirloom", "senjata", "weapon", "pedang"],
        "title_id": "Mendapat Keris atau Pusaka Sakti", "title_en": "Receiving a Sacred Keris",
        "desc_id": "Mendapatkan keris atau pusaka dalam mimpi menandakan Anda akan mendapatkan amanah besar, kekuasaan, atau posisi penting dalam karir. Seseorang berpengaruh akan memberikan kepercayaan besar kepada Anda.",
        "desc_en": "Receiving a keris or heirloom in a dream indicates that you will receive a great trust, authority, or an important position in your career. An influential person will place great confidence in you."
    },
    {
        "cat_id": "Keberuntungan", "cat_en": "Luck",
        "keywords": ["bunga", "flower", "mekar", "bloom", "taman", "garden", "harum"],
        "title_id": "Bermimpi di Taman Bunga yang Indah", "title_en": "Dreaming of a Beautiful Flower Garden",
        "desc_id": "Taman bunga yang indah dan harum dalam mimpi adalah simbol kebahagiaan sejati, keharmonisan keluarga, dan keindahan yang akan Anda alami dalam waktu dekat. Hubungan asmara akan sangat romantis dan kehidupan sosial semakin menyenangkan.",
        "desc_en": "A beautiful and fragrant flower garden in a dream symbolizes true happiness, family harmony, and beauty you will soon experience. Romantic relationships will become very romantic and social life increasingly enjoyable."
    },
    {
        "cat_id": "Keberuntungan", "cat_en": "Luck",
        "keywords": ["emas", "gold", "perhiasan", "jewelry", "berlian", "diamond", "cincin"],
        "title_id": "Bermimpi Mendapat Perhiasan Emas", "title_en": "Dreaming of Receiving Gold Jewelry",
        "desc_id": "Mendapatkan perhiasan emas atau berlian dalam mimpi adalah pertanda keberuntungan besar dalam bidang finansial dan asmara. Bagi yang mencari jodoh, pertanda pasangan ideal sedang mendekat. Bagi yang berbisnis, keuntungan berlipat akan segera terwujud.",
        "desc_en": "Receiving gold jewelry or diamonds in a dream is a sign of great luck in finances and romance. For those seeking a partner, it signals the ideal companion is approaching. For those in business, multiplied profits will soon materialize."
    },
    {
        "cat_id": "Keberuntungan", "cat_en": "Luck",
        "keywords": ["naga", "dragon", "serpent", "ular besar", "naga emas"],
        "title_id": "Bermimpi Bertemu Naga", "title_en": "Dreaming of Meeting a Dragon",
        "desc_id": "Bertemu naga besar berwarna emas atau hijau dalam mimpi adalah pertanda keberuntungan agung. Naga dalam tradisi Nusantara melambangkan kekuatan alam semesta yang berpihak kepada Anda. Segala rencana besar akan mendapat kemudahan luar biasa.",
        "desc_en": "Meeting a large golden or green dragon in a dream is a sign of supreme good fortune. The dragon in Nusantara tradition symbolizes universal power aligning in your favor. All major plans will receive extraordinary ease."
    },
    {
        "cat_id": "Keberuntungan", "cat_en": "Luck",
        "keywords": ["bayi", "baby", "infant", "lahir", "birth", "anak kecil"],
        "title_id": "Bermimpi Menggendong Bayi Lucu", "title_en": "Dreaming of Holding a Cute Baby",
        "desc_id": "Menggendong bayi mungil yang lucu dan sehat dalam mimpi adalah pertanda sangat baik. Ini melambangkan awal yang baru, kreativitas yang lahir, keberhasilan proyek, atau berita bahagia tentang kelahiran atau jodoh dalam keluarga.",
        "desc_en": "Holding a cute and healthy baby in a dream is a very good omen. It symbolizes a fresh start, creativity being born, project success, or joyful news of a birth or new romantic connection in the family."
    },
    # ── CINTA & ASMARA / LOVE & ROMANCE ───────────────────────────────────────
    {
        "cat_id": "Cinta & Asmara", "cat_en": "Love & Romance",
        "keywords": ["pernikahan", "wedding", "nikah", "kawin", "menikah"],
        "title_id": "Bermimpi Menghadiri Pernikahan", "title_en": "Dreaming of Attending a Wedding",
        "desc_id": "Hadir dalam pesta pernikahan yang meriah dalam mimpi adalah pertanda kabar bahagia akan segera datang. Bagi yang belum menikah, ini pertanda jodoh semakin dekat. Bagi yang sudah menikah, hubungan akan semakin harmonis dan mesra.",
        "desc_en": "Attending a lively wedding celebration in a dream signals joyful news approaching. For the unmarried, it signals a soulmate drawing closer. For the married, the relationship will grow more harmonious and intimate."
    },
    {
        "cat_id": "Cinta & Asmara", "cat_en": "Love & Romance",
        "keywords": ["bertengkar", "fight", "cerai", "divorce", "marah", "angry"],
        "title_id": "Bermimpi Bertengkar dengan Pasangan", "title_en": "Dreaming of Fighting with Partner",
        "desc_id": "Mimpi bertengkar dengan pasangan justru sering memiliki arti positif dalam primbon: hubungan kalian akan semakin erat setelah badai berlalu. Namun ini juga ajakan untuk lebih terbuka berkomunikasi sebelum konflik kecil membesar.",
        "desc_en": "Dreaming of arguing with your partner often has a positive meaning in primbon: your relationship will grow stronger after the storm passes. However, it is also an invitation to communicate more openly before small conflicts escalate."
    },
    {
        "cat_id": "Cinta & Asmara", "cat_en": "Love & Romance",
        "keywords": ["mantan", "ex", "orang lama", "old flame", "kekasih lama"],
        "title_id": "Bermimpi Bertemu Mantan Kekasih", "title_en": "Dreaming of Meeting an Ex-Lover",
        "desc_id": "Bermimpi tentang mantan kekasih tidak selalu berarti masih ada perasaan tersisa. Dalam primbon, ini bisa jadi tanda bahwa ada luka batin masa lalu yang perlu Anda sembuhkan dan maafkan agar energi positif bisa mengalir bebas dalam hidup Anda.",
        "desc_en": "Dreaming of an ex-lover does not necessarily mean lingering feelings. In primbon, this may signal that there is a past emotional wound that you need to heal and forgive so that positive energy can flow freely in your life."
    },
    # ── KARIR & ILMU / CAREER & KNOWLEDGE ─────────────────────────────────────
    {
        "cat_id": "Karir & Ilmu", "cat_en": "Career & Knowledge",
        "keywords": ["ujian", "exam", "test", "sekolah", "school", "lulus", "pass", "buku"],
        "title_id": "Bermimpi Ujian atau Lulus Sekolah", "title_en": "Dreaming of Exams or Graduation",
        "desc_id": "Mimpi mengerjakan ujian dengan lancar dan lulus dengan nilai bagus adalah pertanda Anda akan berhasil melewati tantangan nyata yang sedang dihadapi. Kepercayaan diri Anda akan meningkat dan ilmu semakin bertambah.",
        "desc_en": "Dreaming of completing an exam successfully and passing with good grades signals that you will overcome real challenges you currently face. Your confidence will grow and your knowledge will expand."
    },
    {
        "cat_id": "Karir & Ilmu", "cat_en": "Career & Knowledge",
        "keywords": ["naik jabatan", "promotion", "jabatan baru", "kantor", "office", "bos", "boss"],
        "title_id": "Bermimpi Naik Jabatan atau Promosi", "title_en": "Dreaming of Promotion",
        "desc_id": "Bermimpi mendapatkan promosi atau jabatan baru adalah pertanda karir Anda akan mengalami lompatan luar biasa dalam waktu dekat. Tetaplah bekerja keras dan tunjukkan kemampuan terbaik Anda karena atasan sedang memperhatikan.",
        "desc_en": "Dreaming of receiving a promotion or new position signals that your career will experience an extraordinary leap soon. Keep working hard and showcasing your best abilities because superiors are watching."
    },
    # ── KEMATIAN & LELUHUR / DEATH & ANCESTORS ────────────────────────────────
    {
        "cat_id": "Leluhur & Kematian", "cat_en": "Ancestors & Death",
        "keywords": ["almarhum", "deceased", "orang mati", "dead", "kubur", "grave", "makam"],
        "title_id": "Bermimpi Bertemu Orang yang Sudah Meninggal", "title_en": "Dreaming of Deceased Person",
        "desc_id": "Dalam kepercayaan primbon, bermimpi didatangi orang yang sudah meninggal (terutama keluarga) adalah kunjungan spiritual nyata. Jika mereka tersenyum dan menyampaikan pesan, perhatikan kata-katanya. Jika mereka meminta sesuatu, segera tunaikan doa dan sedekah atas namanya.",
        "desc_en": "In primbon belief, dreaming of a deceased person (especially family) is an actual spiritual visitation. If they smile and deliver a message, pay close attention. If they request something, immediately offer prayers and charity in their name."
    },
    {
        "cat_id": "Leluhur & Kematian", "cat_en": "Ancestors & Death",
        "keywords": ["kematian sendiri", "own death", "mati", "meninggal", "wafat"],
        "title_id": "Bermimpi Diri Sendiri Meninggal", "title_en": "Dreaming of Your Own Death",
        "desc_id": "Bermimpi diri sendiri meninggal justru adalah pertanda yang sangat baik dalam primbon. Ini melambangkan akhir dari fase hidup yang lama dan awal dari fase baru yang jauh lebih cerah. Ibarat ulat yang berubah menjadi kupu-kupu — transformasi total sedang terjadi dalam hidup Anda.",
        "desc_en": "Dreaming of your own death is actually a very auspicious sign in primbon. It symbolizes the end of an old life phase and the beginning of a much brighter new one. Like a caterpillar transforming into a butterfly — a total transformation is happening in your life."
    },
]


# ==============================================================================
# SUB-VIEW: DASHBOARD
# ==============================================================================
class DashboardView(QWidget):
    def __init__(self, switch_page_callback, parent=None):
        super().__init__(parent)
        self.switch_page = switch_page_callback
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)
        
        # Left Panel: Mystical Interactive Orb
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        self.orb_card = QFrame()
        self.orb_card.setObjectName("OrbCard")
        self.orb_card.setProperty("class", "MysticCard")
        orb_card_layout = QVBoxLayout(self.orb_card)
        orb_card_layout.setAlignment(Qt.AlignCenter)
        
        self.crystal_orb = MysticCrystalOrb()
        self.crystal_orb.orb_clicked.connect(self.generate_orb_prediction)
        
        self.orb_title = QLabel()
        self.orb_title.setObjectName("OrbTitle")
        self.orb_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.orb_title.setStyleSheet("color: #FFD700;")
        self.orb_title.setAlignment(Qt.AlignCenter)
        
        self.orb_desc = QLabel()
        self.orb_desc.setWordWrap(True)
        self.orb_desc.setAlignment(Qt.AlignCenter)
        self.orb_desc.setStyleSheet("color: #9B98B0; font-size: 11px;")
        
        orb_card_layout.addWidget(self.orb_title)
        orb_card_layout.addWidget(self.crystal_orb)
        orb_card_layout.addWidget(self.orb_desc)
        
        left_layout.addWidget(self.orb_card, 3)
        
        # Quick Shortcuts widget underneath
        self.shortcuts_card = QFrame()
        self.shortcuts_card.setProperty("class", "MysticCard")
        shortcut_layout = QVBoxLayout(self.shortcuts_card)
        
        self.shortcut_title = QLabel()
        self.shortcut_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.shortcut_title.setStyleSheet("color: #FFD700;")
        shortcut_layout.addWidget(self.shortcut_title)
        
        btn_layout = QGridLayout()
        self.btn_goto_name = QPushButton()
        self.btn_goto_name.setProperty("class", "MysticButton")
        self.btn_goto_name.clicked.connect(lambda: self.switch_page(1))
        
        self.btn_goto_birth = QPushButton()
        self.btn_goto_birth.setProperty("class", "MysticButton")
        self.btn_goto_birth.clicked.connect(lambda: self.switch_page(2))
        
        self.btn_goto_compat = QPushButton()
        self.btn_goto_compat.setProperty("class", "MysticButton")
        self.btn_goto_compat.clicked.connect(lambda: self.switch_page(3))
        
        self.btn_goto_dream = QPushButton()
        self.btn_goto_dream.setProperty("class", "MysticButton")
        self.btn_goto_dream.clicked.connect(lambda: self.switch_page(5))
        
        btn_layout.addWidget(self.btn_goto_name, 0, 0)
        btn_layout.addWidget(self.btn_goto_birth, 0, 1)
        btn_layout.addWidget(self.btn_goto_compat, 1, 0)
        btn_layout.addWidget(self.btn_goto_dream, 1, 1)
        
        shortcut_layout.addLayout(btn_layout)
        left_layout.addWidget(self.shortcuts_card, 1)
        
        main_layout.addLayout(left_layout, 4)
        
        # Right Panel: Daily Fortune Insight and Cosmic Energies
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        
        # Crystal Message Box
        self.msg_card = QFrame()
        self.msg_card.setProperty("class", "MysticCard")
        msg_layout = QVBoxLayout(self.msg_card)
        
        self.msg_header = QLabel()
        self.msg_header.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.msg_header.setStyleSheet("color: #FFD700;")
        
        self.msg_body = QTextBrowser()
        self.msg_body.setStyleSheet("background: transparent; border: none; font-size: 13px; font-style: italic;")
        
        msg_layout.addWidget(self.msg_header)
        msg_layout.addWidget(self.msg_body)
        
        right_layout.addWidget(self.msg_card, 3)
        
        # Spiritual Energy Meter
        self.energy_card = QFrame()
        self.energy_card.setProperty("class", "MysticCard")
        energy_layout = QVBoxLayout(self.energy_card)
        
        self.energy_title = QLabel()
        self.energy_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.energy_title.setStyleSheet("color: #B19FFC;")
        energy_layout.addWidget(self.energy_title)
        
        # Energy Indicators
        self.energy1_lbl = QLabel("Aura")
        self.bar_energy1 = QProgressBar()
        self.bar_energy1.setRange(0, 100)
        self.bar_energy1.setValue(78)
        self.bar_energy1.setStyleSheet("""
            QProgressBar { border: 1px solid #432A70; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background-color: #8E44AD; }
        """)
        
        self.energy2_lbl = QLabel("Rezeki / Fortune")
        self.bar_energy2 = QProgressBar()
        self.bar_energy2.setRange(0, 100)
        self.bar_energy2.setValue(85)
        self.bar_energy2.setStyleSheet("""
            QProgressBar { border: 1px solid #432A70; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background-color: #D4AF37; }
        """)
        
        self.energy3_lbl = QLabel("Asmara / Harmony")
        self.bar_energy3 = QProgressBar()
        self.bar_energy3.setRange(0, 100)
        self.bar_energy3.setValue(64)
        self.bar_energy3.setStyleSheet("""
            QProgressBar { border: 1px solid #432A70; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background-color: #FF708C; }
        """)
        
        energy_layout.addWidget(self.energy1_lbl)
        energy_layout.addWidget(self.bar_energy1)
        energy_layout.addWidget(self.energy2_lbl)
        energy_layout.addWidget(self.bar_energy2)
        energy_layout.addWidget(self.energy3_lbl)
        energy_layout.addWidget(self.bar_energy3)
        
        right_layout.addWidget(self.energy_card, 2)
        main_layout.addLayout(right_layout, 5)
        
        self.retranslate()
        self.generate_orb_prediction()
        
    def retranslate(self):
        self.orb_title.setText(lang_mgr.get("app_title"))
        self.orb_desc.setText(lang_mgr.get("crystal_orb_desc"))
        self.shortcut_title.setText(lang_mgr.get("quick_tools"))
        
        self.btn_goto_name.setText(lang_mgr.get("name_analysis"))
        self.btn_goto_birth.setText(lang_mgr.get("birth_analysis"))
        self.btn_goto_compat.setText(lang_mgr.get("compatibility"))
        self.btn_goto_dream.setText(lang_mgr.get("dream_interpreter"))
        
        self.msg_header.setText(lang_mgr.get("daily_msg"))
        self.energy_title.setText(lang_mgr.get("energy_meter"))
        
    def generate_orb_prediction(self):
        # Rich expanded prediction pool — includes daily weton context
        today = datetime.date.today()
        weton_today = DestinyEngine.calculate_weton(today)
        day_id = weton_today['day_id']
        day_en = weton_today['day_en']
        pasaran = weton_today['pasaran']
        neptu = weton_today['neptu_total']

        cosmic_insights_id = [
            f"Energi kosmik Anda hari ini diselimuti <b>aura keemasan</b>. Hari yang luar biasa untuk melangkah maju dan menyelesaikan urusan tertunda.",
            f"Ada pertanda angin mengalir tenang membawa kedamaian sejati. Hindari perdebatan kecil hari ini agar rezeki spiritual Anda mengalir jernih seperti mata air pegunungan.",
            f"Kitab Primbon Jawa menunjukkan getaran tinggi pada elemen spiritual Anda. Inilah saat terbaik untuk menanam tekad, memperkuat hubungan keluarga, dan berfokus pada kesehatan batin.",
            f"Waspadai riak emosi yang bergolak. <b>Kesabaran adalah perisai mistis terkuat</b> Anda hari ini. Energi negatif dari luar tidak akan menembus aura Anda jika Anda tetap tenang.",
            f"Bintang timur menyinari jalan Anda. <b>Peluang emas tersembunyi</b> sedang menunggu di balik tirai rutinitas. Buka mata hati dan bersikaplah ramah kepada siapapun yang Anda temui hari ini.",
            f"Hari ini bertepatan dengan weton <b>{day_id} {pasaran}</b> (Neptu: {neptu}). Waktu yang sangat baik untuk memulai proyek baru, menandatangani kontrak, atau membangun relasi baru.",
            f"Sang Pencipta sedang membuka pintu rezeki yang selama ini tampak tertutup. Jangan lewatkan setiap kesempatan kecil — di situlah benih keajaiban hari ini tersembunyi.",
            f"Energi lunar sedang puncak-puncaknya. <b>Intuisi Anda sedang sangat tajam</b> — percayai insting pertama Anda dalam mengambil keputusan penting hari ini.",
            f"Leluhur Anda menjaga langkah Anda hari ini. Bersedekah atau berbagi kepada yang membutuhkan akan <b>melipatgandakan rezeki Anda</b> secara spiritual tiga kali lipat.",
            f"Elemen <b>{weton_today['element_id']}</b> mendominasi energi hari ini. Sesuaikan aktivitas Anda dengan kekuatan elemen ini untuk hasil yang maksimal.",
        ]
        cosmic_insights_en = [
            f"Your cosmic energy today is wrapped in a <b>golden aura</b>. An outstanding day to move forward and complete all outstanding matters.",
            f"A sign of wind flowing gently, bringing absolute peace. Avoid small debates today so your spiritual fortune stays as pure as a mountain spring.",
            f"The ancient Primbon archives reveal high resonance in your spiritual element. Perfect timing to ground your focus, strengthen family bonds, and nurture soul health.",
            f"Watch for turbulent emotional ripples. <b>Patience is your ultimate mystical shield</b> today. External negative energies cannot penetrate your aura if you remain centered.",
            f"The eastern star illuminates your path. A <b>hidden golden opportunity</b> waits behind the curtain of daily routine. Open your heart's eye and be kind to everyone you encounter.",
            f"Today aligns with the weton <b>{day_en} {pasaran}</b> (Neptu: {neptu}). Excellent timing for launching new projects, signing agreements, or establishing new relationships.",
            f"The Creator is opening doors of fortune that previously seemed sealed. Do not overlook small chances — within them lie the seeds of today's miracle.",
            f"Lunar energy is at its peak. <b>Your intuition is exceptionally sharp</b> — trust your first instinct when making important decisions today.",
            f"Your ancestors guard your every step today. Giving charity or sharing with those in need will <b>spiritually multiply your fortune</b> threefold.",
            f"The <b>{weton_today['element_en']}</b> element dominates today's energy. Align your activities with this elemental strength for maximum results.",
        ]
        
        # Adjust bar values dynamically based on today's neptu
        aura_val = min(98, 50 + neptu * 2 + random.randint(-8, 8))
        fortune_val = min(98, 45 + neptu * 3 + random.randint(-10, 10))
        love_val = min(98, 40 + neptu * 2 + random.randint(-12, 12))

        self.bar_energy1.setValue(max(30, aura_val))
        self.bar_energy2.setValue(max(30, fortune_val))
        self.bar_energy3.setValue(max(30, love_val))
        
        if lang_mgr.current_language == "id":
            chosen = random.choice(cosmic_insights_id)
            self.msg_body.setHtml(
                f"<p style='color:#9B98B0; font-size:11px;'>🗓️ Hari ini: <b style='color:#D4AF37;'>{day_id} {pasaran}</b> — Neptu: {neptu}</p>"
                f"<p style='font-style:italic; color:#E2E1E6;'>{chosen}</p>"
            )
        else:
            chosen = random.choice(cosmic_insights_en)
            self.msg_body.setHtml(
                f"<p style='color:#9B98B0; font-size:11px;'>🗓️ Today: <b style='color:#D4AF37;'>{day_en} {pasaran}</b> — Neptu: {neptu}</p>"
                f"<p style='font-style:italic; color:#E2E1E6;'>{chosen}</p>"
            )


# ==============================================================================
# SUB-VIEW: NAME ANALYSIS
# ==============================================================================
class NameAnalysisView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Title
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Input Form Card
        input_card = QFrame()
        input_card.setProperty("class", "MysticCard")
        form_layout = QVBoxLayout(input_card)
        
        self.lbl_enter_name = QLabel()
        form_layout.addWidget(self.lbl_enter_name)
        
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input)
        
        self.lbl_birth_date = QLabel()
        form_layout.addWidget(self.lbl_birth_date)
        
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate().addYears(-20))
        form_layout.addWidget(self.birth_date_input)
        
        # Buttons Layout
        btn_layout = QHBoxLayout()
        self.btn_analyze = QPushButton()
        self.btn_analyze.setProperty("class", "GoldButton")
        self.btn_analyze.clicked.connect(self.run_analysis)
        btn_layout.addWidget(self.btn_analyze)
        
        self.btn_reset = QPushButton()
        self.btn_reset.setProperty("class", "MysticButton")
        self.btn_reset.clicked.connect(self.reset_inputs)
        btn_layout.addWidget(self.btn_reset)
        
        form_layout.addLayout(btn_layout)
        layout.addWidget(input_card)
        
        # Output Card
        self.output_card = QFrame()
        self.output_card.setProperty("class", "MysticCard")
        output_layout = QVBoxLayout(self.output_card)
        
        self.output_text = QTextBrowser()
        output_layout.addWidget(self.output_text)
        
        # Save & Export layout
        action_layout = QHBoxLayout()
        self.btn_save = QPushButton()
        self.btn_save.setProperty("class", "MysticButton")
        self.btn_save.clicked.connect(self.save_action)
        action_layout.addWidget(self.btn_save)
        
        self.btn_export = QPushButton()
        self.btn_export.setProperty("class", "MysticButton")
        self.btn_export.clicked.connect(self.export_action)
        action_layout.addWidget(self.btn_export)
        
        output_layout.addLayout(action_layout)
        layout.addWidget(self.output_card)
        
        self.retranslate()
        self.reset_inputs()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("name_analysis"))
        self.lbl_enter_name.setText(lang_mgr.get("name_input_placeholder"))
        self.lbl_birth_date.setText(lang_mgr.get("birth_date"))
        self.btn_analyze.setText(lang_mgr.get("analyze_btn"))
        self.btn_reset.setText(lang_mgr.get("reset"))
        self.btn_save.setText(lang_mgr.get("save_history"))
        self.btn_export.setText(lang_mgr.get("export_pdf"))
        
    def run_analysis(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Macan Peramal", "Mohon masukkan nama terlebih dahulu.")
            return
            
        qdate = self.birth_date_input.date()
        birth_date = datetime.date(qdate.year(), qdate.month(), qdate.day())
        
        num_res = DestinyEngine.calculate_numerology(name, birth_date)
        weton_res = DestinyEngine.calculate_weton(birth_date)
        
        # Formulate enriched HTML report
        if lang_mgr.current_language == "id":
            lp = num_res['lp_desc_id']
            dd = num_res['dest_desc_id']
            sd = num_res['soul_desc_id']
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">✦ Kidung Jejak Takdir ✦</h2>
            <h3 style="color: #D4AF37; text-align: center;">{name}</h3>
            <hr style="border: 0.5px solid #432A70;" />

            <h3 style="color:#A259FF;">① Angka Jalan Hidup (Life Path): {num_res['life_path']} — {lp['title']}</h3>
            <p>{lp['desc']}</p>
            <p>🎨 <b>Warna Keberuntungan:</b> {lp['lucky_color']} &nbsp;|&nbsp;
               💎 <b>Batu Keberuntungan:</b> {lp['lucky_gem']}</p>
            <p>📅 <b>Hari Terbaik:</b> {lp['best_day']}</p>
            <p>⚔️ <b>Tantangan Jiwa:</b> {lp['challenge']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#D4AF37;">② Angka Takdir (Destiny): {num_res['destiny']} — {dd['title']}</h3>
            <p>{dd['desc']}</p>
            <p>🎨 <b>Warna Keberuntungan:</b> {dd['lucky_color']} &nbsp;|&nbsp;
               💎 <b>Batu Keberuntungan:</b> {dd['lucky_gem']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FF708C;">③ Angka Hasrat Jiwa (Soul Urge): {num_res['soul_urge']} — {sd['title']}</h3>
            <p>{sd['desc']}</p>
            <p>⚔️ <b>Tantangan Jiwa:</b> {sd['challenge']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#00B4D8;">④ Weton Kelahiran Jawa</h3>
            <p>🗓️ <b>Weton Anda:</b> <span style="font-size:15px; color:#00B4D8;">{weton_res['day_id']} {weton_res['pasaran']}</span></p>
            <p>🔢 <b>Neptu Hari:</b> {weton_res['neptu_day']} + <b>Neptu Pasaran:</b> {weton_res['neptu_pasaran']} = <b>Total: {weton_res['neptu_total']}</b></p>
            <p>🌿 <b>Elemen Spiritual:</b> {weton_res['element_id']}</p>
            <p>🧬 <b>Karakter Spiritual Nusantara:</b> {weton_res['traits_id']}</p>
            <p>💼 <b>Rekomendasi Karier:</b> {weton_res['career_id']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#7ECFB3;">⑤ Rangkuman Kosmik</h3>
            <p>🍀 <b>Kombinasi Angka Keberuntungan:</b> {', '.join(map(str, num_res['lucky_nums']))}</p>
            <p>🔮 <b>Angka Kepribadian:</b> {num_res['personality']}</p>
            <p style="color:#8C84A9; font-size:11px; font-style:italic; margin-top:15px;">
            ✦ Laporan ini dihasilkan berdasarkan Primbon Jawa & sistem Numerologi Pythagorean. 
            Macan Peramal © 2026 Macan Angkasa ✦</p>
            """
        else:
            lp = num_res['lp_desc_en']
            dd = num_res['dest_desc_en']
            sd = num_res['soul_desc_en']
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">✦ Footprints of Destiny ✦</h2>
            <h3 style="color: #D4AF37; text-align: center;">{name}</h3>
            <hr style="border: 0.5px solid #432A70;" />

            <h3 style="color:#A259FF;">① Life Path Number: {num_res['life_path']} — {lp['title']}</h3>
            <p>{lp['desc']}</p>
            <p>🎨 <b>Lucky Color:</b> {lp['lucky_color']} &nbsp;|&nbsp;
               💎 <b>Lucky Gem:</b> {lp['lucky_gem']}</p>
            <p>📅 <b>Best Days:</b> {lp['best_day']}</p>
            <p>⚔️ <b>Soul Challenge:</b> {lp['challenge']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#D4AF37;">② Destiny Number: {num_res['destiny']} — {dd['title']}</h3>
            <p>{dd['desc']}</p>
            <p>🎨 <b>Lucky Color:</b> {dd['lucky_color']} &nbsp;|&nbsp;
               💎 <b>Lucky Gem:</b> {dd['lucky_gem']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FF708C;">③ Soul Urge Number: {num_res['soul_urge']} — {sd['title']}</h3>
            <p>{sd['desc']}</p>
            <p>⚔️ <b>Soul Challenge:</b> {sd['challenge']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#00B4D8;">④ Javanese Weton Birth</h3>
            <p>🗓️ <b>Your Weton:</b> <span style="font-size:15px; color:#00B4D8;">{weton_res['day_en']} {weton_res['pasaran']}</span></p>
            <p>🔢 <b>Day Neptu:</b> {weton_res['neptu_day']} + <b>Pasaran Neptu:</b> {weton_res['neptu_pasaran']} = <b>Total: {weton_res['neptu_total']}</b></p>
            <p>🌿 <b>Spiritual Element:</b> {weton_res['element_en']}</p>
            <p>🧬 <b>Nusantara Spiritual Character:</b> {weton_res['traits_en']}</p>
            <p>💼 <b>Career Recommendation:</b> {weton_res['career_en']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#7ECFB3;">⑤ Cosmic Summary</h3>
            <p>🍀 <b>Lucky Number Combination:</b> {', '.join(map(str, num_res['lucky_nums']))}</p>
            <p>🔮 <b>Personality Number:</b> {num_res['personality']}</p>
            <p style="color:#8C84A9; font-size:11px; font-style:italic; margin-top:15px;">
            ✦ This report is generated based on Javanese Primbon &amp; Pythagorean Numerology.
            Macan Peramal © 2026 Macan Angkasa ✦</p>
            """
        self.output_text.setHtml(html)
        
    def reset_inputs(self):
        self.name_input.clear()
        self.birth_date_input.setDate(QDate.currentDate().addYears(-20))
        self.output_text.setHtml("<p style='color:#8C84A9; font-style:italic; text-align:center;'>Hasil ramalan nama akan tercatat di sini...</p>")
        
    def save_action(self):
        name = self.name_input.text().strip()
        if not name:
            return
        QMessageBox.information(self, "Macan Peramal", lang_mgr.get("history_saved"))
        
    def export_action(self):
        name = self.name_input.text().strip()
        if not name:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Simpan Laporan", f"Ramalan_Nama_{name}.html", "HTML Files (*.html)")
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.output_text.toHtml())
            QMessageBox.information(self, "Macan Peramal", lang_mgr.get("export_success") + filepath)


# ==============================================================================
# SUB-VIEW: BIRTH DATE ANALYSIS
# ==============================================================================
class BirthAnalysisView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        input_card = QFrame()
        input_card.setProperty("class", "MysticCard")
        form_layout = QVBoxLayout(input_card)
        
        self.lbl_birth_date = QLabel()
        form_layout.addWidget(self.lbl_birth_date)
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form_layout.addWidget(self.date_input)
        
        btn_layout = QHBoxLayout()
        self.btn_calc = QPushButton()
        self.btn_calc.setProperty("class", "GoldButton")
        self.btn_calc.clicked.connect(self.run_analysis)
        btn_layout.addWidget(self.btn_calc)
        
        self.btn_reset = QPushButton()
        self.btn_reset.setProperty("class", "MysticButton")
        self.btn_reset.clicked.connect(self.reset_ui)
        btn_layout.addWidget(self.btn_reset)
        
        form_layout.addLayout(btn_layout)
        layout.addWidget(input_card)
        
        # Results Output
        self.results_card = QFrame()
        self.results_card.setProperty("class", "MysticCard")
        res_layout = QVBoxLayout(self.results_card)
        
        self.results_text = QTextBrowser()
        res_layout.addWidget(self.results_text)
        
        layout.addWidget(self.results_card)
        self.retranslate()
        self.reset_ui()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("birth_analysis"))
        self.lbl_birth_date.setText(lang_mgr.get("birth_date"))
        self.btn_calc.setText(lang_mgr.get("analyze_btn"))
        self.btn_reset.setText(lang_mgr.get("reset"))
        
    def run_analysis(self):
        qdate = self.date_input.date()
        birth_date = datetime.date(qdate.year(), qdate.month(), qdate.day())
        weton = DestinyEngine.calculate_weton(birth_date)
        
        # Determine Shio from birth year
        shio_cycle_id = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
                          "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"]
        shio_cycle_en = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
                          "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
        shio_idx = (birth_date.year - 1900) % 12
        shio_id = shio_cycle_id[shio_idx]
        shio_en = shio_cycle_en[shio_idx]

        # Weton-specific taboos (pantangan) – keyed by "DayPasaran"
        PANTANGAN = {
            "Jumat Kliwon": {
                "id": "Hindari memulai perjalanan jauh. Jangan melakukan transaksi besar. Utamakan ibadah dan doa pada malam ini.",
                "en": "Avoid starting long journeys. Refrain from major financial transactions. Prioritize prayer and worship this night."
            },
            "Selasa Kliwon": {
                "id": "Hindari konfrontasi fisik. Jangan membangun atau membeli rumah pada hari ini. Kurangi keluar malam.",
                "en": "Avoid physical confrontations. Refrain from building or purchasing property today. Minimize going out at night."
            },
            "Rabu Wage": {
                "id": "Hindari membuat keputusan besar secara tergesa-gesa. Jangan meminjam atau meminjamkan uang hari ini.",
                "en": "Avoid rushing into major decisions. Refrain from lending or borrowing money today."
            },
        }
        weton_key = f"{weton['day_id']} {weton['pasaran']}"
        pantangan_id = PANTANGAN.get(weton_key, {}).get("id", "Tidak ada pantangan khusus tercatat untuk weton ini. Tetaplah berhati-hati dan perbanyak doa.")
        pantangan_en = PANTANGAN.get(weton_key, {}).get("en", "No specific taboos recorded for this weton. Stay cautious and increase prayers.")

        # Ritual saran berdasarkan elemen
        RITUAL_ID = {
            "Bumi / Tanah": "Lakukan meditasi duduk di atas tanah terbuka setiap pagi. Tanam bunga atau pohon sebagai wujud syukur. Sedekah makanan kepada yang membutuhkan.",
            "Angin / Udara": "Lakukan pernapasan dalam di udara terbuka saat fajar. Tulis jurnal harian sebagai saluran ekspresi. Banyak-banyak berdoa di tempat tinggi.",
            "Api": "Nyalakan lilin atau dupa saat berdoa untuk memfokuskan energi. Olahraga rutin pagi hari sangat dianjurkan. Hindari amarah saat matahari terbenam.",
            "Samudra / Air": "Rendam kaki dalam air garam hangat setiap Jumat malam. Sering-seringlah duduk dekat sumber air (sungai, laut) untuk menyerap energinya."
        }
        RITUAL_EN = {
            "Earth / Ground": "Meditate sitting on open ground each morning. Plant flowers or trees as an act of gratitude. Give food charity to those in need.",
            "Wind / Air": "Practice deep breathing in open air at dawn. Keep a daily journal as an expressive outlet. Pray often in high, open places.",
            "Fire": "Light a candle or incense when praying to focus energy. Daily morning exercise is highly advised. Avoid anger at sunset.",
            "Water / Ocean": "Soak your feet in warm salted water every Friday evening. Sit near water sources (rivers, sea) regularly to absorb their energy."
        }
        ritual_id = RITUAL_ID.get(weton['element_id'], "Perbanyak doa dan sedekah untuk menjaga keseimbangan spiritual.")
        ritual_en = RITUAL_EN.get(weton['element_en'], "Increase prayers and charity to maintain spiritual balance.")

        if lang_mgr.current_language == "id":
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">✦ Perhitungan Kitab Weton Nusantara ✦</h2>
            <h3 style="color:#D4AF37; text-align:center;">Tanggal Lahir: {birth_date.strftime('%d %B %Y')}</h3>
            <hr style="border: 0.5px solid #432A70;" />

            <h3 style="color:#A259FF;">① Data Weton</h3>
            <table width="100%" cellpadding="5" style="font-size: 13px; color: #D2CFDF;">
                <tr><td width="45%"><b>🗓️ Hari Kelahiran:</b></td><td><span style="color:#FF708C; font-size:14px;">{weton['day_id']}</span> &nbsp; (Neptu: <b>{weton['neptu_day']}</b>)</td></tr>
                <tr><td><b>🔴 Pasaran Jawa:</b></td><td><span style="color:#00B4D8; font-size:14px;">{weton['pasaran']}</span> &nbsp; (Neptu: <b>{weton['neptu_pasaran']}</b>)</td></tr>
                <tr><td><b>🔢 Jumlah Neptu Total:</b></td><td><span style="color:#D4AF37; font-size:17px; font-weight:bold;">{weton['neptu_total']}</span></td></tr>
                <tr><td><b>🌿 Elemen Spiritual:</b></td><td><span style="color:#A259FF; font-weight:bold;">{weton['element_id']}</span></td></tr>
                <tr><td><b>🐉 Shio Tionghoa:</b></td><td><span style="color:#7ECFB3; font-weight:bold;">{shio_id}</span> ({birth_date.year})</td></tr>
            </table>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FFD700;">② Sifat & Kepribadian Tradisional</h3>
            <p>{weton['traits_id']}</p>

            <h3 style="color:#FFD700;">③ Karier & Rezeki yang Selaras</h3>
            <p>Berdasarkan Kitab Primbon Jawa kuno, bidang yang paling selaras dan lancar rezekinya bagi weton <b>{weton['day_id']} {weton['pasaran']}</b> adalah:</p>
            <p style="color:#D4AF37; font-size:14px; font-weight:bold;">🏆 {weton['career_id']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FF708C;">④ Pantangan & Larangan Weton</h3>
            <p>⚠️ {pantangan_id}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#7ECFB3;">⑤ Saran Ritual & Laku Spiritual</h3>
            <p>🕯️ {ritual_id}</p>

            <p style="color:#8C84A9; font-size:11px; font-style:italic; margin-top:15px;">
            ✦ Laporan ini dihasilkan berdasarkan Kitab Primbon Jawa & Tradisi Nusantara.
            Macan Peramal © 2026 Macan Angkasa ✦</p>
            """
        else:
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">✦ Archipelago Weton Computations ✦</h2>
            <h3 style="color:#D4AF37; text-align:center;">Birth Date: {birth_date.strftime('%B %d, %Y')}</h3>
            <hr style="border: 0.5px solid #432A70;" />

            <h3 style="color:#A259FF;">① Weton Data</h3>
            <table width="100%" cellpadding="5" style="font-size: 13px; color: #D2CFDF;">
                <tr><td width="45%"><b>🗓️ Birth Day:</b></td><td><span style="color:#FF708C; font-size:14px;">{weton['day_en']}</span> &nbsp; (Neptu: <b>{weton['neptu_day']}</b>)</td></tr>
                <tr><td><b>🔴 Javanese Pasaran:</b></td><td><span style="color:#00B4D8; font-size:14px;">{weton['pasaran']}</span> &nbsp; (Neptu: <b>{weton['neptu_pasaran']}</b>)</td></tr>
                <tr><td><b>🔢 Total Neptu Score:</b></td><td><span style="color:#D4AF37; font-size:17px; font-weight:bold;">{weton['neptu_total']}</span></td></tr>
                <tr><td><b>🌿 Spiritual Element:</b></td><td><span style="color:#A259FF; font-weight:bold;">{weton['element_en']}</span></td></tr>
                <tr><td><b>🐉 Chinese Zodiac (Shio):</b></td><td><span style="color:#7ECFB3; font-weight:bold;">{shio_en}</span> ({birth_date.year})</td></tr>
            </table>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FFD700;">② Traditional Character Insights</h3>
            <p>{weton['traits_en']}</p>

            <h3 style="color:#FFD700;">③ Harmonious Career & Prosperity Path</h3>
            <p>According to ancient Javanese Primbon archives, the most aligned and prosperous professional fields for <b>{weton['day_en']} {weton['pasaran']}</b> are:</p>
            <p style="color:#D4AF37; font-size:14px; font-weight:bold;">🏆 {weton['career_en']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FF708C;">④ Weton Taboos & Warnings</h3>
            <p>⚠️ {pantangan_en}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#7ECFB3;">⑤ Ritual & Spiritual Practice Advice</h3>
            <p>🕯️ {ritual_en}</p>

            <p style="color:#8C84A9; font-size:11px; font-style:italic; margin-top:15px;">
            ✦ This report is generated based on Javanese Primbon &amp; Archipelago Traditions.
            Macan Peramal © 2026 Macan Angkasa ✦</p>
            """
        self.results_text.setHtml(html)
        
    def reset_ui(self):
        self.date_input.setDate(QDate.currentDate())
        self.results_text.setHtml("<p style='color:#8C84A9; font-style:italic; text-align:center;'>Hasil perhitungan pasaran Jawa akan tertera di sini...</p>")


# ==============================================================================
# SUB-VIEW: COMPATIBILITY CALCULATOR
# ==============================================================================
class CompatibilityView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Dual Inputs Card
        inputs_card = QFrame()
        inputs_card.setProperty("class", "MysticCard")
        grid_layout = QGridLayout(inputs_card)
        
        # Partner 1
        self.lbl_p1 = QLabel("<b>Profile 1 (Anda)</b>")
        self.lbl_p1.setStyleSheet("color:#FFD700; font-size: 13px;")
        grid_layout.addWidget(self.lbl_p1, 0, 0, 1, 2)
        
        self.lbl_p1_name = QLabel("Nama Lengkap:")
        self.p1_name_input = QLineEdit()
        grid_layout.addWidget(self.lbl_p1_name, 1, 0)
        grid_layout.addWidget(self.p1_name_input, 1, 1)
        
        self.lbl_p1_date = QLabel("Tanggal Lahir:")
        self.p1_date_input = QDateEdit()
        self.p1_date_input.setCalendarPopup(True)
        self.p1_date_input.setDate(QDate.currentDate().addYears(-22))
        grid_layout.addWidget(self.lbl_p1_date, 2, 0)
        grid_layout.addWidget(self.p1_date_input, 2, 1)
        
        # Partner 2
        self.lbl_p2 = QLabel("<b>Profile 2 (Pasangan / Rekan)</b>")
        self.lbl_p2.setStyleSheet("color:#FFD700; font-size: 13px;")
        grid_layout.addWidget(self.lbl_p2, 3, 0, 1, 2)
        
        self.lbl_p2_name = QLabel("Nama Lengkap:")
        self.p2_name_input = QLineEdit()
        grid_layout.addWidget(self.lbl_p2_name, 4, 0)
        grid_layout.addWidget(self.p2_name_input, 4, 1)
        
        self.lbl_p2_date = QLabel("Tanggal Lahir:")
        self.p2_date_input = QDateEdit()
        self.p2_date_input.setCalendarPopup(True)
        self.p2_date_input.setDate(QDate.currentDate().addYears(-21))
        grid_layout.addWidget(self.lbl_p2_date, 5, 0)
        grid_layout.addWidget(self.p2_date_input, 5, 1)
        
        # Category Selector
        self.lbl_rel_type = QLabel("Tipe Hubungan:")
        self.combo_rel_type = QComboBox()
        self.combo_rel_type.addItem("Asmara / Couple")
        self.combo_rel_type.addItem("Rekan Bisnis / Business")
        self.combo_rel_type.addItem("Persahabatan / Friendship")
        grid_layout.addWidget(self.lbl_rel_type, 6, 0)
        grid_layout.addWidget(self.combo_rel_type, 6, 1)
        
        # Action Button
        self.btn_compat = QPushButton()
        self.btn_compat.setProperty("class", "GoldButton")
        self.btn_compat.clicked.connect(self.calculate_compatibility)
        grid_layout.addWidget(self.btn_compat, 7, 0, 1, 2)
        
        layout.addWidget(inputs_card)
        
        # Output Card
        self.out_card = QFrame()
        self.out_card.setProperty("class", "MysticCard")
        out_layout = QVBoxLayout(self.out_card)
        
        self.out_text = QTextBrowser()
        out_layout.addWidget(self.out_text)
        
        layout.addWidget(self.out_card)
        self.retranslate()
        self.clear_ui()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("compatibility"))
        self.btn_compat.setText(lang_mgr.get("analyze_compat"))
        
    def calculate_compatibility(self):
        name1 = self.p1_name_input.text().strip()
        name2 = self.p2_name_input.text().strip()
        
        if not name1 or not name2:
            QMessageBox.warning(self, "Macan Peramal", "Silakan lengkapi kedua nama profil.")
            return
            
        qd1 = self.p1_date_input.date()
        qd2 = self.p2_date_input.date()
        
        d1 = datetime.date(qd1.year(), qd1.month(), qd1.day())
        d2 = datetime.date(qd2.year(), qd2.month(), qd2.day())
        
        res = DestinyEngine.calculate_compatibility(name1, d1, name2, d2)
        
        if lang_mgr.current_language == "id":
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">Hasil Analisa Kompatibilitas</h2>
            <hr style="border: 0.5px solid #432A70;" />
            <h1 style="color:#FF708C; text-align:center; margin:0; font-size:48px;">{res['score']}%</h1>
            <p style="text-align:center; font-style:italic;">Harmoni Energi Spiritual</p>
            <table width="100%" style="font-size: 13px; color: #D2CFDF; margin-top:10px;">
                <tr><td><b>Weton Anda:</b></td><td>{res['p1_weton']} (Neptu: {res['p1_neptu']})</td></tr>
                <tr><td><b>Weton Pasangan:</b></td><td>{res['p2_weton']} (Neptu: {res['p2_neptu']})</td></tr>
                <tr><td><b>Kategori Primbon:</b></td><td><span style="color:#FFD700; font-weight:bold;">{res['category_id']}</span></td></tr>
            </table>
            <br />
            <p><b>Makna Hubungan:</b> {res['desc_id']}</p>
            """
        else:
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">Compatibility Analysis Results</h2>
            <hr style="border: 0.5px solid #432A70;" />
            <h1 style="color:#FF708C; text-align:center; margin:0; font-size:48px;">{res['score']}%</h1>
            <p style="text-align:center; font-style:italic;">Spiritual Energy Harmony</p>
            <table width="100%" style="font-size: 13px; color: #D2CFDF; margin-top:10px;">
                <tr><td><b>Your Weton:</b></td><td>{res['p1_weton']} (Neptu: {res['p1_neptu']})</td></tr>
                <tr><td><b>Partner's Weton:</b></td><td>{res['p2_weton']} (Neptu: {res['p2_neptu']})</td></tr>
                <tr><td><b>Primbon Category:</b></td><td><span style="color:#FFD700; font-weight:bold;">{res['category_en']}</span></td></tr>
            </table>
            <br />
            <p><b>Relationship Dynamics:</b> {res['desc_en']}</p>
            """
        self.out_text.setHtml(html)
        
    def clear_ui(self):
        self.p1_name_input.clear()
        self.p2_name_input.clear()
        self.out_text.setHtml("<p style='color:#8C84A9; font-style:italic; text-align:center;'>Hasil komparasi aura hubungan Anda akan tampil di sini...</p>")


# ==============================================================================
# SUB-VIEW: NUMEROLOGY CENTER
# ==============================================================================
class NumerologyView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Interactive Numerology Search Box
        form_card = QFrame()
        form_card.setProperty("class", "MysticCard")
        form_layout = QVBoxLayout(form_card)
        
        self.lbl_name_num = QLabel("Nama Lengkap:")
        form_layout.addWidget(self.lbl_name_num)
        
        self.input_name_num = QLineEdit()
        form_layout.addWidget(self.input_name_num)
        
        self.lbl_date_num = QLabel("Tanggal Lahir:")
        form_layout.addWidget(self.lbl_date_num)
        
        self.input_date_num = QDateEdit()
        self.input_date_num.setCalendarPopup(True)
        form_layout.addWidget(self.input_date_num)
        
        self.btn_num = QPushButton()
        self.btn_num.setProperty("class", "GoldButton")
        self.btn_num.clicked.connect(self.calculate_numerology)
        form_layout.addWidget(self.btn_num)
        
        layout.addWidget(form_card)
        
        # Result Details Display
        result_card = QFrame()
        result_card.setProperty("class", "MysticCard")
        res_layout = QVBoxLayout(result_card)
        
        self.output_browser = QTextBrowser()
        res_layout.addWidget(self.output_browser)
        layout.addWidget(result_card)
        
        self.retranslate()
        self.clear_ui()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("numerology"))
        self.btn_num.setText(lang_mgr.get("calculate"))
        
    def calculate_numerology(self):
        name = self.input_name_num.text().strip()
        if not name:
            QMessageBox.warning(self, "Macan Peramal", "Silakan isi nama lengkap untuk numerologi.")
            return
            
        qd = self.input_date_num.date()
        date_birth = datetime.date(qd.year(), qd.month(), qd.day())
        
        nums = DestinyEngine.calculate_numerology(name, date_birth)
        
        # Interpret numbers
        paths_id = {
            1: "Sang Pemimpin Pionir: Penuh ambisi, memiliki inisiatif tinggi, mandiri, dan berani memulai babak baru.",
            2: "Sang Diplomat Pembuat Damai: Peka terhadap harmoni sosial, penyayang, senang bekerja sama, dan intuitif.",
            3: "Sang Komunikator Kreatif: Ekspresif, berjiwa seni tinggi, membawa kegembiraan bagi lingkungan sekitar.",
            4: "Sang Pembangun Fondasi: Terstruktur, berdedikasi tinggi, praktis, disiplin, dan sangat andal.",
            5: "Sang Petualang Dinamis: Menyukai kebebasan, fleksibel, gemar menjelajahi hal baru dan dinamis.",
            6: "Sang Pengasuh Harmonis: Bertanggung jawab, mencintai keluarga, berjiwa penolong, dan penyembuh alami.",
            7: "Sang Pencari Kebenaran Spiritual: Analitis, introspektif, gemar mempelajari hal esoteris, misterius.",
            8: "Sang Eksekutif Sukses: Berorientasi pada kesuksesan finansial, berwibawa, handal mengelola organisasi.",
            9: "Sang Humanis Sejati: Idealis, berpikiran luas, rela berkorban untuk kesejahteraan umat manusia secara global."
        }
        paths_en = {
            1: "The Pioneer Leader: Ambitious, highly proactive, extremely independent, and courageous in opening new horizons.",
            2: "The Harmonious Peacemaker: Extremely sensitive to public dynamics, highly collaborative, compassionate, and intuitive.",
            3: "The Creative Communicator: Expressive, artistic spirit, naturally bringing joy and radiant light into any room.",
            4: "The Structural Builder: Practical, disciplined, highly dependable, focused on long-term systemic stability.",
            5: "The Free-spirited Catalyst: Adaptable, dynamic explorer, thriving in diverse changes and personal freedom.",
            6: "The Nurturer: Responsible, deeply attached to family, healing nature, and a persistent provider.",
            7: "The Spiritual Researcher: Deeply analytical, quiet, drawn to mysteries, philosophy, and esoterics.",
            8: "The Authoritative Achiever: Focus on practical success, organizational execution, business wisdom, and legacy.",
            9: "The Compassionate Humanitarian: Boundless idealist, global thinker, dedicated to selflessly helping humanity."
        }
        
        # Handle Master Numbers (11, 22, 33)
        paths_id[11] = "Angka Master 11 (Pembawa Visi Mistis): Memiliki intuisi luar biasa, menjadi jembatan spiritual, dan inspiratif."
        paths_id[22] = "Angka Master 22 (Sang Pembangun Agung): Mampu merealisasikan impian spiritual terbesar menjadi kenyataan fisik."
        paths_id[33] = "Angka Master 33 (Guru Cinta Kasih Global): Pengorbanan tinggi demi mencerahkan kesadaran spiritual umat manusia."
        
        paths_en[11] = "Master Number 11 (The Spiritual Visionary): Profound intuitive channel, inspirational leader, connecting cosmic dimensions."
        paths_en[22] = "Master Number 22 (The Master Architect): Translates grand abstract dreams into concrete, global material reality."
        paths_en[33] = "Master Number 33 (The Master Teacher): Sacrifices selflessly to elevate spiritual awareness and unconditional love globally."
        
        path_desc_id = paths_id.get(nums["life_path"], "Kombinasi energi unik yang misterius.")
        path_desc_en = paths_en.get(nums["life_path"], "A unique and profoundly mysterious vibration combo.")
        
        if lang_mgr.current_language == "id":
            lp = nums['lp_desc_id']
            dd = nums['dest_desc_id']
            sd = nums['soul_desc_id']
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">✦ Profil Getaran Angka Pythagorean ✦</h2>
            <hr style="border: 0.5px solid #432A70;" />
            <table width="100%" cellpadding="4" style="font-size: 13px; color: #D2CFDF; margin-bottom:10px;">
                <tr><td width="55%"><b>🔮 Angka Jalan Hidup (Life Path):</b></td><td><span style="color:#A259FF; font-size:15px; font-weight:bold;">{nums['life_path']} — {lp['title']}</span></td></tr>
                <tr><td><b>⭐ Angka Takdir (Destiny):</b></td><td><span style="color:#D4AF37; font-size:15px; font-weight:bold;">{nums['destiny']} — {dd['title']}</span></td></tr>
                <tr><td><b>💜 Angka Hasrat Jiwa (Soul Urge):</b></td><td><span style="color:#FF708C; font-size:15px; font-weight:bold;">{nums['soul_urge']} — {sd['title']}</span></td></tr>
                <tr><td><b>🎭 Angka Kepribadian:</b></td><td><span style="color:#00B4D8; font-weight:bold;">{nums['personality']}</span></td></tr>
                <tr><td><b>🍀 Angka Keberuntungan:</b></td><td><span style="color:#7ECFB3; font-weight:bold;">{', '.join(map(str, nums['lucky_nums']))}</span></td></tr>
            </table>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#A259FF;">Jalan Hidup {nums['life_path']} — {lp['title']}</h3>
            <p style="line-height:1.7;">{lp['desc']}</p>
            <p>🎨 <b>Warna Hoki:</b> {lp['lucky_color']} &nbsp;|&nbsp; 💎 <b>Batu Jimat:</b> {lp['lucky_gem']} &nbsp;|&nbsp; 📅 <b>Hari Terbaik:</b> {lp['best_day']}</p>
            <p>⚔️ <b>Tantangan Hidup:</b> {lp['challenge']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#D4AF37;">Angka Takdir {nums['destiny']} — {dd['title']}</h3>
            <p style="line-height:1.7;">{dd['desc']}</p>
            <p>🎨 <b>Warna Hoki:</b> {dd['lucky_color']} &nbsp;|&nbsp; 💎 <b>Batu Jimat:</b> {dd['lucky_gem']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FF708C;">Hasrat Jiwa {nums['soul_urge']} — {sd['title']}</h3>
            <p style="line-height:1.7;">{sd['desc']}</p>
            <p>⚔️ <b>Tantangan Jiwa:</b> {sd['challenge']}</p>
            <p style="color:#8C84A9; font-size:11px; font-style:italic; margin-top:12px;">
            ✦ Macan Peramal © 2026 Macan Angkasa — Sistem Numerologi Pythagorean ✦</p>
            """
        else:
            lp = nums['lp_desc_en']
            dd = nums['dest_desc_en']
            sd = nums['soul_desc_en']
            html = f"""
            <h2 style="color: #FFD700; text-align: center;">✦ Pythagorean Numerology Portrait ✦</h2>
            <hr style="border: 0.5px solid #432A70;" />
            <table width="100%" cellpadding="4" style="font-size: 13px; color: #D2CFDF; margin-bottom:10px;">
                <tr><td width="55%"><b>🔮 Life Path Number:</b></td><td><span style="color:#A259FF; font-size:15px; font-weight:bold;">{nums['life_path']} — {lp['title']}</span></td></tr>
                <tr><td><b>⭐ Destiny Number:</b></td><td><span style="color:#D4AF37; font-size:15px; font-weight:bold;">{nums['destiny']} — {dd['title']}</span></td></tr>
                <tr><td><b>💜 Soul Urge Number:</b></td><td><span style="color:#FF708C; font-size:15px; font-weight:bold;">{nums['soul_urge']} — {sd['title']}</span></td></tr>
                <tr><td><b>🎭 Personality Number:</b></td><td><span style="color:#00B4D8; font-weight:bold;">{nums['personality']}</span></td></tr>
                <tr><td><b>🍀 Lucky Numbers:</b></td><td><span style="color:#7ECFB3; font-weight:bold;">{', '.join(map(str, nums['lucky_nums']))}</span></td></tr>
            </table>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#A259FF;">Life Path {nums['life_path']} — {lp['title']}</h3>
            <p style="line-height:1.7;">{lp['desc']}</p>
            <p>🎨 <b>Lucky Color:</b> {lp['lucky_color']} &nbsp;|&nbsp; 💎 <b>Lucky Gem:</b> {lp['lucky_gem']} &nbsp;|&nbsp; 📅 <b>Best Days:</b> {lp['best_day']}</p>
            <p>⚔️ <b>Life Challenge:</b> {lp['challenge']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#D4AF37;">Destiny {nums['destiny']} — {dd['title']}</h3>
            <p style="line-height:1.7;">{dd['desc']}</p>
            <p>🎨 <b>Lucky Color:</b> {dd['lucky_color']} &nbsp;|&nbsp; 💎 <b>Lucky Gem:</b> {dd['lucky_gem']}</p>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FF708C;">Soul Urge {nums['soul_urge']} — {sd['title']}</h3>
            <p style="line-height:1.7;">{sd['desc']}</p>
            <p>⚔️ <b>Soul Challenge:</b> {sd['challenge']}</p>
            <p style="color:#8C84A9; font-size:11px; font-style:italic; margin-top:12px;">
            ✦ Macan Peramal © 2026 Macan Angkasa — Pythagorean Numerology System ✦</p>
            """
        self.output_browser.setHtml(html)
        
    def clear_ui(self):
        self.input_name_num.clear()
        self.input_date_num.setDate(QDate.currentDate().addYears(-20))
        self.output_browser.setHtml("<p style='color:#8C84A9; font-style:italic; text-align:center;'>Hasil interpretasi getaran angka numerologi akan tersaji disini...</p>")


# ==============================================================================
# SUB-VIEW: DREAM ORACLE / TAFSIR MIMPI
# ==============================================================================
class DreamView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Search Box
        search_card = QFrame()
        search_card.setProperty("class", "MysticCard")
        search_layout = QHBoxLayout(search_card)
        
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_dreams)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_card)
        
        # Results List Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.cellClicked.connect(self.show_dream_detail)
        layout.addWidget(self.results_table)
        
        # Detail Viewer popup or card
        self.detail_card = QFrame()
        self.detail_card.setProperty("class", "MysticCard")
        detail_layout = QVBoxLayout(self.detail_card)
        self.detail_text = QTextBrowser()
        detail_layout.addWidget(self.detail_text)
        layout.addWidget(self.detail_card)
        
        self.retranslate()
        self.populate_table()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("dream_interpreter"))
        self.search_input.setPlaceholderText(lang_mgr.get("search_dream"))
        self.results_table.setHorizontalHeaderLabels([
            lang_mgr.get("category"), 
            "Mimpi / Dream Keyword", 
            "Deskripsi Singkat / Brief"
        ])
        self.detail_text.setHtml(f"<p style='color:#8C84A9; font-style:italic;'>{lang_mgr.get('dream_interpreter')}...</p>")
        
    def populate_table(self, filter_text: str = ""):
        self.results_table.setRowCount(0)
        row = 0
        for d in DREAM_DATA:
            matches_filter = False
            if not filter_text:
                matches_filter = True
            else:
                for keyword in d["keywords"]:
                    if filter_text.lower() in keyword or filter_text.lower() in d["title_id"].lower() or filter_text.lower() in d["title_en"].lower():
                        matches_filter = True
                        break
            
            if matches_filter:
                self.results_table.insertRow(row)
                
                cat = d["cat_id"] if lang_mgr.current_language == "id" else d["cat_en"]
                title = d["title_id"] if lang_mgr.current_language == "id" else d["title_en"]
                desc = d["desc_id"] if lang_mgr.current_language == "id" else d["desc_en"]
                
                # Truncate description for table summary
                summary = desc[:60] + "..." if len(desc) > 60 else desc
                
                self.results_table.setItem(row, 0, QTableWidgetItem(cat))
                self.results_table.setItem(row, 1, QTableWidgetItem(title))
                self.results_table.setItem(row, 2, QTableWidgetItem(summary))
                
                row += 1
                
    def search_dreams(self):
        self.populate_table(self.search_input.text().strip())
        
    def show_dream_detail(self, row, column):
        # Locate corresponding dream based on row title
        selected_title = self.results_table.item(row, 1).text()
        found_dream = None
        for d in DREAM_DATA:
            t_id = d["title_id"]
            t_en = d["title_en"]
            if selected_title in [t_id, t_en]:
                found_dream = d
                break
                
        if found_dream:
            cat = found_dream["cat_id"] if lang_mgr.current_language == "id" else found_dream["cat_en"]
            title = found_dream["title_id"] if lang_mgr.current_language == "id" else found_dream["title_en"]
            desc = found_dream["desc_id"] if lang_mgr.current_language == "id" else found_dream["desc_en"]
            keywords_display = ", ".join(found_dream["keywords"])

            CAT_ICON = {
                "Spiritual": "🕯️", "Rezeki": "💰", "Peringatan": "⚠️",
                "Keberuntungan": "🍀", "Cinta & Asmara": "💜", "Karir & Ilmu": "📚",
                "Leluhur & Kematian": "🪬", "Wealth": "💰", "Warning": "⚠️",
                "Luck": "🍀", "Love & Romance": "💜", "Career & Knowledge": "📚",
                "Ancestors & Death": "🪬",
            }
            icon = CAT_ICON.get(cat, "🔮")

            if lang_mgr.current_language == "id":
                html = f"""
                <h3 style="color:#FFD700; margin-top:0;">{icon} {title}</h3>
                <p style="margin:2px 0;"><b>Kategori:</b> <span style="color:#A259FF;">{cat}</span></p>
                <p style="margin:2px 0; color:#6B6886; font-size:11px;">🔑 <i>Kata kunci:</i> {keywords_display}</p>
                <hr style="border: 0.5px solid #432A70; margin: 8px 0;" />
                <p style="font-size: 14px; line-height: 1.7; color: #E2E1E6;">{desc}</p>
                <hr style="border: 0.3px solid #2B1B4D; margin: 8px 0;" />
                <p style="color:#7ECFB3; font-size:12px;">🕯️ <b>Saran Spiritual:</b> Setelah mengalami mimpi ini, dianjurkan untuk bersedekah, memperbanyak istighfar, dan menceritakan mimpi kepada orang yang dipercaya agar maknanya termanifestasi dengan baik.</p>
                <p style="color:#8C84A9; font-size:10px; font-style:italic; margin-top:8px;">✦ Macan Peramal © 2026 — Kitab Tafsir Mimpi Nusantara</p>
                """
            else:
                html = f"""
                <h3 style="color:#FFD700; margin-top:0;">{icon} {title}</h3>
                <p style="margin:2px 0;"><b>Category:</b> <span style="color:#A259FF;">{cat}</span></p>
                <p style="margin:2px 0; color:#6B6886; font-size:11px;">🔑 <i>Keywords:</i> {keywords_display}</p>
                <hr style="border: 0.5px solid #432A70; margin: 8px 0;" />
                <p style="font-size: 14px; line-height: 1.7; color: #E2E1E6;">{desc}</p>
                <hr style="border: 0.3px solid #2B1B4D; margin: 8px 0;" />
                <p style="color:#7ECFB3; font-size:12px;">🕯️ <b>Spiritual Advice:</b> After experiencing this dream, it is recommended to give charity, increase prayers of forgiveness, and share the dream with a trusted person so its meaning may manifest positively.</p>
                <p style="color:#8C84A9; font-size:10px; font-style:italic; margin-top:8px;">✦ Macan Peramal © 2026 — Nusantara Dream Interpretation Archive</p>
                """
            self.detail_text.setHtml(html)


# ==============================================================================
# SUB-VIEW: ENCYCLOPEDIA OF PRIMBON
# ==============================================================================
class PrimbonView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Category Selector Frame
        cat_card = QFrame()
        cat_card.setProperty("class", "MysticCard")
        cat_layout = QHBoxLayout(cat_card)
        
        self.lbl_search = QLabel("Cari Pengetahuan:")
        cat_layout.addWidget(self.lbl_search)
        
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_encyclopedia)
        cat_layout.addWidget(self.search_input)
        
        layout.addWidget(cat_card)
        
        # Display Scroll Area with matching Cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content_layout.setSpacing(12)
        
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        self.retranslate()
        self.load_entries()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("primbon_encyclopedia"))
        self.lbl_search.setText(lang_mgr.get("search"))
        
    def load_entries(self, filter_text: str = ""):
        # Clear layout safely
        while self.scroll_content_layout.count():
            item = self.scroll_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        CAT_COLOR = {
            "Tanda Alam": "#00B4D8", "Pranata Mangsa": "#7ECFB3",
            "Firasat Tubuh": "#D4AF37", "Aura": "#A259FF",
            "Weton Istimewa": "#FF708C", "Pantangan Adat": "#FF9F43",
            "Ritual Nusantara": "#48C774", "Shio & Zodiak": "#F953C6",
            "Kejawen": "#B2A4FF",
            "Natural Signs": "#00B4D8", "Cosmic Season": "#7ECFB3",
            "Body Sensations": "#D4AF37", "Spiritual Aura": "#A259FF",
            "Special Weton": "#FF708C", "Traditional Taboos": "#FF9F43",
            "Archipelago Rituals": "#48C774", "Shio & Zodiac": "#F953C6",
            "Javanese Mysticism": "#B2A4FF",
        }

        CAT_ICON = {
            "Tanda Alam": "🌿", "Pranata Mangsa": "🌙", "Firasat Tubuh": "🫀",
            "Aura": "✨", "Weton Istimewa": "🗓️", "Pantangan Adat": "⚠️",
            "Ritual Nusantara": "🕯️", "Shio & Zodiak": "🐉", "Kejawen": "📜",
            "Natural Signs": "🌿", "Cosmic Season": "🌙", "Body Sensations": "🫀",
            "Spiritual Aura": "✨", "Special Weton": "🗓️", "Traditional Taboos": "⚠️",
            "Archipelago Rituals": "🕯️", "Shio & Zodiac": "🐉", "Javanese Mysticism": "📜",
        }

        matched = 0
        for e in ENCYCLOPEDIA_DATA:
            title = e["title_id"] if lang_mgr.current_language == "id" else e["title_en"]
            desc  = e["desc_id"]  if lang_mgr.current_language == "id" else e["desc_en"]
            cat   = e["cat_id"]   if lang_mgr.current_language == "id" else e["cat_en"]

            if filter_text and not (filter_text.lower() in title.lower()
                                    or filter_text.lower() in desc.lower()
                                    or filter_text.lower() in cat.lower()):
                continue

            matched += 1
            clr   = CAT_COLOR.get(cat, "#A259FF")
            icon  = CAT_ICON.get(cat, "📖")

            entry_frame = QFrame()
            entry_frame.setProperty("class", "MysticCard")
            entry_frame.setMinimumHeight(110)
            frame_layout = QVBoxLayout(entry_frame)
            frame_layout.setSpacing(4)

            header_lbl = QLabel(f"{icon} {title}")
            header_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
            header_lbl.setStyleSheet("color: #FFD700;")
            header_lbl.setWordWrap(True)

            cat_lbl = QLabel(f"  ▸  {cat}")
            cat_lbl.setStyleSheet(f"color: {clr}; font-size: 11px; font-weight: bold;")

            sep = QFrame()
            sep.setFrameShape(QFrame.HLine)
            sep.setStyleSheet(f"color: {clr}; background-color: {clr}; border: none; max-height: 1px;")

            desc_lbl = QLabel(desc)
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet("color: #D2CFDF; font-size: 12px; line-height: 1.5;")

            frame_layout.addWidget(header_lbl)
            frame_layout.addWidget(cat_lbl)
            frame_layout.addWidget(sep)
            frame_layout.addWidget(desc_lbl)

            self.scroll_content_layout.addWidget(entry_frame)

        # Summary label
        count_lbl = QLabel(f"📚 {matched} entri ditemukan" if lang_mgr.current_language == "id" else f"📚 {matched} entries found")
        count_lbl.setStyleSheet("color:#6B6886; font-size:11px; font-style:italic; margin:4px 0;")
        self.scroll_content_layout.insertWidget(0, count_lbl)

        self.scroll_content_layout.addStretch()
        
    def search_encyclopedia(self):
        self.load_entries(self.search_input.text().strip())


# ==============================================================================
# SUB-VIEW: SPIRITUAL CALENDAR / WETON PASARAN OVERVIEW
# ==============================================================================
class CalendarView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Calendar Controls
        ctrl_card = QFrame()
        ctrl_card.setProperty("class", "MysticCard")
        ctrl_layout = QHBoxLayout(ctrl_card)
        
        self.lbl_month = QLabel("Pilih Bulan:")
        ctrl_layout.addWidget(self.lbl_month)
        
        self.combo_month = QComboBox()
        months_id = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                     "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        for m in months_id:
            self.combo_month.addItem(m)
        self.combo_month.setCurrentIndex(datetime.date.today().month - 1)
        self.combo_month.currentIndexChanged.connect(self.render_calendar_month)
        ctrl_layout.addWidget(self.combo_month)
        
        self.lbl_year = QLabel("Pilih Tahun:")
        ctrl_layout.addWidget(self.lbl_year)
        
        self.combo_year = QComboBox()
        for y in range(2020, 2036):
            self.combo_year.addItem(str(y))
        self.combo_year.setCurrentText(str(datetime.date.today().year))
        self.combo_year.currentIndexChanged.connect(self.render_calendar_month)
        ctrl_layout.addWidget(self.combo_year)
        
        layout.addWidget(ctrl_card)
        
        # Grid layout representing calendar dates
        self.grid_card = QFrame()
        self.grid_card.setProperty("class", "MysticCard")
        self.grid_layout = QGridLayout(self.grid_card)
        layout.addWidget(self.grid_card, 5)
        
        self.retranslate()
        self.render_calendar_month()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("calendar"))
        self.lbl_month.setText("Bulan / Month:")
        self.lbl_year.setText("Tahun / Year:")
        
    def render_calendar_month(self):
        # Clear layout safely
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
                
        month = self.combo_month.currentIndex() + 1
        year = int(self.combo_year.currentText())
        
        # Day Names Header Row
        days_header = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"]
        for i, dh in enumerate(days_header):
            dh_lbl = QLabel(dh)
            dh_lbl.setAlignment(Qt.AlignCenter)
            dh_lbl.setStyleSheet("color:#FFD700; font-weight:bold;")
            self.grid_layout.addWidget(dh_lbl, 0, i)
            
        # Get start weekday of month
        first_day = datetime.date(year, month, 1)
        start_weekday = first_day.weekday() # Monday=0, Sunday=6
        # Offset to start Sunday (Min)=0
        start_col = (start_weekday + 1) % 7
        
        # Number of days in chosen month
        if month == 12:
            num_days = (datetime.date(year + 1, 1, 1) - first_day).days
        else:
            num_days = (datetime.date(year, month + 1, 1) - first_day).days
            
        row = 1
        col = start_col
        
        for d in range(1, num_days + 1):
            date_obj = datetime.date(year, month, d)
            weton = DestinyEngine.calculate_weton(date_obj)
            neptu = weton['neptu_total']
            is_today = (date_obj == datetime.date.today())

            # Determine styling
            is_jumat_kliwon = weton["day_id"] == "Jumat" and weton["pasaran"] == "Kliwon"
            is_selasa_kliwon = weton["day_id"] == "Selasa" and weton["pasaran"] == "Kliwon"
            is_high_neptu = neptu >= 14

            day_box = QFrame()
            if is_today:
                day_box.setStyleSheet("QFrame { background-color: #1A3A2A; border: 2px solid #48C774; border-radius: 6px; }")
            elif is_jumat_kliwon:
                day_box.setStyleSheet("QFrame { background-color: #4D1226; border: 1.5px solid #FF708C; border-radius: 6px; }")
            elif is_selasa_kliwon:
                day_box.setStyleSheet("QFrame { background-color: #2D1A40; border: 1.5px solid #A259FF; border-radius: 6px; }")
            elif is_high_neptu:
                day_box.setStyleSheet("QFrame { background-color: #1E2A1A; border: 1px solid #7ECFB3; border-radius: 6px; }")
            else:
                day_box.setStyleSheet("""
                    QFrame { background-color: #1A1333; border: 1.5px solid #332057; border-radius: 6px; }
                    QFrame:hover { border-color: #FFD700; }
                """)

            box_layout = QVBoxLayout(day_box)
            box_layout.setContentsMargins(3, 3, 3, 3)
            box_layout.setSpacing(1)

            day_lbl = QLabel(f"<b>{d}</b>")
            day_lbl.setStyleSheet(f"color:{'#48C774' if is_today else '#FFFFFF'}; font-size:12px;")
            day_lbl.setAlignment(Qt.AlignCenter)

            pas_lbl = QLabel(weton["pasaran"])
            if is_jumat_kliwon:
                pas_lbl.setStyleSheet("color:#FF708C; font-weight:bold; font-size:9px;")
            elif is_selasa_kliwon:
                pas_lbl.setStyleSheet("color:#A259FF; font-weight:bold; font-size:9px;")
            elif is_high_neptu:
                pas_lbl.setStyleSheet("color:#7ECFB3; font-size:9px;")
            else:
                pas_lbl.setStyleSheet("color:#6B6886; font-size:9px;")
            pas_lbl.setAlignment(Qt.AlignCenter)

            neptu_lbl = QLabel(f"N:{neptu}")
            neptu_lbl.setStyleSheet("color:#4A4260; font-size:8px;")
            neptu_lbl.setAlignment(Qt.AlignCenter)

            box_layout.addWidget(day_lbl)
            box_layout.addWidget(pas_lbl)
            box_layout.addWidget(neptu_lbl)

            self.grid_layout.addWidget(day_box, row, col)

            col += 1
            if col > 6:
                col = 0
                row += 1

        # Legend row
        legend_id = "<span style='color:#FF708C;'>■</span> Jumat Kliwon &nbsp; <span style='color:#A259FF;'>■</span> Selasa Kliwon &nbsp; <span style='color:#7ECFB3;'>■</span> Neptu Tinggi ≥14 &nbsp; <span style='color:#48C774;'>■</span> Hari Ini"
        legend_en = "<span style='color:#FF708C;'>■</span> Friday Kliwon &nbsp; <span style='color:#A259FF;'>■</span> Tuesday Kliwon &nbsp; <span style='color:#7ECFB3;'>■</span> High Neptu ≥14 &nbsp; <span style='color:#48C774;'>■</span> Today"
        legend_lbl = QLabel(legend_id if lang_mgr.current_language == "id" else legend_en)
        legend_lbl.setStyleSheet("font-size:10px; color:#8C84A9; padding:4px 0;")
        self.grid_layout.addWidget(legend_lbl, row + 1, 0, 1, 7)


# ==============================================================================
# SUB-VIEW: DAILY FORTUNE & AUSPICIOUS DAY FINDER
# ==============================================================================
class DailyFortuneView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        # Top Card: Dynamic Daily Oracle Generator
        top_card = QFrame()
        top_card.setProperty("class", "MysticCard")
        top_layout = QVBoxLayout(top_card)
        
        self.fortune_header = QLabel()
        self.fortune_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.fortune_header.setStyleSheet("color: #FFD700;")
        
        self.fortune_body = QTextBrowser()
        self.fortune_body.setMinimumHeight(150)
        
        top_layout.addWidget(self.fortune_header)
        top_layout.addWidget(self.fortune_body)
        layout.addWidget(top_card)
        
        # Bottom Card: Auspicious / Lucky Day Finder
        find_card = QFrame()
        find_card.setProperty("class", "MysticCard")
        find_layout = QVBoxLayout(find_card)
        
        self.lbl_lucky_finder = QLabel()
        self.lbl_lucky_finder.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.lbl_lucky_finder.setStyleSheet("color: #FFD700;")
        find_layout.addWidget(self.lbl_lucky_finder)
        
        h_layout = QHBoxLayout()
        self.lbl_activity = QLabel()
        h_layout.addWidget(self.lbl_activity)
        
        self.combo_act = QComboBox()
        self.combo_act.addItem("Buka Usaha / Business Start")
        self.combo_act.addItem("Bepergian / Journey Travel")
        self.combo_act.addItem("Pernikahan / Marriage Ceremony")
        h_layout.addWidget(self.combo_act)
        
        self.btn_lucky = QPushButton()
        self.btn_lucky.setProperty("class", "GoldButton")
        self.btn_lucky.clicked.connect(self.find_auspicious_dates)
        h_layout.addWidget(self.btn_lucky)
        
        find_layout.addLayout(h_layout)
        
        self.lucky_results = QTextBrowser()
        self.lucky_results.setMinimumHeight(120)
        find_layout.addWidget(self.lucky_results)
        
        layout.addWidget(find_card)
        
        self.retranslate()
        self.generate_daily_outlook()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("daily_fortune"))
        self.fortune_header.setText(lang_mgr.get("daily_msg"))
        self.lbl_lucky_finder.setText(lang_mgr.get("lucky_day"))
        self.lbl_activity.setText(lang_mgr.get("choose_activity"))
        self.btn_lucky.setText(lang_mgr.get("find_lucky_days"))
        self.lucky_results.setHtml("<p style='color:#8C84A9; font-style:italic;'>Hasil hari baik akan tertera di sini...</p>")
        
    def generate_daily_outlook(self):
        today = datetime.date.today()
        weton = DestinyEngine.calculate_weton(today)
        day_id = weton['day_id']
        day_en = weton['day_en']
        pasaran = weton['pasaran']
        neptu = weton['neptu_total']
        elem_id = weton['element_id']
        elem_en = weton['element_en']

        # Neptu-based prosperity rating
        if neptu >= 15:
            rating_id, rating_en = "🌟🌟🌟🌟🌟 Sangat Baik", "🌟🌟🌟🌟🌟 Excellent"
        elif neptu >= 12:
            rating_id, rating_en = "🌟🌟🌟🌟 Baik", "🌟🌟🌟🌟 Good"
        elif neptu >= 9:
            rating_id, rating_en = "🌟🌟🌟 Cukup Baik", "🌟🌟🌟 Moderate"
        else:
            rating_id, rating_en = "🌟🌟 Perlu Waspada", "🌟🌟 Caution Advised"

        # Element-specific daily advice
        ELEM_ADV_ID = {
            "Bumi / Tanah": "Energi tanah mendukung stabilitas dan kerja keras. Hari ini cocok untuk transaksi properti, bertanam, atau memperkuat pondasi usaha.",
            "Angin / Udara": "Energi angin membawa kreativitas dan komunikasi. Ideal untuk presentasi, negosiasi, atau memperbarui media sosial dan pemasaran.",
            "Api": "Energi api memuncak. Keberanian dan semangat Anda sangat tinggi — cocok untuk memimpin rapat, berolahraga, dan mengambil keputusan tegas.",
            "Samudra / Air": "Energi air membawa intuisi dan kepekaan spiritual. Waktu terbaik untuk meditasi, introspeksi, dan memperkuat hubungan emosional dengan orang tercinta."
        }
        ELEM_ADV_EN = {
            "Earth / Ground": "Earth energy supports stability and hard work. Excellent for property transactions, planting, or strengthening business foundations.",
            "Wind / Air": "Wind energy brings creativity and communication. Ideal for presentations, negotiations, or renewing social media and marketing campaigns.",
            "Fire": "Fire energy peaks today. Your courage and drive are high — perfect for leading meetings, exercise, and making decisive calls.",
            "Water / Ocean": "Water energy brings intuition and spiritual sensitivity. Best for meditation, self-reflection, and deepening emotional bonds with loved ones."
        }
        adv_id = ELEM_ADV_ID.get(elem_id, "Jaga keseimbangan batin dan banyak bersyukur hari ini.")
        adv_en = ELEM_ADV_EN.get(elem_en, "Maintain inner balance and practice gratitude throughout today.")

        # Friday Kliwon special message
        bonus_id = ""
        bonus_en = ""
        if day_id == "Jumat" and pasaran == "Kliwon":
            bonus_id = "<p style='color:#FF708C; font-weight:bold;'>🔮 Malam ini adalah Jumat Kliwon — malam paling sakral dalam kalender Jawa. Perbanyak doa, sedekah, dan meditasi malam ini untuk mendapat berkah spiritual berlipat ganda.</p>"
            bonus_en = "<p style='color:#FF708C; font-weight:bold;'>🔮 Tonight is Friday Kliwon — the most sacred night in the Javanese calendar. Increase prayers, charity, and meditation tonight to receive multiplied spiritual blessings.</p>"

        if lang_mgr.current_language == "id":
            html = f"""
            <table width="100%" cellpadding="4" style="margin-bottom:8px; font-size:12px; color:#9B98B0;">
                <tr>
                    <td>📅 <b>Weton Hari Ini:</b></td>
                    <td><span style="color:#D4AF37; font-weight:bold;">{day_id} {pasaran}</span></td>
                    <td>🔢 <b>Neptu:</b></td>
                    <td><span style="color:#A259FF; font-weight:bold;">{neptu}</span></td>
                </tr>
                <tr>
                    <td>🌿 <b>Elemen:</b></td>
                    <td><span style="color:#7ECFB3;">{elem_id}</span></td>
                    <td>⭐ <b>Rating Hari:</b></td>
                    <td>{rating_id}</td>
                </tr>
            </table>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FFD700; margin-bottom:4px;">🌅 Ramalan Rezeki & Karier</h3>
            <p>Aliran energi {elem_id.lower()} hari ini memberikan getaran kuat untuk kemajuan. {adv_id}</p>
            {bonus_id}
            <h3 style="color:#FFD700; margin-bottom:4px;">🍃 Hubungan & Sosial</h3>
            <p>Neptu {neptu} menandakan hari yang {'sangat mendukung interaksi sosial yang hangat dan tulus' if neptu >= 12 else 'meminta Anda lebih berhati-hati dalam tutur kata dan sikap'}. Jaga silaturahmi, hindari gosip, dan jadilah pendengar yang baik.</p>

            <h3 style="color:#FFD700; margin-bottom:4px;">🧘 Kesehatan & Batin</h3>
            <p>{'Energi fisik Anda tinggi — manfaatkan untuk olahraga atau kegiatan produktif.' if neptu >= 11 else 'Istirahatlah cukup dan jangan paksakan diri. Hari ini saatnya mengisi ulang energi batin.'} Minum air putih cukup dan luangkan waktu 10 menit untuk bernapas dalam-dalam.</p>
            """
        else:
            html = f"""
            <table width="100%" cellpadding="4" style="margin-bottom:8px; font-size:12px; color:#9B98B0;">
                <tr>
                    <td>📅 <b>Today's Weton:</b></td>
                    <td><span style="color:#D4AF37; font-weight:bold;">{day_en} {pasaran}</span></td>
                    <td>🔢 <b>Neptu:</b></td>
                    <td><span style="color:#A259FF; font-weight:bold;">{neptu}</span></td>
                </tr>
                <tr>
                    <td>🌿 <b>Element:</b></td>
                    <td><span style="color:#7ECFB3;">{elem_en}</span></td>
                    <td>⭐ <b>Day Rating:</b></td>
                    <td>{rating_en}</td>
                </tr>
            </table>
            <hr style="border: 0.3px solid #2B1B4D;" />

            <h3 style="color:#FFD700; margin-bottom:4px;">🌅 Prosperity & Career Forecast</h3>
            <p>Today's {elem_en.lower()} energy delivers strong vibrations for advancement. {adv_en}</p>
            {bonus_en}
            <h3 style="color:#FFD700; margin-bottom:4px;">🍃 Relationships & Social Life</h3>
            <p>Neptu {neptu} signals a day that {'strongly supports warm and sincere social interactions' if neptu >= 12 else 'calls for careful, measured speech and conduct'}. Nurture relationships, avoid gossip, and be a great listener.</p>

            <h3 style="color:#FFD700; margin-bottom:4px;">🧘 Health & Inner Balance</h3>
            <p>{'Your physical energy is high — use it for exercise or productive activities.' if neptu >= 11 else 'Rest well and avoid overexertion. Today is a day to replenish your inner reserves.'} Stay well hydrated and set aside 10 minutes for deep breathing.</p>
            """
        self.fortune_body.setHtml(html)
        
    def find_auspicious_dates(self):
        today = datetime.date.today()
        lucky_found = []
        activity = self.combo_act.currentText()

        # Per-activity minimum neptu thresholds and sacred combos
        ACTIVITY_RULES = {
            "Buka Usaha / Business Start": {"min_neptu": 12, "sacred": [("Kamis", "Pahing"), ("Rabu", "Wage"), ("Jumat", "Legi")]},
            "Bepergian / Journey Travel":  {"min_neptu": 10, "sacred": [("Minggu", "Wage"), ("Senin", "Pon"), ("Kamis", "Kliwon")]},
            "Pernikahan / Marriage Ceremony": {"min_neptu": 13, "sacred": [("Jumat", "Kliwon"), ("Sabtu", "Legi"), ("Rabu", "Pahing")]},
        }
        rule = ACTIVITY_RULES.get(activity, {"min_neptu": 12, "sacred": []})

        for d in range(1, 60):
            target = today + datetime.timedelta(days=d)
            w = DestinyEngine.calculate_weton(target)
            is_sacred = (w['day_id'], w['pasaran']) in rule['sacred']
            if w['neptu_total'] >= rule['min_neptu'] or is_sacred:
                lucky_found.append((target, w, is_sacred))
                if len(lucky_found) >= 5:
                    break

        results_html = f"<h3 style='color:#FFD700;'>🌟 {lang_mgr.get('lucky_days_result')}</h3>"
        results_html += f"<p style='color:#9B98B0; font-size:11px;'>Aktivitas: <b>{activity}</b></p>"

        for ld, weton_info, is_sacred in lucky_found:
            formatted_date = ld.strftime("%d %B %Y")
            badge = " <span style='color:#FF708C; font-weight:bold;'>✦ SAKRAL</span>" if is_sacred else ""

            if lang_mgr.current_language == "id":
                results_html += (
                    f"<div style='margin:6px 0; padding:6px; background:#1A1333; border:1px solid #332057; border-radius:6px;'>"
                    f"<b style='color:#D4AF37;'>{formatted_date}</b>{badge}<br/>"
                    f"<span style='color:#00B4D8;'>{weton_info['day_id']} {weton_info['pasaran']}</span> "
                    f"— Neptu: <b>{weton_info['neptu_total']}</b> "
                    f"| Elemen: <span style='color:#7ECFB3;'>{weton_info['element_id']}</span>"
                    f"</div>"
                )
            else:
                results_html += (
                    f"<div style='margin:6px 0; padding:6px; background:#1A1333; border:1px solid #332057; border-radius:6px;'>"
                    f"<b style='color:#D4AF37;'>{formatted_date}</b>{badge}<br/>"
                    f"<span style='color:#00B4D8;'>{weton_info['day_en']} {weton_info['pasaran']}</span> "
                    f"— Neptu: <b>{weton_info['neptu_total']}</b> "
                    f"| Element: <span style='color:#7ECFB3;'>{weton_info['element_en']}</span>"
                    f"</div>"
                )

        if not lucky_found:
            results_html += "<p style='color:#FF708C;'>Tidak ditemukan hari baik dalam 60 hari ke depan untuk aktivitas ini.</p>"

        results_html += "<p style='color:#8C84A9; font-size:10px; margin-top:8px;'>✦ Tanda SAKRAL menunjukkan kombinasi weton paling ideal untuk aktivitas yang dipilih.</p>"
        self.lucky_results.setHtml(results_html)


# ==============================================================================
# SUB-VIEW: SETTINGS & LOCALIZATION CONTROL
# ==============================================================================
class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        lang_mgr.language_changed.connect(self.retranslate)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.title = QLabel()
        self.title.setProperty("class", "MysticSectionTitle")
        layout.addWidget(self.title)
        
        card = QFrame()
        card.setProperty("class", "MysticCard")
        form_layout = QVBoxLayout(card)
        
        self.lbl_lang = QLabel()
        self.lbl_lang.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.lbl_lang.setStyleSheet("color: #FFD700;")
        form_layout.addWidget(self.lbl_lang)
        
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("Bahasa Indonesia", "id")
        self.combo_lang.addItem("English Support", "en")
        self.combo_lang.currentIndexChanged.connect(self.change_language)
        form_layout.addWidget(self.combo_lang)
        
        # Purge Data Box
        form_layout.addSpacing(20)
        self.lbl_danger_zone = QLabel("Zona Pembersihan Spiritual / Purge Area")
        self.lbl_danger_zone.setStyleSheet("color:#FF708C; font-weight:bold;")
        form_layout.addWidget(self.lbl_danger_zone)
        
        self.btn_clear = QPushButton()
        self.btn_clear.setProperty("class", "DestructiveButton")
        self.btn_clear.clicked.connect(self.clear_history)
        form_layout.addWidget(self.btn_clear)
        
        layout.addWidget(card)
        layout.addStretch()
        self.retranslate()
        
    def retranslate(self):
        self.title.setText(lang_mgr.get("settings"))
        self.lbl_lang.setText(lang_mgr.get("language_select"))
        self.btn_clear.setText(lang_mgr.get("clear_history"))
        
    def change_language(self, index):
        lang = self.combo_lang.currentData()
        lang_mgr.set_language(lang)
        
    def clear_history(self):
        QMessageBox.information(self, "Macan Peramal", lang_mgr.get("history_cleared"))


# ==============================================================================
# MAIN WINDOW FRAME WITH WINDOW CONTROLS & MODERN SIDEBAR
# ==============================================================================
class MacanPeramalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_position = QPoint()
        
        # Frameless Window aesthetics & styling
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(1150, 780)
        
        self.init_main_ui()
        lang_mgr.language_changed.connect(self.retranslate_ui)
        
    def init_main_ui(self):
        # Outer boundary with rounded borders
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setStyleSheet("""
            QWidget#CentralWidget {
                background-color: #0B0816;
                border: 1px solid #2B1B4D;
                border-radius: 12px;
            }
        """)
        self.setCentralWidget(self.central_widget)
        
        # Ambient Particle Layer under content
        self.particle_bg = MysticParticleWidget(self.central_widget)
        
        # Core vertical layout organizing TitleBar and Main Content Area
        core_layout = QVBoxLayout(self.central_widget)
        core_layout.setContentsMargins(0, 0, 0, 0)
        core_layout.setSpacing(0)
        
        # 1. Custom Title Bar
        title_bar = QFrame()
        title_bar.setObjectName("TitleBarFrame")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(15, 10, 15, 10)
        
        # App Identity Icon & Title
        self.title_lbl = QLabel("🐯 Macan Peramal")
        self.title_lbl.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 15px; letter-spacing: 1px;")
        title_bar_layout.addWidget(self.title_lbl)
        
        title_bar_layout.addStretch()
        
        # Window buttons (Min, Max, Close) styled as glowing circles
        btn_min = QPushButton("━")
        btn_min.setStyleSheet("background: transparent; color: #8C84A9; font-weight: bold; border: none; padding: 4px;")
        btn_min.clicked.connect(self.showMinimized)
        
        btn_close = QPushButton("✕")
        btn_close.setStyleSheet("background: transparent; color: #FF708C; font-weight: bold; border: none; padding: 4px;")
        btn_close.clicked.connect(self.close)
        
        title_bar_layout.addWidget(btn_min)
        title_bar_layout.addWidget(btn_close)
        
        core_layout.addWidget(title_bar)
        
        # 2. Workspace Splitter (Sidebar navigation & stack container)
        workspace = QFrame()
        workspace_layout = QHBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)
        
        # Sidebar Panel
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 15, 12, 15)
        sidebar_layout.setSpacing(8)
        
        # App identity header in sidebar
        app_header = QVBoxLayout()
        self.sidebar_app_title = QLabel("Macan Peramal")
        self.sidebar_app_title.setObjectName("AppNameLabel")
        self.sidebar_app_slogan = QLabel("Jejak Takdir Nusantara")
        self.sidebar_app_slogan.setObjectName("AppSloganLabel")
        app_header.addWidget(self.sidebar_app_title)
        app_header.addWidget(self.sidebar_app_slogan)
        sidebar_layout.addLayout(app_header)
        sidebar_layout.addSpacing(25)
        
        # Navigation Items mapped directly to QStackedWidget indices
        self.nav_buttons = []
        self.nav_info = [
            ("dashboard", "🔮"),
            ("name_analysis", "👤"),
            ("birth_analysis", "📅"),
            ("compatibility", "💞"),
            ("numerology", "⭐"),
            ("dream_interpreter", "🌙"),
            ("primbon_encyclopedia", "📖"),
            ("calendar", "🕯️"),
            ("daily_fortune", "🍀"),
            ("settings", "⚙️")
        ]
        
        for index, (key, emoji) in enumerate(self.nav_info):
            btn = QPushButton(f"{emoji}  {lang_mgr.get(key)}")
            btn.setProperty("class", "NavButton")
            btn.setCheckable(True)
            if index == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_view(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append((btn, key, emoji))
            
        sidebar_layout.addStretch()
        
        # Copyright Info Footer inside sidebar
        self.copyright_lbl = QLabel(lang_mgr.get("copyright"))
        self.copyright_lbl.setStyleSheet("color:#5A5475; font-size:9px; font-weight: bold;")
        self.copyright_lbl.setAlignment(Qt.AlignCenter)
        self.copyright_lbl.setWordWrap(True)
        sidebar_layout.addWidget(self.copyright_lbl)
        
        workspace_layout.addWidget(sidebar, 2)
        
        # Stack Widget (Views Container)
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentFrame")
        
        # Initialize views & register to the stack
        self.view_dashboard = DashboardView(self.switch_view)
        self.view_name_analysis = NameAnalysisView()
        self.view_birth_analysis = BirthAnalysisView()
        self.view_compatibility = CompatibilityView()
        self.view_numerology = NumerologyView()
        self.view_dream = DreamView()
        self.view_primbon = PrimbonView()
        self.view_calendar = CalendarView()
        self.view_daily_fortune = DailyFortuneView()
        self.view_settings = SettingsView()
        
        self.content_stack.addWidget(self.view_dashboard)
        self.content_stack.addWidget(self.view_name_analysis)
        self.content_stack.addWidget(self.view_birth_analysis)
        self.content_stack.addWidget(self.view_compatibility)
        self.content_stack.addWidget(self.view_numerology)
        self.content_stack.addWidget(self.view_dream)
        self.content_stack.addWidget(self.view_primbon)
        self.content_stack.addWidget(self.view_calendar)
        self.content_stack.addWidget(self.view_daily_fortune)
        self.content_stack.addWidget(self.view_settings)
        
        workspace_layout.addWidget(self.content_stack, 7)
        core_layout.addWidget(workspace)
        
        # Apply Global Stylingsheet
        self.setStyleSheet(MYSTIC_THEME_QSS)
        self.retranslate_ui()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Match particle background size dynamically
        self.particle_bg.setGeometry(self.rect())
        
    def switch_view(self, index: int):
        self.content_stack.setCurrentIndex(index)
        # Uncheck other navigation buttons
        for idx, (btn, _, _) in enumerate(self.nav_buttons):
            btn.setChecked(idx == index)
            
    def retranslate_ui(self):
        self.sidebar_app_title.setText(lang_mgr.get("app_title"))
        self.sidebar_app_slogan.setText(lang_mgr.get("app_slogan"))
        self.copyright_lbl.setText(lang_mgr.get("copyright"))
        
        # Retranslate Sidebar button labels
        for btn, key, emoji in self.nav_buttons:
            btn.setText(f"{emoji}  {lang_mgr.get(key)}")
            
    # Window dragging logic overrides for Frameless UI Experience
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


# ==============================================================================
# MAIN APPLICATION LAUNCHPOINT
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Force beautiful rendering engine configs
    app.setStyle("Fusion")
    
    window = MacanPeramalWindow()
    window.show()
    
    sys.exit(app.exec())