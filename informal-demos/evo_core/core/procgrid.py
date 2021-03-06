# Support non-edged 2-dim grid, access to proper cell and cells next to it.
# With ProcessGrid, You'll able to :
#   pg = ProcessGrid()
#   cell = pg.getCellAt(i, j);
#   cellBelow = cell.getCellAwayFrom(0, -1);
# etc.

# -*- coding:UTF-8 -*-


class ProcessGrid(object):
    data = {}
    minI = None
    minJ = None
    maxI = None
    maxJ = None
    bounded = False

    def __init__(self):
        pass

    def getCellAt(self, i, j):
        if i not in self.data:
            self.data[i] = {}
            return None
        elif j not in self.data[i]:
            return None

        return self.data[i][j]

    def setCellAt(self, i, j, value, imm=True):
        # type: (int, int, object) -> GridCell
        if self.bounded:
            if i < self.minI or i > self.maxI or j < self.minJ or j > self.maxJ:
                return None

        if i not in self.data:
            self.data[i] = {}
            self.data[i][j] = GridCell(None, self, i, j)
            self.data[i][j].setValue(value, imm)    #TODO performance
        elif j not in self.data[i]:
            self.data[i][j] = GridCell(None, self, i, j)
            self.data[i][j].setValue(value, imm)    #TODO performance
        else:
            self.data[i][j].setValue(value, imm)

        if self.minI is None or (self.minI > i):
            self.minI = i
        if self.maxI is None or (self.maxI < i):
            self.maxI = i
        if self.minJ is None or (self.minJ > j):
            self.minJ = j
        if self.maxJ is None or (self.maxJ < j):
            self.maxJ = j

        return self.data[i][j]    #TODO performance

    def traversal(self, on_cell, on_complete=None):
        if on_cell is not None:
            data = {}
            for i in self.data:
                data[i] = dict(self.data[i])

            for i in data:
                row = data[i]
                for j in row:
                    on_cell(row[j])

        if on_complete is not None:
            on_complete()

    def traversalThenUpdate(self, on_cell, on_complete=None):
        if on_cell is not None:
            data = {}
            dirtyCells = []

            for i in self.data:
                data[i] = dict(self.data[i])

            for i in data:
                row = data[i]
                for j in row:
                    c = row[j]
                    on_cell(c)
                    if c.isDirty():
                        dirtyCells.append(c)

        for cell in dirtyCells:
            cell.update()

        if on_complete is not None:
            on_complete()

    def traversalAreaThenUpdate(self, i, j, w, h, on_cell, on_complete=None):
        if on_cell is not None:
            for x in range(i, i+h):
                for y in range(j, j+w):
                    c = self.getCellAt(x, y)
                    if c is None:
                        on_cell(None, x, y)
                        c = self.getCellAt(x, y)
                    else:
                        on_cell(c)

        for x in self.data:
            for y in self.data[x]:
                self.data[x][y].update()

        if on_complete is not None:
            on_complete()

    def width(self):
        if self.maxJ is None:
            return 0

        return self.maxJ - self.minJ + 1

    def height(self):
        if self.maxI is None:
            return 0

        return self.maxI - self.minI + 1


class GridCell(object):
    value = None
    grid = None
    i = None
    j = None
    dirty = False
    nextValue = None

    def __init__(self, value, grid, i, j):
        self.value = value
        self.grid = grid
        self.i = i
        self.j = j

    def getCellAwayFrom(self, offsetI, offsetJ):
        # type (int, int) -> GridCell
        cell = self.grid.getCellAt(self.i + offsetI, self.j + offsetJ)
        if cell is None:
            cell = self.grid.setCellAt(self.i + offsetI, self.j + offsetJ, None)

        return cell

    def seeCellAwayFrom(self, offsetI, offsetJ):
        return self.grid.getCellAt(self.i + offsetI, self.j + offsetJ)

    def setValue(self, next_value, imm=True):
        if imm:
            self.dirty = False
            self.value = next_value
        else:
            self.dirty = True
            self.nextValue = next_value

    def update(self):
        if self.dirty:
            self.value = self.nextValue
            self.dirty = False

    def isDirty(self):
        return self.dirty
