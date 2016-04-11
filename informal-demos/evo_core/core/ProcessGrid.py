# Support non-edged 2-dim grid, access to proper cell and cells next to it.
# With ProcessGrid, You'll able to :
#   pg = ProcessGrid()
#   cell = pg.getCellAt(i, j);
#   cellBelow = cell.getCellAwayFrom(0, -1);
# etc.

# -*- coding:UTF-8 -*-


class ProcessGrid(object):
    def __init__(self):
        pass

    def getCellAt(self, i, j):
        pass


class GridCell(object):
    def __init__(self):
        pass

    def getCellAwayFrom(self, offsetI, offsetJ):
        pass