from __future__ import annotations

import dataclasses
from typing import NamedTuple, Union

from qtpy import QtCore


class TabState(NamedTuple):
    title: str
    cls_name: str


@dataclasses.dataclass
class BaseWidgetState:
    geometry: QtCore.QRect = dataclasses.field(default_factory=QtCore.QRect)
    flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.Widget


@dataclasses.dataclass
class SplitterState(BaseWidgetState):
    kind: str = 'splitter'
    sizes: tuple[int, ...] = ()
    orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
    states: tuple[WidgetState, ...] = ()


@dataclasses.dataclass
class DockWidgetState(BaseWidgetState):
    kind: str = 'dock'
    current_index: int = 0
    widgets: tuple[TabState, ...] = ()
    detachable: bool = True
    auto_delete: bool = True
    is_center_widget: bool = False


WidgetState = Union[SplitterState, DockWidgetState]


@dataclasses.dataclass
class WindowState:
    geometry: QtCore.QRect = dataclasses.field(default_factory=QtCore.QRect)
    states: tuple[WidgetState, ...] = ()
