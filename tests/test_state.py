from qtpy import QtCore, QtWidgets

from qt_dock_window import (
    DockWidgetState,
    SplitterState,
    StateDockWindow,
    TabState,
    WindowState,
)


class WidgetA(QtWidgets.QWidget):
    pass


class WidgetB(QtWidgets.QWidget):
    pass


def _dock(current_index: int, widgets: list[list[str]]) -> DockWidgetState:
    return DockWidgetState(
        current_index=current_index,
        widgets=tuple(TabState(title, cls_name) for title, cls_name in widgets),
    )


def _splitter(states: list, sizes: list[int]) -> SplitterState:
    return SplitterState(
        sizes=tuple(sizes),
        orientation=QtCore.Qt.Orientation.Horizontal,
        states=tuple(states),
    )


def _window() -> StateDockWindow:
    window = StateDockWindow()
    window.register_widget(WidgetA, name='A', unique=True)
    window.register_widget(WidgetB, name='B')
    return window


def _titles(state: WindowState) -> list[str]:
    titles = []
    for child in state.states:
        if not isinstance(child, SplitterState):
            continue
        for dock in child.states:
            if isinstance(dock, DockWidgetState):
                titles.extend(tab.title for tab in dock.widgets)
    return titles


def test_state_round_trip(app: QtWidgets.QApplication) -> None:
    window = _window()
    window.set_window_state(
        WindowState(
            states=(
                _splitter(
                    [_dock(0, [['A', 'WidgetA']]), _dock(0, [['B', 'WidgetB']])],
                    [200, 200],
                ),
            ),
        )
    )

    titles = _titles(window.window_state())
    assert 'A' in titles
    assert 'B' in titles


def test_unique_widget_not_duplicated(app: QtWidgets.QApplication) -> None:
    window = _window()
    window.set_window_state(
        WindowState(
            states=(
                _splitter(
                    [_dock(0, [['A', 'WidgetA']]), _dock(0, [['A', 'WidgetA']])],
                    [200, 200],
                ),
            ),
        )
    )

    count = sum(isinstance(widget, WidgetA) for widget in window._widgets.values())
    assert count == 1


def test_state_kinds() -> None:
    assert SplitterState().kind == 'splitter'
    assert DockWidgetState().kind == 'dock'


def test_close_does_not_delete_widgets(app: QtWidgets.QApplication) -> None:
    window = _window()
    window.show_widget('A')
    dock = window.dock_widgets()[0]
    dock.close()

    assert any(isinstance(w, WidgetA) for w in window._widgets.values())


def test_close_closes_floating_docks(app: QtWidgets.QApplication) -> None:
    window = _window()
    window.show()
    window.show_widget('A')
    dock = window.dock_widgets()[0]
    assert dock.isVisible()

    window.close()
    assert not dock.isVisible()


def _process_deletions() -> None:
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.Type.DeferredDelete)


def test_close_tab_deletes_widget(app: QtWidgets.QApplication) -> None:
    window = _window()
    window.show_widget('A')
    dock = window.dock_widgets()[0]
    widget = dock.widget(0)
    assert widget is not None

    dock.close_tab(0)
    _process_deletions()

    assert not any(w is widget for w in window._widgets.values())
