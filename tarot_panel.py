#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Module  : tarot_panel.py
Project : Macan Peramal
Author  : © 2026 Macan Angkasa
Description:
    Modern Tarot Reading module for the Macan Peramal spiritual dashboard.
    Implements Daily Tarot, Pick-A-Card, shuffle/flip animations, and a full
    Major Arcana database — all styled to match the mystical premium dark-purple
    and gold aesthetic of the main application.

Classes:
    TarotDeck               — Data layer: card pool, shuffling, random picks
    TarotReadingEngine      — Business logic: reading modes, interpretation
    TarotCardWidget         — Single interactive card (flip + glow animations)
    TarotPanel              — Top-level view widget integrated into the app stack
================================================================================
"""

import os
import math
import random
import threading
from typing import Optional

try:
    import winsound
    _WINSOUND_AVAILABLE = True
except ImportError:
    _WINSOUND_AVAILABLE = False

from PySide6.QtCore import (
    Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve,
    QParallelAnimationGroup, QSequentialAnimationGroup,
    Signal, Slot, Property, QRect, QRectF, QPoint
)
from PySide6.QtGui import (
    QPainter, QColor, QLinearGradient, QRadialGradient,
    QFont, QPen, QBrush, QPixmap, QPainterPath
)
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QGraphicsOpacityEffect, QSizePolicy,
    QStackedWidget, QGridLayout, QSpacerItem,
    QGraphicsDropShadowEffect
)


# ==============================================================================
# TAROT DATABASE — Full Major Arcana (22 cards)
# ==============================================================================
TAROT_DB: dict[str, dict] = {
    "the_fool": {
        "title": "The Fool",
        "number": "0",
        "keywords": ["Awal Baru", "Petualangan", "Kebebasan"],
        "meaning": (
            "Alam semesta mengundangmu melangkah tanpa rasa takut. "
            "Saatnya memulai babak baru dengan jiwa yang bersih dan hati terbuka. "
            "Percayakan dirimu pada alur kosmik yang sedang bergerak untukmu."
        ),
        "upright": "Keberanian memulai, spontanitas, potensi tak terbatas.",
        "reversed": "Kecerobohan, kurang pertimbangan, perlu berhenti sejenak.",
        "element": "Udara",
        "planet": "Uranus",
        "color_accent": "#A8D8EA",
    },
    "the_magician": {
        "title": "The Magician",
        "number": "I",
        "keywords": ["Manifestasi", "Kekuatan", "Kreasi"],
        "meaning": (
            "Semua sumber daya yang kamu butuhkan sudah ada di tanganmu. "
            "Fokuskan niatmu dan ubah keinginan menjadi kenyataan. "
            "Kamu memiliki kekuatan untuk menciptakan takdirmu sendiri."
        ),
        "upright": "Kekuatan manifestasi, keterampilan, konsentrasi penuh.",
        "reversed": "Manipulasi, potensi yang belum dimanfaatkan, tidak fokus.",
        "element": "Api",
        "planet": "Merkurius",
        "color_accent": "#FFD700",
    },
    "the_high_priestess": {
        "title": "The High Priestess",
        "number": "II",
        "keywords": ["Intuisi", "Misteri", "Kebijaksanaan Batin"],
        "meaning": (
            "Jawaban yang kamu cari tidak ada di luar — ia bersemayam jauh di dalam batinmu. "
            "Diam dan dengarkan suara hati nuranimu. "
            "Rahasia kosmik sedang menunggumu di ambang kesadaran."
        ),
        "upright": "Intuisi tajam, pengetahuan batin, kebijaksanaan tersembunyi.",
        "reversed": "Menekan perasaan, abaikan intuisi, rahasia yang menyakiti.",
        "element": "Air",
        "planet": "Bulan",
        "color_accent": "#B19FFC",
    },
    "the_empress": {
        "title": "The Empress",
        "number": "III",
        "keywords": ["Kesuburan", "Kelimpahan", "Alam"],
        "meaning": (
            "Energi keibuan alam sedang memelukmu dengan penuh kasih. "
            "Saatnya menumbuhkan sesuatu yang berharga — hubungan, karya seni, atau karier. "
            "Kelimpahan mengalir deras ke arahmu."
        ),
        "upright": "Kesuburan, kreativitas, kemakmuran, koneksi dengan alam.",
        "reversed": "Ketergantungan berlebihan, kurang kreatif, menahan diri.",
        "element": "Bumi",
        "planet": "Venus",
        "color_accent": "#90EE90",
    },
    "the_emperor": {
        "title": "The Emperor",
        "number": "IV",
        "keywords": ["Otoritas", "Struktur", "Stabilitas"],
        "meaning": (
            "Tegakkan fondasi hidupmu dengan disiplin dan ketegasan. "
            "Saatnya menjadi pemimpin sejati — bagi dirimu sendiri maupun orang-orang di sekitarmu. "
            "Keteraturan adalah jembatan menuju kemakmuran."
        ),
        "upright": "Kepemimpinan, disiplin, kontrol, fondasi yang kuat.",
        "reversed": "Dominasi berlebihan, kekakuan, abai terhadap perasaan.",
        "element": "Api",
        "planet": "Aries",
        "color_accent": "#FF6B6B",
    },
    "the_hierophant": {
        "title": "The Hierophant",
        "number": "V",
        "keywords": ["Tradisi", "Bimbingan Spiritual", "Keyakinan"],
        "meaning": (
            "Carilah bimbingan dari mereka yang lebih bijaksana atau dari ajaran spiritual. "
            "Tradisi dan ritual memiliki kekuatan tersendiri dalam perjalananmu. "
            "Saatnya menghubungkan diri dengan warisan rohani yang mendalam."
        ),
        "upright": "Spiritualitas, konvensi, bimbingan moral, tradisi.",
        "reversed": "Dogmatisme, pemberontakan terhadap norma, kebebasan berpikir.",
        "element": "Bumi",
        "planet": "Taurus",
        "color_accent": "#DEB887",
    },
    "the_lovers": {
        "title": "The Lovers",
        "number": "VI",
        "keywords": ["Cinta", "Pilihan", "Harmoni"],
        "meaning": (
            "Sebuah pilihan penting ada di hadapanmu — ikuti hatimu dengan penuh kesadaran. "
            "Energi cinta kosmik sedang memberkati hubungan-hubunganmu. "
            "Persatuan sejati lahir dari keselarasan nilai dan jiwa."
        ),
        "upright": "Cinta, keselarasan, hubungan bermakna, pilihan hati.",
        "reversed": "Ketidakseimbangan, pilihan buruk, ketidaksetiaan.",
        "element": "Udara",
        "planet": "Gemini",
        "color_accent": "#FFB6C1",
    },
    "the_chariot": {
        "title": "The Chariot",
        "number": "VII",
        "keywords": ["Tekad", "Kemenangan", "Kontrol Diri"],
        "meaning": (
            "Kendalikan energi yang bertentangan dalam dirimu dan arahkan menuju satu tujuan. "
            "Kemenangan sudah di depan mata — tapi hanya jika kamu tidak menyerah. "
            "Disiplin dan tekad adalah kendaraanmu menuju kejayaan."
        ),
        "upright": "Tekad baja, disiplin, kemenangan atas rintangan.",
        "reversed": "Kehilangan kontrol, agresivitas, hambatan besar.",
        "element": "Air",
        "planet": "Kanker",
        "color_accent": "#87CEEB",
    },
    "strength": {
        "title": "Strength",
        "number": "VIII",
        "keywords": ["Keberanian", "Kesabaran", "Kekuatan Batin"],
        "meaning": (
            "Kekuatan terbesar bukan terletak pada otot, melainkan pada kelembutan dan kasih sayang. "
            "Hadapi situasi sulit dengan hati yang tenang dan pikiran yang jernih. "
            "Kamu lebih kuat dari yang kamu bayangkan."
        ),
        "upright": "Keberanian batin, ketahanan, pengendalian emosi.",
        "reversed": "Keraguan diri, kelemahan sesaat, perlu memulihkan energi.",
        "element": "Api",
        "planet": "Leo",
        "color_accent": "#FFA500",
    },
    "the_hermit": {
        "title": "The Hermit",
        "number": "IX",
        "keywords": ["Refleksi", "Kebijaksanaan", "Kesendirian"],
        "meaning": (
            "Saatnya fokus pada refleksi diri dan mencari jawaban dari dalam. "
            "Kesendirian bukan hukuman — ia adalah hadiah dari alam semesta untuk bertumbuh. "
            "Kebijaksanaan sejati lahir dari keheningan yang mendalam."
        ),
        "upright": "Introspeksi, bimbingan batin, pencarian makna hidup.",
        "reversed": "Isolasi berlebihan, menolak bantuan, terlalu menarik diri.",
        "element": "Bumi",
        "planet": "Virgo",
        "color_accent": "#C8B89A",
    },
    "wheel_of_fortune": {
        "title": "Wheel of Fortune",
        "number": "X",
        "keywords": ["Siklus", "Takdir", "Perubahan"],
        "meaning": (
            "Roda takdir sedang berputar dan membawa perubahan besar. "
            "Apa yang turun pasti akan naik kembali — percayai siklus kosmik ini. "
            "Saatnya mengalir bersama arus dan memanfaatkan momentum."
        ),
        "upright": "Perubahan positif, siklus baru, keberuntungan datang.",
        "reversed": "Nasib buruk sementara, melawan perubahan, siklus negatif.",
        "element": "Api",
        "planet": "Jupiter",
        "color_accent": "#FFD700",
    },
    "justice": {
        "title": "Justice",
        "number": "XI",
        "keywords": ["Keadilan", "Kebenaran", "Keseimbangan"],
        "meaning": (
            "Alam semesta mencatat setiap perbuatan dan akan memberikan balasan yang setimpal. "
            "Kebenaran akan terungkap — jadilah jujur dalam setiap tindakanmu. "
            "Keseimbangan kosmik sedang bekerja untuk meluruskan segala ketimpangan."
        ),
        "upright": "Kejujuran, keadilan, akuntabilitas, keseimbangan karma.",
        "reversed": "Ketidakadilan, kebohongan, kurang tanggung jawab.",
        "element": "Udara",
        "planet": "Libra",
        "color_accent": "#E0E0E0",
    },
    "the_hanged_man": {
        "title": "The Hanged Man",
        "number": "XII",
        "keywords": ["Pelepasan", "Perspektif Baru", "Pengorbanan"],
        "meaning": (
            "Terkadang, tidak bergerak adalah langkah terbaik. "
            "Lepaskan kebutuhan untuk mengontrol segalanya dan lihat dari sudut pandang berbeda. "
            "Pengorbanan kecil kini akan membuka jalan bagi berkah yang jauh lebih besar."
        ),
        "upright": "Melepaskan ego, perspektif unik, periode penantian.",
        "reversed": "Menunda, menolak melepaskan, pengorbanan sia-sia.",
        "element": "Air",
        "planet": "Neptunus",
        "color_accent": "#7EC8C8",
    },
    "death": {
        "title": "Death",
        "number": "XIII",
        "keywords": ["Transformasi", "Penutupan", "Kelahiran Baru"],
        "meaning": (
            "Kartu ini bukan tentang kematian fisik — ia adalah tentang akhir dari sebuah era. "
            "Sesuatu yang lama harus berakhir agar sesuatu yang baru dapat lahir. "
            "Sambut transformasi ini dengan berani, karena di baliknya menunggu kehidupan baru yang luar biasa."
        ),
        "upright": "Transformasi besar, akhir yang diperlukan, awal yang segar.",
        "reversed": "Menolak perubahan, terjebak masa lalu, ketakutan akan transformasi.",
        "element": "Air",
        "planet": "Scorpio",
        "color_accent": "#9370DB",
    },
    "temperance": {
        "title": "Temperance",
        "number": "XIV",
        "keywords": ["Keseimbangan", "Kesabaran", "Moderasi"],
        "meaning": (
            "Harmoni tercapai bukan melalui ekstrim, melainkan melalui keseimbangan yang bijaksana. "
            "Sabar dan biarkan segala sesuatu berjalan pada waktu yang tepat. "
            "Aliran energi kosmik sedang menyeimbangkan hidupmu dengan penuh kasih."
        ),
        "upright": "Moderasi, kesabaran, keseimbangan hidup, kedamaian batin.",
        "reversed": "Kelebihan, ketidaksabaran, ketidakseimbangan.",
        "element": "Api",
        "planet": "Sagitarius",
        "color_accent": "#98FB98",
    },
    "the_devil": {
        "title": "The Devil",
        "number": "XV",
        "keywords": ["Ikatan", "Godaan", "Bayangan Diri"],
        "meaning": (
            "Kamu mungkin terikat pada sesuatu yang menguras energi dan kebahagiaanmu. "
            "Rantai itu hanya ilusi — kamu memiliki kekuatan untuk membebaskan diri. "
            "Hadapi sisi gelapmu dengan jujur agar kamu bisa melangkah maju."
        ),
        "upright": "Ikatan yang membatasi, godaan, aspek gelap yang perlu dihadapi.",
        "reversed": "Membebaskan diri, melepaskan ketergantungan, pencerahan.",
        "element": "Bumi",
        "planet": "Capricorn",
        "color_accent": "#8B0000",
    },
    "the_tower": {
        "title": "The Tower",
        "number": "XVI",
        "keywords": ["Guncangan", "Wahyu", "Perubahan Mendadak"],
        "meaning": (
            "Fondasi yang dibangun di atas kebohongan atau ilusi akan runtuh. "
            "Meski menyakitkan, guncangan ini adalah berkah — ia membersihkan apa yang tidak lagi melayanimu. "
            "Dari reruntuhan, akan lahir sesuatu yang jauh lebih kokoh dan autentik."
        ),
        "upright": "Perubahan tiba-tiba, kehancuran ilusi, wahyu mengejutkan.",
        "reversed": "Menghindari kehancuran yang diperlukan, menunda perubahan.",
        "element": "Api",
        "planet": "Mars",
        "color_accent": "#FF4500",
    },
    "the_star": {
        "title": "The Star",
        "number": "XVII",
        "keywords": ["Harapan", "Pemulihan", "Ilham"],
        "meaning": (
            "Setelah badai, langit cerah selalu datang. "
            "Kartu bintang membawa angin segar harapan dan penyembuhan ke dalam hidupmu. "
            "Percayalah bahwa alam semesta sedang memandu langkahmu menuju cahaya."
        ),
        "upright": "Harapan baru, pemulihan, inspirasi kosmik, keyakinan.",
        "reversed": "Kehilangan harapan, keputusasaan, kurang percaya diri.",
        "element": "Udara",
        "planet": "Aquarius",
        "color_accent": "#87CEFA",
    },
    "the_moon": {
        "title": "The Moon",
        "number": "XVIII",
        "keywords": ["Ilusi", "Ketakutan", "Bawah Sadar"],
        "meaning": (
            "Tidak semua yang tampak adalah kenyataan. "
            "Ketakutan dan ilusi mungkin mengaburkan pandanganmu saat ini. "
            "Percayai intuisimu untuk menavigasi kegelapan ini — cahaya bulan akan menunjukkan jalan."
        ),
        "upright": "Ilusi, ketakutan tersembunyi, mimpi, bawah sadar aktif.",
        "reversed": "Kejernihan setelah kebingungan, menghadapi ketakutan.",
        "element": "Air",
        "planet": "Pisces",
        "color_accent": "#C3B1E1",
    },
    "the_sun": {
        "title": "The Sun",
        "number": "XIX",
        "keywords": ["Kegembiraan", "Suksess", "Vitalitas"],
        "meaning": (
            "Energi matahari sedang menyinari setiap aspek hidupmu dengan kehangatan dan keceriaan. "
            "Ini adalah waktu keberhasilan, kejelasan, dan kebahagiaan yang tulus. "
            "Rayakan keberadaanmu dan biarkan cahayamu bersinar terang."
        ),
        "upright": "Keberhasilan, kebahagiaan, vitalitas, kejernihan pikiran.",
        "reversed": "Optimisme berlebihan, ego membesar, kebahagiaan tertunda.",
        "element": "Api",
        "planet": "Matahari",
        "color_accent": "#FFD700",
    },
    "judgement": {
        "title": "Judgement",
        "number": "XX",
        "keywords": ["Kebangkitan", "Panggilan Jiwa", "Refleksi Akhir"],
        "meaning": (
            "Alam semesta memanggilmu untuk bangkit ke versi dirimu yang lebih tinggi. "
            "Ini saat refleksi mendalam — evaluasi masa lalumu dan lepaskan beban yang tidak perlu. "
            "Kebangkitan spiritualmu telah dimulai."
        ),
        "upright": "Kebangkitan, panggilan jiwa, refleksi, keputusan besar.",
        "reversed": "Menghindari evaluasi diri, kurang introspeksi, tidak mau berubah.",
        "element": "Api",
        "planet": "Pluto",
        "color_accent": "#FFB347",
    },
    "the_world": {
        "title": "The World",
        "number": "XXI",
        "keywords": ["Penyelesaian", "Integrasi", "Pencapaian"],
        "meaning": (
            "Sebuah siklus besar dalam hidupmu telah mencapai puncaknya. "
            "Rayakan pencapaianmu dan akui sejauh mana kamu telah berkembang. "
            "Dunia ini adalah milikmu — kamu telah memenangkan perjalanan kosmik ini."
        ),
        "upright": "Penyelesaian, pencapaian puncak, integrasi sempurna.",
        "reversed": "Siklus belum selesai, perlu lebih banyak pekerjaan, penundaan.",
        "element": "Bumi",
        "planet": "Saturnus",
        "color_accent": "#7FFFD4",
    },
}

CARD_KEYS = list(TAROT_DB.keys())


# ==============================================================================
# TAROT DECK — Data Layer
# ==============================================================================
class TarotDeck:
    """
    Manages the pool of tarot cards.
    Responsible for shuffling and drawing cards from the Major Arcana.
    Completely decoupled from any UI concerns.
    """

    def __init__(self):
        self._cards: list[str] = CARD_KEYS.copy()
        self._shuffled: list[str] = []
        self.shuffle()

    def shuffle(self) -> None:
        """Randomise the deck order."""
        self._shuffled = self._cards.copy()
        random.shuffle(self._shuffled)

    def draw_one(self) -> str:
        """Pop one card key from the shuffled deck (replenishes when empty)."""
        if not self._shuffled:
            self.shuffle()
        return self._shuffled.pop()

    def draw_many(self, n: int) -> list[str]:
        """Draw n distinct card keys."""
        if n > len(self._shuffled):
            self.shuffle()
        drawn, self._shuffled = self._shuffled[:n], self._shuffled[n:]
        return drawn

    def peek_daily(self) -> str:
        """
        Deterministically pick the same card for the current calendar day
        so 'Daily Tarot' does not change when the panel is re-opened.
        """
        import datetime
        day_seed = int(datetime.date.today().strftime("%Y%m%d"))
        rng = random.Random(day_seed)
        return rng.choice(CARD_KEYS)

    @staticmethod
    def get_card(key: str) -> dict:
        """Return the data dict for a given card key."""
        return TAROT_DB.get(key, {})


# ==============================================================================
# TAROT READING ENGINE — Business Logic Layer
# ==============================================================================
class TarotReadingEngine:
    """
    Orchestrates reading modes and produces the interpretation payload
    returned to the UI layer.

    Two reading modes are currently supported:
        - daily   : single-card draw pinned to today's date
        - pick    : n-card open draw for interactive selection
    """

    def __init__(self):
        self.deck = TarotDeck()

    def daily_reading(self) -> dict:
        """Return a complete reading dict for today's daily card."""
        key = self.deck.peek_daily()
        card = TAROT_DB[key]
        return {
            "mode": "daily",
            "keys": [key],
            "cards": [card],
        }

    def pick_reading(self, n: int = 3) -> dict:
        """Draw n cards for a Pick-A-Card session."""
        self.deck.shuffle()
        keys = self.deck.draw_many(n)
        cards = [TAROT_DB[k] for k in keys]
        return {
            "mode": "pick",
            "keys": keys,
            "cards": cards,
        }

    def refresh_shuffle(self) -> None:
        """Re-shuffle the deck (called by the Shuffle button)."""
        self.deck.shuffle()


