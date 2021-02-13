"""
This file contains class Layouter.
This class solves layout management with QGridLayout of QBoxLayout from Qt
as much similar as possible to geometry manager of Tkinter. Layouter
does not support place geometry method from Tkinter since

Layouter is instantiated as not initiated. This is because Layouter
if created immediately when widget is created, where child
layouts might not be needed. Child layouts are instantiated only when
another widget is created with original widget as master.

Child widget could be added with add_widget method. When not initiated,
as mentioned above, method _manual_init is called. Added child widget
decides if Layouter is initiated with grid of pack strategy.

If grid strategy is used, QGridLayout is initiated. Layouter currently
supports assignment of row/column, row/column-span and sticky, which decides
how free space in grid is used. More could be implemented - TODO.

If pack strategy is used, initiation differs according to child widgets
packed side. If child is packed on left side, QHBoxLayout (horizontal) is
initiated and gradually filled with:
1) QHBoxLayout (for left packed child),
2) QHBoxLayout with QVBoxLayout (for top packed child) and QVBoxLayout with
reverse order (for bottom packed child)
3) QHBoxLayout with reverse order (for right packed child)
as for three columns with middle column having top and bottom part.

If child is packed on any other side then left, QVBoxLayout (vertical) is
initiated and gradually filled with:
1) QVBoxLayout (for top packed child),
2) QVBoxLayout with QHBoxLayout (for left packed child) and QHBoxLayout with
reverse order (for right packed child),
3) QVBoxLayout with reverse order (for bottom packed child),
as for three rows with middle row having left and right part.

These two strategies for packing proved as most similar solution
to the Packer from Tkinter and also the best looking one since
packing first widget as bottom or right did not really made sense.

Packing does not support any more additional options at the moment - TODO.

After initial, pack_widget or grid_widget methods are used by Layouter
independently. In case of pack, Layouter has references on every layout
(left, right, bottom, top), all of them are created everytime.

Layouter does not support mixing layouts, when Layouter is initiated,
kind of layout (pack, grid) cannot change. If widget with different
kind is being packed, exception is thrown.

Layouter is recursive structure by its definition. Kind of layout
cannot be mixed in one master widget, but master widget could be
placed in different kind of layout then its own layout kind is and
so on.

Note that it would be better to have Layouter class as ancestor
of GridLayouter and PackLayouter to implement polymorphism - TODO.
"""

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout

from .translate_qt_core import translate_align


PACK = "pack"
GRID = "grid"

TOP = "top"
RIGHT = "right"
BOTTOM = "bottom"
LEFT = "left"


class MixedLayouts(Exception):
    pass


class Layouter:
    """This class solves itself placing widget
    similarly as tkinter geometry manager does."""

    def __init__(self, kind=None):
        self.kind = None
        self.layout = None
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.widget_found = False  # Ending recursion faster...

        self.inited = False

        if kind is None:
            return

        self._manual_init(kind)

    def _manual_init(self, kind, other_args={}):
        self.kind = kind

        if kind == PACK:
            self._init_pack(other_args)
        elif kind == GRID:
            self._init_grid(other_args)
        # Place omited.

        self.inited = True

    def _init_pack(self, other_args={}):
        """
        If pack strategy is used, initiation differs according to child widgets
        packed side. If child is packed on left side, QHBoxLayout (horizontal)
        is initiated and gradually filled with:
        1) QHBoxLayout (for left packed child),
        2) QHBoxLayout with QVBoxLayout (for top packed child) and QVBoxLayout
        with reverse order (for bottom packed child)
        3) QHBoxLayout with reverse order (for right packed child)
        as for three columns with middle column having top and bottom part.

        If child is packed on any other side then left, QVBoxLayout (vertical)
        is initiated and gradually filled with:
        1) QVBoxLayout (for top packed child),
        2) QVBoxLayout with QHBoxLayout (for left packed child) and QHBoxLayout
        with reverse order (for right packed child),
        3) QVBoxLayout with reverse order (for bottom packed child),
        as for three rows with middle row having left and right part.

        These two strategies for packing proved as most similar solution
        to the Packer from Tkinter and also the best looking one since
        packing first widget as bottom or right did not really made sense.
        """

        side = other_args.get('-side', TOP)

        # Init vertical layouts
        self.top = QVBoxLayout()
        self.bottom = QVBoxLayout()
        self.bottom.setDirection(QBoxLayout.BottomToTop)

        # Init horizontal layouts
        self.left = QHBoxLayout()
        self.right = QHBoxLayout()
        self.right.setDirection(QBoxLayout.RightToLeft)

        if side == LEFT:
            # Init top level layout
            self.layout = QHBoxLayout()

            # Init middle column layout and add vertical layouts
            self.column_layout = QHBoxLayout()
            self.column_layout.addLayout(self.top)
            self.column_layout.addLayout(self.bottom)

            # Compose layout
            self.layout.addLayout(self.left)
            self.layout.addLayout(self.column_layout)
            self.layout.addLayout(self.right)
        else:  # Supports only left and top - Gonna say this means top.
            # Init top level layout
            self.layout = QVBoxLayout()

            # Init middle row layout and add horizontal layouts
            self.row_layout = QHBoxLayout()
            self.row_layout.addLayout(self.left)
            self.row_layout.addLayout(self.right)

            # Compose layout
            self.layout.addLayout(self.top)
            self.layout.addLayout(self.row_layout)
            self.layout.addLayout(self.bottom)

    def _init_grid(self, other_args={}):
        """Initiates QGridLayout."""
        self.layout = QGridLayout()

    def _get_layout_for_side(self, side=TOP):
        side_switch = {
            TOP: self.top,
            LEFT: self.left,
            RIGHT: self.right,
        }

        return side_switch.get(side, self.bottom)

    def pack_widget(self, widget, other_args={}):
        side = other_args.get('-side', "top")
        # TODO: Other args

        self._get_layout_for_side(side).addWidget(widget)

    def grid_find_widget(self, layout, widget):
        if self.widget_found:
            return None, -1

        # There is no better way then recursion?!
        idx = layout.indexOf(widget)
        if idx == -1:
            for children in layout.children():
                self.grid_find_widget(self, widget, children)

            return None, -1

        return layout, idx

    def grid_widget(self, widget, other_args):
        row, column = 0, 0
        rows, cols = 1, 1

        layout, found_index = self.grid_find_widget(self.layout, widget)
        if found_index != -1:
            row, column, rows, cols = layout.getItemPosition(found_index)

        row_new = other_args.get('-row', row)
        column_new = other_args.get('-column', column)
        rows_new = other_args.get('-rowspan', rows)
        columns_new = other_args.get('-columnspan', cols)

        if '-sticky' not in other_args and found_index != -1:
            self.layout.addWidget(widget, row_new, column_new,
                                  rows_new, columns_new)
        else:
            sticky = translate_align(other_args.get('-sticky', ''))
            self.layout.addWidget(widget, row_new, column_new,
                                  rows_new, columns_new, alignment=sticky)

        return

    def add_widget(self, widget, kind="pack", other_args={}):
        """Adds widget to the layout, checks layout kind
        and accepts other arguments as "-side" for pack
        or "-columnspan" for grid."""

        if not self.inited:
            self._manual_init(kind, other_args)

        if kind != self.kind:
            raise MixedLayouts

        if kind == PACK:
            self.pack_widget(widget, other_args)
        elif kind == GRID:
            self.grid_widget(widget, other_args)
        # Place omitted.
