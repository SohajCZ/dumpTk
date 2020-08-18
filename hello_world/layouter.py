from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout

# TODO: Enums?
PACK = "pack"
GRID = "grid"

TOP="top"
RIGHT="right"
BOTTOM="bottom"
LEFT="left"


class MixedLayouts(Exception):
    pass


class Layouter: # TODO Pack / Grid polymorfism.

    def __init__(self, kind=None, side=None, *args): # TODO: Args
        self.kind=None
        self.layout = None
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.master = None

        self.inited = False

        if kind is None: # TODO: I might need to not have it really inited?
            return

        self._manual_init(kind)
        
    def _manual_init(self, kind, side=None):
        self.kind = kind

        if kind == PACK:
            self._init_pack(side)
        elif kind == GRID:
            self._init_grid()
        # TODO Else? (place)

        self.master.setLayout(self.layout) # TODO This might solve it

        self.inited = True

    def _init_pack(self, side=None):
        # TODO: Docs

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
            self.row_layout.addLayout(self.top)
            self.row_layout.addLayout(self.bottom)

            # Compose layout
            self.layout.addLayout(self.left)
            self.layout.addLayout(self.column_layout)
            self.layout.addLayout(self.right)
        else: # TODO: Support only left and top? Gonna say this means top.
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

    def _init_grid(self):
        self.layout = QGridLayout()

    def _get_layout_for_side(self, side=TOP):
        # TODO : "Switch"

        if side == TOP:
            return self.top
        elif side == LEFT:
            return self.left
        elif side == RIGHT:
            return self.right
        else:
            return self.bottom

    def pack_widget(self, widget, side, *args): # TODO args?
        self._get_layout_for_side(side).addWidget(widget)

    def grid_widget(self, widget, row, column, *args): # TODO args? sticky ...
        self.layout.addWidget(widget, row, column)

    def add_widget(self, widget, kind, side=None, *args):
        # TODO: Docs. Args could be side for pack, row/column for grid, sticky and so on.

        if not self.inited:
            self._manual_init(kind, side)

        if kind != self.kind:
            raise MixedLayouts

        if kind == PACK:
            self.pack_widget(widget, side, *args) # TODO other args?
        elif kind == GRID:
            self.grid_widget(widget, *args) # TODO other args? (also row and column now).
        # TODO Else? (place)
        

        
            

