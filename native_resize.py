# -*- coding: utf-8 -*-
"""
native_resize.py — Native 8-Direction Window Resize Mixin
==========================================================
Provides smooth, OS-level frameless window resizing on Windows via
WM_NCHITTEST (nativeEvent). Falls back silently on non-Windows platforms.

Also provides maximize/restore handling that is aware of Windows taskbar
auto-hide (pseudo-maximize), plus double-click-on-titlebar to toggle
maximize/restore.

Originally developed for Macan Quick View, then refined and extracted
into this reusable mixin for the Macan app family.

USAGE
-----
1. Import the mixin:

       from native_resize import NativeResizeMixin

2. Add it to your QMainWindow subclass (before QMainWindow in MRO):

       class MyWindow(NativeResizeMixin, QMainWindow):
           def __init__(self):
               super().__init__()
               self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

               # Optional: set the drag widget (title bar).
               # Any QWidget whose empty area should allow window dragging,
               # AND will respond to double-click for maximize/restore.
               # If not set, only resize edges will be handled.
               self.set_drag_widget(self.title_bar)

               # Optional: set interactive child types that should NOT
               # trigger window drag / double-click maximize inside the
               # drag widget. Defaults to (QPushButton,) if not called.
               self.set_drag_interactive_types((QPushButton, QToolButton, QSlider))

               # Optional: change resize border width in pixels (default: 8).
               self.resize_margin = 6

               # Optional: register icons so your maximize/restore button
               # auto-swaps its icon when the window state changes.
               self.set_maximize_icons(self.maximize_icon, self.restore_icon,
                                        target=self.maximize_action)

       # Call this from your maximize/restore button or menu action:
       self.toggle_maximize_restore()

REQUIREMENTS
------------
- PySide6
- Windows OS for native resize / taskbar auto-hide detection
  (graceful no-op / fallback on Linux/macOS)

NOTES
-----
- The mixin overrides nativeEvent() and mouseDoubleClickEvent(). If your
  class also overrides either, call the super() version at the end of yours.
- Double-click-to-maximize/restore works in both directions: the
  maximize -> restore direction is handled by mouseDoubleClickEvent()
  (normal Qt client-area event), while the normal -> maximize direction is
  handled inside nativeEvent() via WM_NCLBUTTONDBLCLK, since clicks on the
  HTCAPTION-classified drag zone arrive as non-client messages while the
  window is not maximized.
- toggle_maximize_restore() automatically detects Windows taskbar
  auto-hide and uses a 1px "pseudo-maximize" geometry instead of native
  showMaximized() so hovering the screen edge still reveals the taskbar.
"""

import platform
import ctypes
import ctypes.wintypes

from PySide6.QtWidgets import QPushButton, QApplication
from PySide6.QtCore import QPoint, Qt, QTimer

# ── WM_NCHITTEST constants ────────────────────────────────────────────────────
_WM_NCHITTEST  = 0x0084
_WM_NCLBUTTONDBLCLK = 0x00A3  # Double-click on a non-client (e.g. HTCAPTION) area
_HTCLIENT      = 1
_HTCAPTION     = 2
_HTLEFT        = 10
_HTRIGHT       = 11
_HTTOP         = 12
_HTTOPLEFT     = 13
_HTTOPRIGHT    = 14
_HTBOTTOM      = 15
_HTBOTTOMLEFT  = 16
_HTBOTTOMRIGHT = 17

_IS_WINDOWS = platform.system() == "Windows"


