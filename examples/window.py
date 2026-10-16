from __future__ import annotations

import logging
import random

from qtpy import QtCore, QtWidgets

from examples import application, save_screenshot
from qt_dock_window import (
    DockWidgetState,
    SplitterState,
    StateDockWindow,
    TabState,
    WindowState,
)

_ROWS = ['Sun', 'Earth', 'Moon', 'Mars', 'Jupiter']


class WidgetTree(QtWidgets.QTreeWidget):
    """A tree widget with two levels of random data."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setHeaderLabels(['Name', 'Value'])

        rng = random.Random(0)
        for group in ('Alpha', 'Beta', 'Gamma'):
            item = QtWidgets.QTreeWidgetItem([group, ''])
            self.addTopLevelItem(item)
            for index in range(rng.randint(2, 5)):
                child = QtWidgets.QTreeWidgetItem(
                    [f'{group}-{index}', str(rng.randint(0, 1000))]
                )
                item.addChild(child)

        self.expandAll()
        self.resizeColumnToContents(0)


class WidgetTable(QtWidgets.QTableWidget):
    """A table widget with random data."""

    _count = 0

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        WidgetTable._count += 1
        rng = random.Random(WidgetTable._count)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Name', 'Radius', 'Weight'])
        self.setRowCount(len(_ROWS))
        self.setAlternatingRowColors(True)

        for row, name in enumerate(_ROWS):
            values = [
                name,
                str(rng.randint(1000, 700000)),
                f'{rng.uniform(1, 10000):.2f}',
            ]
            for column, value in enumerate(values):
                self.setItem(row, column, QtWidgets.QTableWidgetItem(value))

        self.horizontalHeader().setStretchLastSection(True)


class WidgetLog(QtWidgets.QPlainTextEdit):
    """A read-only log widget."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setReadOnly(True)
        for index in range(20):
            self.appendPlainText(f'log message {index:02d}')


def build_window() -> StateDockWindow:
    """Create a window with a docked layout and return it."""

    window = StateDockWindow()
    window.setWindowTitle('qt-dock-window')
    window.resize(960, 480)

    window.register_widget(WidgetTree, 'Tree')
    window.register_widget(WidgetTable, 'Table')
    window.register_widget(WidgetLog, 'Log')

    window.set_window_state(
        WindowState(
            states=(
                SplitterState(
                    orientation=QtCore.Qt.Orientation.Horizontal,
                    sizes=(300, 660),
                    states=(
                        DockWidgetState(
                            current_index=0,
                            widgets=(
                                TabState('Tree', 'Tree'),
                                TabState('Log', 'Log'),
                            ),
                        ),
                        DockWidgetState(
                            current_index=0,
                            widgets=(
                                TabState('Table 1', 'Table'),
                                TabState('Table 2', 'Table'),
                                TabState('Table 3', 'Table'),
                                TabState('Table 4', 'Table'),
                            ),
                            is_center_widget=True,
                        ),
                    ),
                ),
            ),
        )
    )
    return window


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, force=True)

    with application() as app:
        window = build_window()
        window.show()

        # Let the layout settle, then save the screenshot.
        app.processEvents()
        save_screenshot(window, 'window')


if __name__ == '__main__':
    main()
