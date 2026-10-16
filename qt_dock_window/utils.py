from __future__ import annotations

import re
from collections.abc import Sequence

from qtpy import QtCore, QtWidgets


def activate_window(widget: QtWidgets.QWidget) -> None:
    """Show, raise and activate the window that contains a widget."""

    window = widget.window()
    window.show()
    if window.windowState() & QtCore.Qt.WindowState.WindowMinimized:
        window.setWindowState(QtCore.Qt.WindowState.WindowActive)
    window.raise_()  # bring to front (macOS)
    window.activateWindow()  # give focus (Windows)


def unique_name(name: str, existing_names: Sequence[str]) -> str:
    """Return a unique name."""

    for existing_name in existing_names:
        if name.casefold() == existing_name.casefold():
            match = re.search(r'(.*?)(\d+)$', name)
            if match:
                number = int(match.group(2))
                name = match.group(1)
            else:
                number = 0
            name = f'{name}{number + 1}'
            return unique_name(name, existing_names)
    return name
