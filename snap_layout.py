# =============================================================================
# snap_layout.py — Modul Reusable Snap Window Layout (Windows 11 Style)
# =============================================================================
# Cara pakai:
#   from snap_layout import SnapLayoutOverlay
#
#   self._snap_overlay = SnapLayoutOverlay()
#   self._snap_overlay.snapRequested.connect(self.apply_snap_layout)
#
#   # Di eventFilter / hover handler tombol maximize:
#   self._snap_overlay.show_above(self.max_btn, is_maximized=self.isMaximized())
#   self._snap_overlay.schedule_hide()
#   self._snap_overlay.cancel_hide()
# =============================================================================

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel, QPushButton, QApplication
)
from PySide6.QtCore import Qt, QTimer, QPoint, QRect, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QEvent


# =============================================================================
# Layout Presets — setiap preset adalah satu "kartu grup" zona snap
# Format tuple: (zone_id, tooltip, row, col, rowspan, colspan)
#
# Preset ini mencerminkan screenshot: 2 baris grup, masing-masing dengan
# kombinasi zona yang berbeda, persis seperti Windows 11 Snap Layouts.
# =============================================================================

SNAP_LAYOUT_PRESETS = [
    # ── Grup 1: Full-screen (1 zona besar) ──────────────────────────────────
    {
        "id": "preset_full",
        "zones": [
            ("full", "Full Screen", 0, 0, 2, 4),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 2: Half-Half kiri-kanan ─────────────────────────────────────────
    {
        "id": "preset_halves",
        "zones": [
            ("left",  "Left Half",  0, 0, 2, 2),
            ("right", "Right Half", 0, 2, 2, 2),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 3: 1/3 kiri + 2/3 kanan ────────────────────────────────────────
    {
        "id": "preset_third_wide",
        "zones": [
            ("left_third",   "Left Third",         0, 0, 2, 1),
            ("right_twothird","Right Two-Thirds",  0, 1, 2, 3),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 4: 2/3 kiri + 1/3 kanan ────────────────────────────────────────
    {
        "id": "preset_wide_third",
        "zones": [
            ("left_twothird", "Left Two-Thirds",  0, 0, 2, 3),
            ("right_third",   "Right Third",       0, 3, 2, 1),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 5: Quarter kiri atas + Quarter kanan atas + Bottom half ─────────
    {
        "id": "preset_top2_bottom",
        "zones": [
            ("topleft",  "Top-Left Quarter",  0, 0, 1, 2),
            ("topright", "Top-Right Quarter", 0, 2, 1, 2),
            ("bottom",   "Bottom Half",       1, 0, 1, 4),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 6: Left half + Top-right quarter + Bottom-right quarter ─────────
    {
        "id": "preset_left_tworight",
        "zones": [
            ("left",         "Left Half",          0, 0, 2, 2),
            ("topright",     "Top-Right Quarter",  0, 2, 1, 2),
            ("bottomright",  "Bottom-Right Quarter",1,2, 1, 2),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 7: Top-left + Bottom-left + Right half ──────────────────────────
    {
        "id": "preset_twoLeft_right",
        "zones": [
            ("topleft",      "Top-Left Quarter",    0, 0, 1, 2),
            ("bottomleft",   "Bottom-Left Quarter", 1, 0, 1, 2),
            ("right",        "Right Half",          0, 2, 2, 2),
        ],
        "cols": 4,
        "rows": 2,
    },

    # ── Grup 8: Quarter Grid (4 penjuru) ────────────────────────────────────
    {
        "id": "preset_quarters",
        "zones": [
            ("topleft",     "Top-Left Quarter",     0, 0, 1, 2),
            ("topright",    "Top-Right Quarter",    0, 2, 1, 2),
            ("bottomleft",  "Bottom-Left Quarter",  1, 0, 1, 2),
            ("bottomright", "Bottom-Right Quarter", 1, 2, 1, 2),
        ],
        "cols": 4,
        "rows": 2,
    },
]


# =============================================================================
# Pemetaan zone_id ke geometri aktual layar
# Bisa di-extend sesuai kebutuhan
# =============================================================================

def compute_snap_geometry(zone_id: str, avail: QRect) -> QRect | None:
    """
    Hitung QRect dari zone_id berdasarkan available screen geometry.
    Return None jika zone_id tidak dikenal.
    """
    x, y, w, h = avail.x(), avail.y(), avail.width(), avail.height()
    half_w = w // 2
    half_h = h // 2
    third_w = w // 3
    two_third_w = w - third_w

    mapping = {
        "full":          None,  # Handled via showMaximized()
        "left":          QRect(x,            y,      half_w,      h),
        "right":         QRect(x + half_w,   y,      w - half_w,  h),
        "topleft":       QRect(x,            y,      half_w,      half_h),
        "topright":      QRect(x + half_w,   y,      w - half_w,  half_h),
        "bottomleft":    QRect(x,            y + half_h, half_w,  h - half_h),
        "bottomright":   QRect(x + half_w,   y + half_h, w-half_w,h - half_h),
        "bottom":        QRect(x,            y + half_h, w,       h - half_h),
        "left_third":    QRect(x,            y,      third_w,     h),
        "right_twothird":QRect(x + third_w,  y,      two_third_w, h),
        "left_twothird": QRect(x,            y,      two_third_w, h),
        "right_third":   QRect(x + two_third_w, y,   third_w,    h),
    }
    return mapping.get(zone_id)


# =============================================================================
# SnapLayoutOverlay — Widget popup reusable
# =============================================================================

class SnapLayoutOverlay(QWidget):
    """
    Popup Windows-11-style Snap Layout.

    Menampilkan preset zona snap dalam grid 4 kolom × 2 baris.
    Preset dikelompokkan dalam kartu-kartu kecil, persis seperti
    tampilan snap layout Windows 11.

    Signal:
        snapRequested(str) — dikirim saat user klik zona, berisi zone_id

    Cara pakai:
        overlay = SnapLayoutOverlay()
        overlay.snapRequested.connect(handler)

        # Tampilkan di bawah tombol maximize:
        overlay.show_above(max_button, is_maximized=self.isMaximized())

        # Sembunyikan dengan delay (pasang di leaveEvent tombol):
        overlay.schedule_hide()
        overlay.cancel_hide()
    """

    snapRequested = Signal(str)

    # Dimensi satu "sel" zona dalam kartu
    CELL_W = 32
    CELL_H = 22
    CELL_GAP = 3
    CARD_GAP = 6          # Jarak antar kartu preset
    CARD_COLS = 2         # Jumlah kartu per baris
    SAFE_MARGIN = 12      # Margin aman dari tepi layar

    def __init__(self, parent=None):
        super().__init__(
            parent,
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self._anchor_widget: QWidget | None = None
        self._is_maximized: bool = False

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.setInterval(300)
        self._hide_timer.timeout.connect(self._check_hide)

        self._build_ui()
        self._setup_fade()

    # ------------------------------------------------------------------
    # UI Builder
    # ------------------------------------------------------------------

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._card = QFrame(self)
        self._card.setObjectName("snapCard")
        self._card.setStyleSheet("""
            QFrame#snapCard {
                background: rgba(28, 28, 30, 240);
                border: 1px solid rgba(255, 255, 255, 0.13);
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(10, 8, 10, 10)
        card_layout.setSpacing(6)

        # ── Judul ─────────────────────────────────────────────────────
        title_lbl = QLabel("Snap Layout")
        title_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.50); font-size: 10px;"
            "font-weight: 500; background: transparent; letter-spacing: 0.5px;"
        )
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_lbl)

        # ── Grid preset ────────────────────────────────────────────────
        presets_grid = QGridLayout()
        presets_grid.setContentsMargins(0, 0, 0, 0)
        presets_grid.setSpacing(self.CARD_GAP)

        self._zone_btns: dict[str, list[QPushButton]] = {}  # preset_id → [btn, ...]
        self._btn_zone_map: dict[QPushButton, str] = {}     # btn → zone_id
        self._btn_preset_map: dict[QPushButton, str] = {}   # btn → preset_id

        total_presets = len(SNAP_LAYOUT_PRESETS)
        for p_idx, preset in enumerate(SNAP_LAYOUT_PRESETS):
            preset_id = preset["id"]
            p_row = p_idx // self.CARD_COLS
            p_col = p_idx % self.CARD_COLS

            # Mini-kartu per preset
            mini_card = QFrame()
            mini_card.setObjectName(f"miniCard_{preset_id}")
            mini_card.setStyleSheet("""
                QFrame {
                    background: transparent;
                    border: none;
                }
            """)

            mini_layout = QGridLayout(mini_card)
            mini_layout.setContentsMargins(0, 0, 0, 0)
            mini_layout.setSpacing(self.CELL_GAP)

            preset_btns = []
            for zone_id, tooltip, row, col, rspan, cspan in preset["zones"]:
                btn = QPushButton()
                btn_w = self.CELL_W * cspan + self.CELL_GAP * (cspan - 1)
                btn_h = self.CELL_H * rspan + self.CELL_GAP * (rspan - 1)
                btn.setFixedSize(btn_w, btn_h)
                btn.setToolTip(tooltip)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet(self._zone_style(False))
                btn.installEventFilter(self)
                btn.clicked.connect(
                    lambda checked=False, z=zone_id: self._on_zone_clicked(z)
                )
                mini_layout.addWidget(btn, row, col, rspan, cspan)
                preset_btns.append(btn)
                self._btn_zone_map[btn] = zone_id
                self._btn_preset_map[btn] = preset_id

            self._zone_btns[preset_id] = preset_btns
            presets_grid.addWidget(mini_card, p_row, p_col)

        card_layout.addLayout(presets_grid)
        outer.addWidget(self._card)
        self.adjustSize()

    # ------------------------------------------------------------------
    # Styles
    # ------------------------------------------------------------------

    def _zone_style(self, hovered: bool) -> str:
        if hovered:
            return """
                QPushButton {
                    background: rgba(10, 132, 255, 0.92);
                    border: 1px solid rgba(10, 160, 255, 0.85);
                    border-radius: 4px;
                }
            """
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.10);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 4px;
            }
            QPushButton:hover {
                background: rgba(10, 132, 255, 0.80);
                border: 1px solid rgba(10, 160, 255, 0.75);
            }
        """

    def _zone_style_sibling(self) -> str:
        """Style untuk zona saudara (dalam preset yang sama) saat satu zona di-hover."""
        return """
            QPushButton {
                background: rgba(10, 132, 255, 0.30);
                border: 1px solid rgba(10, 160, 255, 0.40);
                border-radius: 4px;
            }
        """

    # ------------------------------------------------------------------
    # Fade animation
    # ------------------------------------------------------------------

    def _setup_fade(self):
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._fade_anim.setDuration(130)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show_above(self, anchor_widget: QWidget, is_maximized: bool = False):
        """
        Tampilkan overlay di bawah anchor_widget.

        Saat is_maximized=True (window sedang maximize/fullscreen),
        posisi dihitung dari koordinat global anchor_widget agar tidak
        terpotong di tepi layar, dan pastikan overlay tampil sepenuhnya
        di dalam batas layar yang tersedia.

        Args:
            anchor_widget: Tombol yang menjadi acuan posisi (biasanya max_btn)
            is_maximized:  True jika window sedang dalam kondisi maximized/fullscreen
        """
        self._anchor_widget = anchor_widget
        self._is_maximized = is_maximized

        self.adjustSize()
        ow = self.width()
        oh = self.height()

        # Posisi dasar: tepat di bawah anchor button
        global_anchor = anchor_widget.mapToGlobal(
            QPoint(anchor_widget.width() // 2, anchor_widget.height() + 4)
        )
        x = global_anchor.x() - ow // 2
        y = global_anchor.y()

        # Cari screen yang relevan berdasarkan posisi anchor
        screen = QApplication.screenAt(global_anchor)
        if screen is None:
            screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()

        # Clamp agar tidak keluar batas layar (kiri, kanan, bawah)
        x = max(avail.x() + self.SAFE_MARGIN, x)
        x = min(avail.right() - ow - self.SAFE_MARGIN, x)

        # Jika terlalu ke bawah (kasus jarang), munculkan di atas anchor
        if y + oh > avail.bottom() - self.SAFE_MARGIN:
            anchor_top = anchor_widget.mapToGlobal(QPoint(0, 0)).y()
            y = anchor_top - oh - 4

        self.move(x, y)
        self._opacity_effect.setOpacity(0.0)
        self.show()
        self.raise_()
        self._fade_anim.stop()
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def hide_overlay(self):
        """Fade-out lalu sembunyikan overlay."""
        self._fade_anim.stop()
        self._fade_anim.setStartValue(self._opacity_effect.opacity())
        self._fade_anim.setEndValue(0.0)
        # Pastikan tidak ada duplikat connection
        try:
            self._fade_anim.finished.disconnect(self._do_hide)
        except RuntimeError:
            pass
        self._fade_anim.finished.connect(self._do_hide)
        self._fade_anim.start()

    def schedule_hide(self):
        """Jadwalkan sembunyikan setelah delay singkat."""
        self._hide_timer.start()

    def cancel_hide(self):
        """Batalkan jadwal sembunyi."""
        self._hide_timer.stop()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _do_hide(self):
        try:
            self._fade_anim.finished.disconnect(self._do_hide)
        except RuntimeError:
            pass
        self.hide()

    def _check_hide(self):
        """Sembunyikan kalau mouse tidak di atas overlay."""
        if not self.underMouse():
            self.hide_overlay()

    def _on_zone_clicked(self, zone_id: str):
        self.hide()
        self.snapRequested.emit(zone_id)

    def _highlight_preset(self, hovered_btn: QPushButton | None, active_btn: QPushButton | None):
        """
        Saat salah satu btn di-hover:
        - btn yang di-hover → highlighted penuh
        - btn lain dalam preset yang sama → highlight redup (sibling)
        - btn di preset lain → normal
        """
        active_preset = self._btn_preset_map.get(active_btn) if active_btn else None

        for preset_id, btns in self._zone_btns.items():
            for btn in btns:
                if btn is active_btn:
                    btn.setStyleSheet(self._zone_style(True))
                elif preset_id == active_preset:
                    btn.setStyleSheet(self._zone_style_sibling())
                else:
                    btn.setStyleSheet(self._zone_style(False))

    def eventFilter(self, obj, event):
        if isinstance(obj, QPushButton) and obj in self._btn_zone_map:
            if event.type() == QEvent.Type.Enter:
                self._highlight_preset(obj, obj)
            elif event.type() == QEvent.Type.Leave:
                self._highlight_preset(None, None)
        return super().eventFilter(obj, event)

    def leaveEvent(self, event):
        self.schedule_hide()

    def enterEvent(self, event):
        self.cancel_hide()


# =============================================================================
# SnapLayoutMixin — Mixin untuk QWidget/QMainWindow yang ingin pakai snap
# =============================================================================

class SnapLayoutMixin:
    """
    Mixin yang bisa ditambahkan ke QWidget / QMainWindow agar mendapatkan
    fitur snap layout otomatis pada tombol maximize.

    Cara pakai:
        class MyWindow(SnapLayoutMixin, QWidget):
            def __init__(self):
                super().__init__()
                self.max_btn = QPushButton("□")
                self.init_snap_layout(self.max_btn)

            def apply_snap_layout(self, zone: str):
                # Override untuk handle snap behavior
                ...

    Metode yang HARUS diimplementasikan oleh kelas pemilik:
        apply_snap_layout(zone: str)   — dipanggil saat zona diklik
        isMaximized() -> bool          — sudah tersedia dari QWidget
        isFullScreen() -> bool         — sudah tersedia dari QWidget
        showNormal()                   — sudah tersedia dari QWidget
    """

    def init_snap_layout(self, max_btn: QPushButton, hover_delay_ms: int = 400):
        """
        Inisialisasi snap layout. Panggil di __init__ setelah max_btn dibuat.

        Args:
            max_btn:        Tombol maximize yang akan memicu overlay
            hover_delay_ms: Delay (ms) sebelum overlay muncul saat hover
        """
        self._snap_overlay = SnapLayoutOverlay()
        self._snap_overlay.snapRequested.connect(self._on_snap_requested)
        self._snap_max_btn = max_btn
        self._snap_max_btn.installEventFilter(self)

        self._snap_hover_timer = QTimer(self)
        self._snap_hover_timer.setSingleShot(True)
        self._snap_hover_timer.setInterval(hover_delay_ms)
        self._snap_hover_timer.timeout.connect(self._show_snap_overlay)

    def _show_snap_overlay(self):
        """Tampilkan overlay jika mouse masih di tombol maximize."""
        if hasattr(self, "_snap_overlay") and self._snap_max_btn.underMouse():
            self._snap_overlay.show_above(
                self._snap_max_btn,
                is_maximized=self.isMaximized() or self.isFullScreen(),
            )

    def _on_snap_requested(self, zone: str):
        """Relay dari overlay ke handler di kelas pemilik."""
        self.apply_snap_layout(zone)

    def apply_snap_layout(self, zone: str):
        """
        Default implementation: snap window ke geometri yang sesuai.
        Override untuk perilaku kustom (misal: animasi, update ikon, dsb).
        """
        from PySide6.QtWidgets import QApplication

        if self.isFullScreen() or self.isMaximized():
            self.showNormal()
            QTimer.singleShot(80, lambda: self._do_snap(zone))
        else:
            self._do_snap(zone)

    def _do_snap(self, zone: str):
        """Terapkan geometri snap ke window."""
        from PySide6.QtWidgets import QApplication

        screen = QApplication.screenAt(self.geometry().center())
        if screen is None:
            screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()

        if zone == "full":
            self.showMaximized()
            return

        geom = compute_snap_geometry(zone, avail)
        if geom is not None:
            self.showNormal()
            self.setGeometry(geom)

    def snap_event_filter(self, obj, event):
        """
        Pasang ini di eventFilter() milik kelas pemilik untuk mendeteksi
        hover pada tombol maximize:

            def eventFilter(self, obj, event):
                if self.snap_event_filter(obj, event):
                    return True
                return super().eventFilter(obj, event)
        """
        if not hasattr(self, "_snap_max_btn"):
            return False
        if obj is self._snap_max_btn:
            if event.type() == QEvent.Type.Enter:
                self._snap_hover_timer.start()
                self._snap_overlay.cancel_hide()
                return False
            elif event.type() == QEvent.Type.Leave:
                self._snap_hover_timer.stop()
                if self._snap_overlay.isVisible():
                    self._snap_overlay.schedule_hide()
                return False
        return False