# ==============================================================================
# HELPER — Asset path resolver
# ==============================================================================
def _asset_path(filename: str) -> str:
    """
    Returns the absolute path for a tarot asset image.
    Falls back gracefully if the file does not exist so the widget
    can still render a styled placeholder.
    """
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "tarot")
    return os.path.join(base, filename)


def _load_pixmap(card_key: str, fallback_color: str = "#1a0a3a") -> Optional[QPixmap]:
    """Load a card's PNG from assets/tarot/<key>.png. Returns None if missing."""
    path = _asset_path(f"{card_key}.png")
    if os.path.exists(path):
        return QPixmap(path)
    return None


def _load_back_pixmap() -> Optional[QPixmap]:
    path = _asset_path("card_back.png")
    if os.path.exists(path):
        return QPixmap(path)
    return None


def _play_whoosh():
    """
    Play assets/whoosh.wav asynchronously using winsound.
    Runs in a daemon thread so the UI is never blocked.
    Falls back silently on non-Windows platforms.
    """
    if not _WINSOUND_AVAILABLE:
        return
    wav_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "assets", "whoosh.wav"
    )
    if not os.path.exists(wav_path):
        return
    threading.Thread(
        target=winsound.PlaySound,
        args=(wav_path, winsound.SND_FILENAME),
        daemon=True,
    ).start()


