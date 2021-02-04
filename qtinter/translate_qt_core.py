from PyQt5.QtCore import Qt


def translate_align(sticky_string):
    # TODO Doc (for real)
    """
    https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/grid.html

    ---------------
    | NW   N   NE |
    | W CENTER E  |
    | SW   S   SE |
    ---------------

    If you do not provide a sticky attribute, the default behavior
    is to center the widget in the cell.

    You can position the widget in a corner of the cell by using
    sticky=tk.NE (top right), tk.SE (bottom right), tk.SW (bottom left),
    or tk.NW (top left).

    You can position the widget centered against one side of the cell
    by using sticky=tk.N (top center), tk.E (right center),
    tk.S (bottom center), or tk.W (left center).

    Use sticky=tk.N+tk.S to stretch the widget vertically but leave
    it centered horizontally.

    Use sticky=tk.E+tk.W to stretch it horizontally but leave
    it centered vertically.

    Use sticky=tk.N+tk.E+tk.S+tk.W to stretch the widget
    both horizontally and vertically to fill the cell.

    The other combinations will also work. For example, sticky=tk.N+tk.S+tk.W
    will stretch the widget vertically and place it against the
    west (left) wall.

    Qt:
    https://doc.bccnsoft.com/docs/PyQt4/qt.html#AlignmentFlag-enum

    """

    # Int value of Qt.AlignCenter = 132
    alignment = 0

    align_switch = {
        'n': Qt.AlignTop,
        'w': Qt.AlignLeft,
        'e': Qt.AlignRight,
        's': Qt.AlignBottom,
    }

    # We could use bitwise operations ...
    # Such as QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom
    for align in sticky_string:
        alignment |= align_switch[align]

    if (('n' in sticky_string and 's' in sticky_string) or
        ('w' in sticky_string and 'e' in sticky_string)):
        alignment |= Qt.AlignJustify

    return Qt.Alignment(alignment)
