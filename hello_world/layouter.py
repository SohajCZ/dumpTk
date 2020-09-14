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

    def __init__(self, kind=None):
        self.kind=None
        self.layout = None
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

        self.inited = False

        if kind is None: # TODO: I might need to not have it really inited?
            return

        self._manual_init(kind)
        
    def _manual_init(self, kind, other_args={}):
        self.kind = kind

        if kind == PACK:
            self._init_pack(other_args)
        elif kind == GRID:
            self._init_grid(other_args)
        # TODO Else? (place)

        self.inited = True

    def insert_child_layouter(self, layouter, other_args={}):
        if self.kind == 'pack':
            self._get_layout_for_side(other_args.get('-side', TOP)).addLayout(layouter.layout)
        elif self.kind == 'grid':
            self.layout.addLayout(layouter.layout,
                                  other_args.get('-row'), other_args.get('-column'))
        # TODO Else? (place)

    def _init_pack(self, other_args={}):
        side = other_args.get('-side', TOP)
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
            self.column_layout.addLayout(self.top)
            self.column_layout.addLayout(self.bottom)

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

    def _init_grid(self, other_args={}):
        row = other_args.get('-row', 0)
        column = other_args.get('-column', 0)

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

    def pack_widget(self, widget, other_args={}):
        side = other_args.get('-side', "top")
        # TODO: Other args

        self._get_layout_for_side(side).addWidget(widget)

    def grid_widget(self, widget, other_args):
        row = other_args.get('-row', 0)
        column = other_args.get('-column', 0)
        # TODO: Other args

        self.layout.addWidget(widget, row, column)

    def add_widget(self, widget, kind="pack", other_args={}):
        # TODO: Docs.
        # Args could be dict with side for pack (-side),
        # row (-row)/column (-column) for grid, sticky and so on.

        if not self.inited:
            self._manual_init(kind, other_args)

        if kind != self.kind:
            raise MixedLayouts

        if kind == PACK:
            self.pack_widget(widget, other_args)
        elif kind == GRID:
            self.grid_widget(widget, other_args)
        # TODO Else? (place)
        

        
            