# ==============================================================================
# TAROT CARD WIDGET — Interactive card with flip + glow animations
# ==============================================================================
class TarotCardWidget(QWidget):
    """
    Renders a single Tarot card face-down (showing card_back.png or a stylised
    back) and exposes:
        - hover glow effect (golden border + drop shadow)
        - flip animation (3D-simulated shrink → swap image → expand)
        - card_clicked signal emitted after the reveal

    The width-shrink/expand trick via QPropertyAnimation on _card_width is the
    classic Qt approach to simulating a 3D card flip without OpenGL.
    """

    card_clicked = Signal(str)   # emits the card key after flip completes

    # ------------------------------------------------------------------ init
    def __init__(self, card_key: str, face_up: bool = False, parent=None):
        super().__init__(parent)
        self.card_key = card_key
        self._face_up = face_up
        self._flipping = False
        self._hovering = False

        # Stored card data
        self._card_data = TAROT_DB.get(card_key, {})
        self._face_pixmap: Optional[QPixmap] = _load_pixmap(card_key)
        self._back_pixmap: Optional[QPixmap] = _load_back_pixmap()

        # The animated width property (used by the flip animation)
        self._card_width: int = 130

        self.setFixedSize(150, 240)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)

        # Drop-shadow glow (enhanced on hover)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(18)
        self._shadow.setColor(QColor(125, 44, 255, 120))
        self._shadow.setOffset(0, 0)
        self.setGraphicsEffect(self._shadow)

    # ------------------------------------------------------------------ Qt property for animation
    def _get_card_width(self) -> int:
        return self._card_width

    def _set_card_width(self, value: int):
        self._card_width = value
        self.update()          # repaint whenever the animated width changes

    # Expose as a real Qt Property so QPropertyAnimation can drive it
    cardWidth = Property(int, _get_card_width, _set_card_width)

    # ------------------------------------------------------------------ Hover
    def enterEvent(self, event):
        if not self._face_up and not self._flipping:
            self._hovering = True
            # Gold glow on hover
            self._shadow.setColor(QColor(255, 204, 51, 200))
            self._shadow.setBlurRadius(28)
            self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovering = False
        if not self._face_up:
            self._shadow.setColor(QColor(125, 44, 255, 120))
            self._shadow.setBlurRadius(18)
        self.update()
        super().leaveEvent(event)

    # ------------------------------------------------------------------ Click → flip
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._face_up and not self._flipping:
            self._start_flip()
        super().mousePressEvent(event)

    # ------------------------------------------------------------------ Flip animation
    def _start_flip(self):
        """
        3-stage flip simulation:
          Stage 1 — animate cardWidth → 0   (card 'turns away')
          Stage 2 — swap the displayed image at width=0  (invisible instant swap)
          Stage 3 — animate cardWidth → 150 (card 'turns back')

        QSequentialAnimationGroup chains stages automatically.
        """
        self._flipping = True
        self.setCursor(Qt.ArrowCursor)

        # Play whoosh sound at the moment the flip begins
        _play_whoosh()

        CARD_W = self.width()
        HALF_MS = 250       # ms for each half of the flip

        # --- Stage 1: shrink to 0
        shrink = QPropertyAnimation(self, b"cardWidth", self)
        shrink.setStartValue(CARD_W)
        shrink.setEndValue(0)
        shrink.setDuration(HALF_MS)
        shrink.setEasingCurve(QEasingCurve.InQuad)   # accelerates toward centre

        # --- Stage 3: expand back to full width
        expand = QPropertyAnimation(self, b"cardWidth", self)
        expand.setStartValue(0)
        expand.setEndValue(CARD_W)
        expand.setDuration(HALF_MS)
        expand.setEasingCurve(QEasingCurve.OutQuad)  # decelerates as it opens

        # Chain stages
        self._flip_seq = QSequentialAnimationGroup(self)
        self._flip_seq.addAnimation(shrink)
        self._flip_seq.addAnimation(expand)

        # At the invisible midpoint (shrink finished), swap the face
        shrink.finished.connect(self._reveal_face)
        self._flip_seq.finished.connect(self._flip_done)
        self._flip_seq.start()

    @Slot()
    def _reveal_face(self):
        """Called at the invisible midpoint of the flip to swap to the face image."""
        self._face_up = True
        # Upgrade glow to purple-gold for revealed state
        self._shadow.setColor(QColor(180, 100, 255, 180))
        self._shadow.setBlurRadius(35)
        self.update()

    @Slot()
    def _flip_done(self):
        """Called when the full flip animation completes."""
        self._flipping = False
        self.card_clicked.emit(self.card_key)

    # ------------------------------------------------------------------ Shuffle nudge animation
    def play_shuffle_nudge(self, delay_ms: int = 0):
        """
        Briefly tilts the card left/right to simulate being in a shuffled deck.
        Uses a QPropertyAnimation on the cardWidth as a cheap 'wobble' — because
        true rotation requires a QGraphicsScene. The visual impression is enough.
        """
        # We only nudge face-down cards in Pick-A-Card mode
        if self._face_up:
            return

        # Small width pulse: full → 90% → full  (gives a perspective-tilt feel)
        CARD_W = self.width()
        nudge = QPropertyAnimation(self, b"cardWidth", self)
        nudge.setKeyValueAt(0.0, CARD_W)
        nudge.setKeyValueAt(0.25, int(CARD_W * 0.85))
        nudge.setKeyValueAt(0.50, CARD_W)
        nudge.setKeyValueAt(0.75, int(CARD_W * 0.90))
        nudge.setKeyValueAt(1.0, CARD_W)
        nudge.setDuration(400)
        nudge.setEasingCurve(QEasingCurve.InOutSine)

        # Stagger each card slightly for a natural deck-shuffle impression
        QTimer.singleShot(delay_ms, nudge.start)
        self._nudge_anim = nudge   # keep reference so GC doesn't kill it

    # ------------------------------------------------------------------ Paint
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w, h = self.width(), self.height()
        # Centre offset so animation shrinks from the middle
        x_offset = (w - self._card_width) // 2

        rect = QRect(x_offset, 0, self._card_width, h)

        # ---- Background / rounded border
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 10, 10)

        if self._face_up:
            # Mystical face gradient
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0.0, QColor("#1a0640"))
            grad.setColorAt(1.0, QColor("#0b0220"))
            painter.fillPath(path, QBrush(grad))
        else:
            # Back-face dark gradient with subtle gold shimmer
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0.0, QColor("#12002f"))
            grad.setColorAt(0.5, QColor("#1e004a"))
            grad.setColorAt(1.0, QColor("#0b0220"))
            painter.fillPath(path, QBrush(grad))

        # ---- Border
        border_color = QColor("#ffcc33" if self._hovering else (
                               "#9d5fff" if self._face_up else "#4a1a7a"))
        painter.setPen(QPen(border_color, 1.5 if self._face_up else 1))
        painter.drawPath(path)

        # ---- Image
        if self._face_up and self._face_pixmap:
            img_rect = QRect(x_offset + 6, 6, self._card_width - 12, h - 12)
            painter.setClipPath(path)
            painter.drawPixmap(img_rect, self._face_pixmap.scaled(
                img_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            painter.setClipping(False)
        elif not self._face_up and self._back_pixmap:
            img_rect = QRect(x_offset + 6, 6, self._card_width - 12, h - 12)
            painter.setClipPath(path)
            painter.drawPixmap(img_rect, self._back_pixmap.scaled(
                img_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            painter.setClipping(False)
        else:
            # Fallback: decorative placeholder
            self._draw_placeholder(painter, rect, h)

        # ---- Hover overlay (golden shimmer)
        if self._hovering and not self._face_up:
            glow_path = QPainterPath()
            glow_path.addRoundedRect(QRectF(rect), 10, 10)
            painter.fillPath(glow_path, QBrush(QColor(255, 204, 51, 18)))

    def _draw_placeholder(self, painter: QPainter, rect: QRect, h: int):
        """Decorative fallback when no PNG asset is found."""
        cx = rect.x() + rect.width() // 2
        cy = h // 2

        if self._face_up:
            data = self._card_data
            # Card number circle
            painter.setPen(QPen(QColor("#ffcc33"), 1))
            painter.setBrush(QBrush(QColor(125, 44, 255, 60)))
            painter.drawEllipse(cx - 28, cy - 48, 56, 56)

            # Roman numeral
            num_font = QFont("Segoe UI", 13, QFont.Bold)
            painter.setFont(num_font)
            painter.setPen(QColor("#ffcc33"))
            painter.drawText(QRect(rect.x(), cy - 48, rect.width(), 56),
                             Qt.AlignCenter, data.get("number", "?"))

            # Title
            title_font = QFont("Segoe UI", 7, QFont.Bold)
            painter.setFont(title_font)
            painter.setPen(QColor("#e2d4ff"))
            painter.drawText(QRect(rect.x(), cy + 16, rect.width(), 30),
                             Qt.AlignCenter | Qt.TextWordWrap,
                             data.get("title", "Unknown"))
        else:
            # Back pattern — concentric diamonds
            painter.setPen(QPen(QColor(125, 44, 255, 80), 1))
            painter.setBrush(Qt.NoBrush)
            for i in range(4):
                r = 20 + i * 14
                diamond = QPainterPath()
                diamond.moveTo(cx,     cy - r)
                diamond.lineTo(cx + r, cy)
                diamond.lineTo(cx,     cy + r)
                diamond.lineTo(cx - r, cy)
                diamond.closeSubpath()
                painter.drawPath(diamond)

            # Centre star glyph
            painter.setPen(QPen(QColor("#ffcc33"), 1))
            star_font = QFont("Segoe UI", 16)
            painter.setFont(star_font)
            painter.drawText(QRect(rect.x(), cy - 14, rect.width(), 28),
                             Qt.AlignCenter, "✦")


# ==============================================================================
# TAROT PANEL — Top-level view widget
# ==============================================================================
class TarotPanel(QWidget):
    """
    The main Tarot module panel, designed to be inserted into the
    MacanPeramalWindow's QStackedWidget just like every other view.

    Layout (vertical):
        ┌────────────────────────────────────────┐
        │  Header (title + subtitle)             │
        ├────────────────────────────────────────┤
        │  Mode tabs: [Daily Tarot] [Pick A Card]│
        ├────────────────────────────────────────┤
        │  QStackedWidget                        │
        │    page 0 → Daily Tarot view           │
        │    page 1 → Pick A Card view           │
        ├────────────────────────────────────────┤
        │  Interpretation panel (scrollable)     │
        └────────────────────────────────────────┘
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._engine = TarotReadingEngine()
        self._pick_cards: list[TarotCardWidget] = []
        self._current_mode = "daily"
        self._setup_ui()
        # Auto-load today's daily card
        QTimer.singleShot(300, self._load_daily)

    # ------------------------------------------------------------------ UI build
    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(0)

        # ---- Header
        header = self._make_header()
        root.addWidget(header)
        root.addSpacing(20)

        # ---- Mode toggle tabs
        tabs = self._make_mode_tabs()
        root.addLayout(tabs)
        root.addSpacing(20)

        # ---- Card display area (stacked)
        self._card_stack = QStackedWidget()
        self._card_stack.setMinimumHeight(300)
        self._page_daily = self._make_daily_page()
        self._page_pick  = self._make_pick_page()
        self._card_stack.addWidget(self._page_daily)
        self._card_stack.addWidget(self._page_pick)
        root.addWidget(self._card_stack)
        root.addSpacing(22)

        # ---- Interpretation / result area
        interp = self._make_interpretation_area()
        root.addWidget(interp, 1)   # stretch factor=1 so it fills remaining space

    # ------------------------------------------------------------------ Header
    def _make_header(self) -> QWidget:
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        title = QLabel("🃏  Tarot Reading")
        title.setStyleSheet("""
            color: #FFD700;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        subtitle = QLabel("Biarkan kartu-kartu kosmik mengungkap pesan alam semesta untukmu")
        subtitle.setStyleSheet("color: #8C84A9; font-size: 12px; font-style: italic;")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Thin gold separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #2B1B4D; background: #2B1B4D; max-height: 1px;")
        layout.addSpacing(10)
        layout.addWidget(sep)
        return frame

    # ------------------------------------------------------------------ Mode tabs
    def _make_mode_tabs(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self._btn_daily = self._tab_button("🌙  Tarot Harian", active=True)
        self._btn_pick  = self._tab_button("✨  Pick A Card",  active=False)
        self._btn_shuffle = self._action_button("🔮  Shuffle Deck")

        self._btn_daily.clicked.connect(lambda: self._switch_mode("daily"))
        self._btn_pick.clicked.connect(lambda: self._switch_mode("pick"))
        self._btn_shuffle.clicked.connect(self._on_shuffle)

        layout.addWidget(self._btn_daily)
        layout.addWidget(self._btn_pick)
        layout.addStretch()
        layout.addWidget(self._btn_shuffle)
        return layout

    def _tab_button(self, text: str, active: bool) -> QPushButton:
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(active)
        btn.setStyleSheet(self._tab_qss())
        btn.setFixedHeight(36)
        return btn

    def _action_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(36)
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #6C33A3, stop:1 #491E74);
                border: 1px solid #8B4AD4;
                border-radius: 6px;
                color: #F8F7FF;
                padding: 0 18px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #8442C4, stop:1 #5B278D);
                border: 1px solid #FFD700;
            }
            QPushButton:pressed { background: #391559; }
        """)
        return btn

    @staticmethod
    def _tab_qss() -> str:
        return """
            QPushButton {
                background: transparent;
                border: 1px solid #2B1B4D;
                border-radius: 6px;
                color: #8C84A9;
                padding: 0 18px;
                font-size: 12px;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #3D1C6E, stop:1 #251148);
                border: 1px solid #7d2cff;
                color: #FFD700;
                font-weight: bold;
            }
            QPushButton:hover:!checked {
                border: 1px solid #6A329F;
                color: #D4C8FF;
            }
        """

    # ------------------------------------------------------------------ Daily page
    def _make_daily_page(self) -> QWidget:
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        # Placeholder card slot — filled at runtime
        self._daily_card_slot = QHBoxLayout()
        self._daily_card_slot.setAlignment(Qt.AlignCenter)

        # Right: daily keyword summary
        self._daily_info = QFrame()
        self._daily_info.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #140F2D, stop:1 #0D0A20);
                border: 1px solid #351C5E;
                border-radius: 12px;
            }
        """)
        info_lay = QVBoxLayout(self._daily_info)
        info_lay.setContentsMargins(20, 20, 20, 20)
        info_lay.setSpacing(8)

        self._lbl_daily_date = QLabel()
        self._lbl_daily_date.setStyleSheet("color:#5A5475; font-size:11px;")

        self._lbl_daily_title = QLabel("—")
        self._lbl_daily_title.setStyleSheet(
            "color:#FFD700; font-size:17px; font-weight:bold; letter-spacing:1px;")

        self._lbl_daily_num = QLabel("")
        self._lbl_daily_num.setStyleSheet("color:#7d2cff; font-size:12px;")

        self._lbl_daily_keywords = QLabel("")
        self._lbl_daily_keywords.setStyleSheet(
            "color:#B19FFC; font-size:12px; font-style:italic;")
        self._lbl_daily_keywords.setWordWrap(True)

        self._lbl_daily_element = QLabel("")
        self._lbl_daily_element.setStyleSheet("color:#8C84A9; font-size:11px;")

        info_lay.addWidget(self._lbl_daily_date)
        info_lay.addSpacing(4)
        info_lay.addWidget(self._lbl_daily_title)
        info_lay.addWidget(self._lbl_daily_num)
        info_lay.addSpacing(6)
        info_lay.addWidget(self._lbl_daily_keywords)
        info_lay.addSpacing(4)
        info_lay.addWidget(self._lbl_daily_element)
        info_lay.addStretch()

        self._daily_info.setMinimumWidth(240)

        layout.addLayout(self._daily_card_slot)
        layout.addWidget(self._daily_info)
        return page

    # ------------------------------------------------------------------ Pick page
    def _make_pick_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        prompt = QLabel("✦  Pilih satu kartu yang menarik perhatianmu  ✦")
        prompt.setAlignment(Qt.AlignCenter)
        prompt.setStyleSheet("color:#B19FFC; font-size:13px; font-style:italic;")
        layout.addWidget(prompt)

        self._pick_row = QHBoxLayout()
        self._pick_row.setSpacing(24)
        self._pick_row.setAlignment(Qt.AlignCenter)
        layout.addLayout(self._pick_row)
        return page

    # ------------------------------------------------------------------ Interpretation area
    def _make_interpretation_area(self) -> QWidget:
        outer = QFrame()
        outer.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #0E0921, stop:1 #0b0220);
                border: 1px solid #2B1B4D;
                border-radius: 12px;
            }
        """)
        outer.setMinimumHeight(140)
        outer_lay = QVBoxLayout(outer)
        outer_lay.setContentsMargins(20, 16, 20, 16)
        outer_lay.setSpacing(6)

        header_row = QHBoxLayout()
        lbl_section = QLabel("✦  Interpretasi Kosmik")
        lbl_section.setStyleSheet(
            "color:#FFD700; font-size:13px; font-weight:bold; letter-spacing:1px;")
        header_row.addWidget(lbl_section)
        header_row.addStretch()

        outer_lay.addLayout(header_row)

        # Scrollable text area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._interp_label = QLabel(
            "Pilih mode membaca dan kartu akan mengungkap pesannya…")
        self._interp_label.setWordWrap(True)
        self._interp_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self._interp_label.setStyleSheet(
            "color:#C8C0E0; font-size:13px; line-height: 160%; background: transparent;")
        self._interp_label.setTextFormat(Qt.RichText)

        scroll.setWidget(self._interp_label)
        outer_lay.addWidget(scroll, 1)
        return outer

    # ------------------------------------------------------------------ Mode switching
    def _switch_mode(self, mode: str):
        self._current_mode = mode
        self._btn_daily.setChecked(mode == "daily")
        self._btn_pick.setChecked(mode == "pick")

        if mode == "daily":
            self._card_stack.setCurrentIndex(0)
            self._load_daily()
        else:
            self._card_stack.setCurrentIndex(1)
            self._load_pick()

    # ------------------------------------------------------------------ Daily logic
    def _load_daily(self):
        """Populate the Daily Tarot page with today's card."""
        import datetime
        reading = self._engine.daily_reading()
        key = reading["keys"][0]
        card = reading["cards"][0]

        # Remove old card widget if any
        while self._daily_card_slot.count():
            item = self._daily_card_slot.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create card widget (face-up for daily — no interaction needed)
        card_w = TarotCardWidget(key, face_up=True)
        # Apply a subtle permanent purple glow for the daily card
        glow = QGraphicsDropShadowEffect(card_w)
        glow.setBlurRadius(40)
        glow.setColor(QColor(125, 44, 255, 160))
        glow.setOffset(0, 0)
        card_w.setGraphicsEffect(glow)
        self._daily_card_slot.addWidget(card_w)

        # Update info labels
        today = datetime.date.today()
        self._lbl_daily_date.setText(
            f"Tarot Harian — {today.strftime('%A, %d %B %Y')}")
        self._lbl_daily_title.setText(card.get("title", "Unknown").upper())
        self._lbl_daily_num.setText(f"Arkana Major  ·  {card.get('number', '')}")
        keywords = "  ·  ".join(card.get("keywords", []))
        self._lbl_daily_keywords.setText(f"✦  {keywords}")
        element_planet = (
            f"Elemen: {card.get('element', '—')}   "
            f"Planet: {card.get('planet', '—')}"
        )
        self._lbl_daily_element.setText(element_planet)

        # Interpretation
        self._show_interpretation(card)

    # ------------------------------------------------------------------ Pick logic
    def _load_pick(self, reshuffled: bool = False):
        """Populate Pick-A-Card with 3 face-down cards."""
        # Clear existing cards
        self._pick_cards.clear()
        while self._pick_row.count():
            item = self._pick_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Draw 3 cards from the deck
        reading = self._engine.pick_reading(3)

        for i, key in enumerate(reading["keys"]):
            card_w = TarotCardWidget(key, face_up=False)
            card_w.card_clicked.connect(self._on_pick_card_clicked)
            self._pick_row.addWidget(card_w)
            self._pick_cards.append(card_w)

        if reshuffled:
            # Play staggered nudge animation on all 3 cards
            for i, cw in enumerate(self._pick_cards):
                cw.play_shuffle_nudge(delay_ms=i * 120)

        self._interp_label.setText(
            "✦  Tenangkan pikiranmu…  Fokuskan niatmu…  "
            "Lalu pilih satu kartu yang terasa memanggil jiwamu.  ✦"
        )

    @Slot(str)
    def _on_pick_card_clicked(self, card_key: str):
        """Called when the user flips a pick-a-card card."""
        card = TAROT_DB.get(card_key, {})

        # Disable the other cards so only one can be flipped
        for cw in self._pick_cards:
            if cw.card_key != card_key:
                cw.setEnabled(False)
                cw.setStyleSheet("opacity: 0.4;")

        # Show a 'personal reading' interpretation
        self._show_interpretation(card, mode="pick")

        # Offer reshuffle below
        QTimer.singleShot(600, self._show_reshuffle_hint)

    def _show_reshuffle_hint(self):
        current = self._interp_label.text()
        if "🔮" not in current:
            self._interp_label.setText(
                current +
                "<br><br><span style='color:#5A5475; font-size:11px;'>"
                "Klik  🔮 Shuffle Deck  untuk sesi pembacaan baru.</span>"
            )

    # ------------------------------------------------------------------ Shuffle
    def _on_shuffle(self):
        """
        Shuffle the deck then refresh the active page.

        For Daily mode: re-shuffling has no visible effect on the result since
        daily card is date-seeded, but we still play the animation.
        For Pick mode: draws 3 new cards and plays the nudge animation.
        """
        self._engine.refresh_shuffle()

        if self._current_mode == "pick":
            self._load_pick(reshuffled=True)
        else:
            # Play a visual shuffle pulse on the existing daily card
            if self._daily_card_slot.count():
                item = self._daily_card_slot.itemAt(0)
                if item and item.widget():
                    cw: TarotCardWidget = item.widget()
                    cw.play_shuffle_nudge(delay_ms=0)
            self._load_daily()

    # ------------------------------------------------------------------ Interpretation renderer
    def _show_interpretation(self, card: dict, mode: str = "daily"):
        title = card.get("title", "Unknown")
        meaning = card.get("meaning", "")
        upright = card.get("upright", "")
        reversed_ = card.get("reversed", "")
        keywords = card.get("keywords", [])
        accent = card.get("color_accent", "#B19FFC")

        if mode == "daily":
            prefix_html = (
                f"<span style='color:#5A5475; font-size:11px;'>TAROT HARIAN</span><br>"
                f"<span style='color:{accent}; font-size:16px; font-weight:bold; "
                f"letter-spacing:1px;'>{title.upper()}</span><br><br>"
            )
        else:
            prefix_html = (
                f"<span style='color:#5A5475; font-size:11px;'>KARTU PILIHANMU</span><br>"
                f"<span style='color:{accent}; font-size:16px; font-weight:bold; "
                f"letter-spacing:1px;'>{title.upper()}</span><br><br>"
            )

        keywords_html = (
            "<span style='color:#7d2cff; font-size:12px;'>"
            + "  ✦  ".join(keywords) +
            "</span><br><br>"
        )

        meaning_html = (
            f"<span style='color:#C8C0E0; font-size:13px; line-height:170%;'>"
            f"{meaning}</span><br><br>"
        )

        upright_html = (
            f"<span style='color:#5A5475; font-size:11px;'>✅ Tegak: </span>"
            f"<span style='color:#A8D8B0; font-size:12px;'>{upright}</span><br>"
        )
        reversed_html = (
            f"<span style='color:#5A5475; font-size:11px;'>🔄 Terbalik: </span>"
            f"<span style='color:#D8A8A8; font-size:12px;'>{reversed_}</span>"
        )

        full_html = (
            prefix_html + keywords_html +
            meaning_html + upright_html + reversed_html
        )

        self._interp_label.setText(full_html)


# ==============================================================================
# STANDALONE TEST ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Apply the same base palette as the main app
    app.setStyleSheet("""
        QWidget { background-color: #0B0816; color: #E2E1E6;
                  font-family: "Segoe UI", Arial; font-size: 13px; }
        QScrollBar:vertical { border:none; background:#0B0816; width:8px; }
        QScrollBar::handle:vertical { background:#4E2C7E; border-radius:4px; min-height:20px; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
    """)

    win = QMainWindow()
    win.setWindowTitle("Macan Peramal — Tarot Module Test")
    win.setMinimumSize(900, 640)

    panel = TarotPanel()
    win.setCentralWidget(panel)
    win.show()

    sys.exit(app.exec())