class NativeResizeMixin:
    """
    Mixin that adds native 8-direction resize, optional title-bar drag,
    and taskbar-aware maximize/restore (with double-click toggle) to any
    FramelessWindowHint QMainWindow on Windows.

    Attributes set on the host class (all optional):
        resize_margin (int)          : Pixel width of the resize hit zone. Default 8.
        _drag_widget  (QWidget|None) : Widget whose empty area acts as a drag handle
                                       AND a double-click maximize/restore zone.
        _drag_iactive (tuple)        : Widget types inside _drag_widget that should NOT
                                       trigger drag / double-click maximize (e.g. buttons).
        _pseudo_maximized (bool)             : True when window is in pseudo-maximize state.
        _normal_geometry_before_pseudo (QRect): Geometry saved before pseudo-maximize,
                                       used to restore exact position/size.
    """

    # ── Public configuration API ──────────────────────────────────────────────

    def set_drag_widget(self, widget):
        """
        Register a widget (typically your custom title bar) as the drag handle.
        Clicking on empty space inside this widget will move the window.

        Parameters
        ----------
        widget : QWidget
            The widget to use as the drag zone.
        """
        self._drag_widget = widget

    def set_drag_interactive_types(self, types: tuple):
        """
        Specify which child widget types inside the drag widget should NOT
        trigger a window drag (because they have their own click behaviour).

        Parameters
        ----------
        types : tuple of type
            E.g. (QPushButton, QToolButton, QSlider)
        """
        self._drag_iactive = types

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _nrm_resize_margin(self) -> int:
        return getattr(self, "resize_margin", 8)

    def _nrm_drag_widget(self):
        return getattr(self, "_drag_widget", None)

    def _nrm_drag_iactive(self) -> tuple:
        return getattr(self, "_drag_iactive", (QPushButton,))

    # ── nativeEvent override ──────────────────────────────────────────────────

    def nativeEvent(self, eventType, message):
        """
        Intercept Windows messages to provide native hit-testing for:
          - 8-direction resize from window edges and corners
          - Window drag from the registered drag widget's empty area
        """
        if not _IS_WINDOWS:
            return super().nativeEvent(eventType, message)

        try:
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
        except Exception:
            return super().nativeEvent(eventType, message)

        # ── Double-click on the non-client (HTCAPTION) drag zone ─────────────
        # While the window is NOT maximized, the empty area of the registered
        # drag widget is classified as HTCAPTION below, which makes Windows
        # treat clicks there as non-client messages. A double-click in that
        # state arrives as WM_NCLBUTTONDBLCLK, not the regular client-area
        # WM_LBUTTONDBLCLK that mouseDoubleClickEvent() listens for — so
        # without this, double-click-to-maximize would only ever work in the
        # maximize -> restore direction (where hit-testing is bypassed below).
        if msg.message == _WM_NCLBUTTONDBLCLK:
            if msg.wParam == _HTCAPTION:
                self.toggle_maximize_restore()
                return True, 0
            return super().nativeEvent(eventType, message)

        if msg.message != _WM_NCHITTEST:
            return super().nativeEvent(eventType, message)

        # ── Skip border hit-testing saat window maximized / pseudo-maximized ──
        if self._is_pseudo_or_maximized():
            return super().nativeEvent(eventType, message)

        # ── Convert screen coords to window-local coords ──────────────────────
        # msg.pt is in PHYSICAL pixels; Qt geometry is in LOGICAL pixels.
        # On HiDPI (125 %, 150 %, …) we must divide by devicePixelRatioF().
        # frameGeometry() is used so the result is correct regardless of
        # WA_TranslucentBackground (where self.x() == frameGeometry.x()).
        dpr = self.devicePixelRatioF()
        fg  = self.frameGeometry()
        x   = msg.pt.x / dpr - fg.x()
        y   = msg.pt.y / dpr - fg.y()
        w   = fg.width()
        h   = fg.height()
        bw  = self._nrm_resize_margin()

        # ── 8-direction edge & corner detection ───────────────────────────────
        is_top    = y < bw
        is_bottom = y > h - bw
        is_left   = x < bw
        is_right  = x > w - bw

        # Corners take priority over edges (checked first)
        if is_top    and is_left:  return True, _HTTOPLEFT
        if is_top    and is_right: return True, _HTTOPRIGHT
        if is_bottom and is_left:  return True, _HTBOTTOMLEFT
        if is_bottom and is_right: return True, _HTBOTTOMRIGHT
        if is_top:                 return True, _HTTOP
        if is_bottom:              return True, _HTBOTTOM
        if is_left:                return True, _HTLEFT
        if is_right:               return True, _HTRIGHT

        # ── Drag zone: empty area inside the drag widget → HTCAPTION ─────────
        drag_widget = self._nrm_drag_widget()
        if drag_widget is not None:
            global_pos = QPoint(msg.pt.x, msg.pt.y)
            local_pos  = drag_widget.mapFromGlobal(global_pos)
            if drag_widget.rect().contains(local_pos):
                child = drag_widget.childAt(local_pos)
                iactive = self._nrm_drag_iactive()
                if child is None or not isinstance(child, iactive):
                    return True, _HTCAPTION

        return True, _HTCLIENT

    # ── Maximize / Restore configuration API ────────────────────────────────

    def set_maximize_icons(self, maximize_icon, restore_icon, target=None):
        """
        Register icons so a maximize/restore button or action automatically
        swaps its icon whenever the window's maximize state changes.
        Calling this is optional — if skipped, icon sync is simply a no-op.

        Parameters
        ----------
        maximize_icon : QIcon
            Icon to show when the window is in its normal (non-maximized) state.
        restore_icon : QIcon
            Icon to show when the window is maximized / pseudo-maximized.
        target : QAction | QAbstractButton | None
            Object exposing setIcon(). If None, falls back to
            self.maximize_action on the host class (if present).
        """
        self._nrm_max_icon = maximize_icon
        self._nrm_restore_icon = restore_icon
        self._nrm_max_icon_target = target

    # ── Taskbar Auto-Hide Detection ─────────────────────────────────────────

    def _nrm_is_taskbar_autohide(self) -> bool:
        """
        Detect whether the Windows taskbar is currently in Auto-Hide mode,
        using the SHAppBarMessage Windows API via ctypes.
        Returns False on non-Windows platforms or on any failure.
        """
        if not _IS_WINDOWS:
            return False
        try:
            ABM_GETSTATE = 0x00000004
            ABS_AUTOHIDE = 0x00000001

            class APPBARDATA(ctypes.Structure):
                _fields_ = [
                    ("cbSize",           ctypes.wintypes.DWORD),
                    ("hWnd",             ctypes.wintypes.HWND),
                    ("uCallbackMessage", ctypes.wintypes.UINT),
                    ("uEdge",            ctypes.wintypes.UINT),
                    ("rc",               ctypes.wintypes.RECT),
                    ("lParam",           ctypes.c_long),
                ]

            abd = APPBARDATA()
            abd.cbSize = ctypes.sizeof(APPBARDATA)
            result = ctypes.windll.shell32.SHAppBarMessage(ABM_GETSTATE, ctypes.byref(abd))
            return bool(result & ABS_AUTOHIDE)
        except Exception:
            return False

    def _nrm_taskbar_edge(self) -> str:
        """
        Detect which screen edge the Windows taskbar is docked to.
        Returns one of 'left' / 'top' / 'right' / 'bottom'.
        Defaults to 'bottom' on non-Windows platforms or on any failure.
        """
        if not _IS_WINDOWS:
            return "bottom"
        try:
            ABM_GETTASKBARPOS = 0x00000005
            ABE_LEFT, ABE_TOP, ABE_RIGHT, ABE_BOTTOM = 0, 1, 2, 3

            class APPBARDATA(ctypes.Structure):
                _fields_ = [
                    ("cbSize",           ctypes.wintypes.DWORD),
                    ("hWnd",             ctypes.wintypes.HWND),
                    ("uCallbackMessage", ctypes.wintypes.UINT),
                    ("uEdge",            ctypes.wintypes.UINT),
                    ("rc",               ctypes.wintypes.RECT),
                    ("lParam",           ctypes.c_long),
                ]

            abd = APPBARDATA()
            abd.cbSize = ctypes.sizeof(APPBARDATA)
            abd.hWnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            ctypes.windll.shell32.SHAppBarMessage(ABM_GETTASKBARPOS, ctypes.byref(abd))
            edge_map = {ABE_LEFT: "left", ABE_TOP: "top", ABE_RIGHT: "right", ABE_BOTTOM: "bottom"}
            return edge_map.get(abd.uEdge, "bottom")
        except Exception:
            return "bottom"

    # ── Maximize / Restore (taskbar auto-hide aware) ────────────────────────

    def _apply_maximize_with_taskbar(self):
        """
        Maximize the window, taking Windows taskbar auto-hide into account.
        - Taskbar auto-hide ON  → pseudo-maximize (shrink 1px on the taskbar's
          edge) so hovering the screen edge still reveals the taskbar.
        - Taskbar auto-hide OFF → plain showMaximized().
        """
        screen = QApplication.screenAt(self.geometry().center()) or QApplication.primaryScreen()
        screen_geom = screen.availableGeometry()

        if self._nrm_is_taskbar_autohide():
            # Save normal geometry first so it can be restored exactly later.
            self._normal_geometry_before_pseudo = self.geometry()

            edge = self._nrm_taskbar_edge()
            x, y, w, h = screen_geom.x(), screen_geom.y(), screen_geom.width(), screen_geom.height()

            if edge == "bottom":
                h -= 1
            elif edge == "top":
                y += 1
                h -= 1
            elif edge == "left":
                x += 1
                w -= 1
            elif edge == "right":
                w -= 1

            self.showNormal()
            self.setGeometry(x, y, w, h)
            self._pseudo_maximized = True
            QTimer.singleShot(0, self._sync_maximize_icon)
        else:
            self._pseudo_maximized = False
            self._normal_geometry_before_pseudo = None
            self.showMaximized()

    def _is_pseudo_or_maximized(self) -> bool:
        """Return True if the window is maximized, fullscreen, or pseudo-maximized."""
        return self.isMaximized() or self.isFullScreen() or getattr(self, "_pseudo_maximized", False)

    def _sync_maximize_icon(self):
        """Update the maximize/restore button icon to match the current window state."""
        target = getattr(self, "_nrm_max_icon_target", None) or getattr(self, "maximize_action", None)
        if target is None:
            return
        if self._is_pseudo_or_maximized():
            icon = getattr(self, "_nrm_restore_icon", None)
        else:
            icon = getattr(self, "_nrm_max_icon", None)
        if icon is not None:
            target.setIcon(icon)

    def toggle_maximize_restore(self):
        """
        Toggle between maximized (or pseudo-maximized) and the normal window size.
        Wire this to your maximize/restore button or menu action.
        """
        if self._is_pseudo_or_maximized():
            was_pseudo = getattr(self, "_pseudo_maximized", False)
            self._pseudo_maximized = False
            if was_pseudo and getattr(self, "_normal_geometry_before_pseudo", None) is not None:
                self.showNormal()
                self.setGeometry(self._normal_geometry_before_pseudo)
                self._normal_geometry_before_pseudo = None
            else:
                self.showNormal()
            QTimer.singleShot(0, self._sync_maximize_icon)
        else:
            self._apply_maximize_with_taskbar()

    # ── Double-click on title bar → maximize / restore ──────────────────────

    def mouseDoubleClickEvent(self, event):
        """
        Double-clicking empty space inside the registered drag widget
        (set via set_drag_widget) toggles maximize/restore, mirroring
        native OS title-bar behaviour.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            drag_widget = self._nrm_drag_widget()
            if drag_widget is not None:
                global_pos = event.globalPosition().toPoint()
                local_pos  = drag_widget.mapFromGlobal(global_pos)
                if drag_widget.rect().contains(local_pos):
                    child = drag_widget.childAt(local_pos)
                    iactive = self._nrm_drag_iactive()
                    if child is None or not isinstance(child, iactive):
                        self.toggle_maximize_restore()
                        event.accept()
                        return
        super().mouseDoubleClickEvent(event)
