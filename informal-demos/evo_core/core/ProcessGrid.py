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

    def __init__(self):
        pass

    def getCellAt(self, i, j):
        if i not in self.data:
            self.data[i] = {}
            return None
        elif j not in self.data[i]:
            return None

        return self.data[i][j]

    def setCellAt(self, i, j, value):
        if i not in self.data:
            self.data[i] = {}
            self.data[i][j] = GridCell(value, self, i, j)
        elif j not in self.data[i]:
            self.data[i][j] = GridCell(value, self, i, j)
        else:
            self.data[i][j].value = value

        if self.minI is None or (self.minI > i):
            self.minI = i
        if self.maxI is None or (self.maxI < i):
            self.maxI = i
        if self.minJ is None or (self.minJ > j):
            self.minJ = j
        if self.maxJ is None or (self.maxJ < j):
            self.maxJ = j

        return self.data[i][j]

    def traversal(self, onCell, onComplete):
        data = {}
        for i in self.data:
            data[i] = dict(self.data[i])

        for i in data:
            row = data[i]
            for j in row:
                onCell(row[j])

        onComplete()

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

    def __init__(self, value, grid, i, j):
        self.value = value
        self.grid = grid
        self.i = i
        self.j = j

    def getCellAwayFrom(self, offsetI, offsetJ):
        cell = self.grid.getCellAt(self.i + offsetI, self.j + offsetJ)
        if cell is None:
            cell = self.grid.setCellAt(self.i + offsetI, self.j + offsetJ, None)

        return cell

    def seeCellAwayFrom(self, offsetI, offsetJ):
        return self.grid.getCellAt(self.i + offsetI, self.j + offsetJ)

import time


class IntCell:
    value = 0
    nextValue = 0

    def __init__(self, value, next):
        self.value = value
        self.nextValue = next

    def update(self):
        self.value = self.nextValue

grid = ProcessGrid()
grid.setCellAt(0, 0, IntCell(1, 1))

loopTimes = 200


def onCell(cell):
    value = cell.value
    if value is None or value.value is None:
        return

    if value.value == 0:
        cell.value = IntCell(None, None)
    elif value.value == 1:
        cell.getCellAwayFrom(-1, 0).value = IntCell(None, 2)
        cell.value.nextValue = 2
    elif value.value == 2:
        cell.getCellAwayFrom(0, 1).value = IntCell(None, 3)
        cell.value.nextValue = 3
    elif value.value == 3:
        cell.getCellAwayFrom(-1, 1).value = IntCell(None, 4)
        cell.value.nextValue = 4
    elif value.value == 4:
        cell.getCellAwayFrom(1, 1).value = IntCell(None, 5)
        cell.value.nextValue = 5
    elif value.value == 5:
        cell.value = IntCell(None, None)

        c = cell.getCellAwayFrom(-1, -1)
        if c.value is not None and c.value.value is not None:
            v = c.value.value - 1
            if v <= 0:
                c.value.nextValue = None
            else:
                c.value.nextValue = v

        c = cell.getCellAwayFrom(1, 0)
        if c.value is None:
            c.value = IntCell(None, 1)
        elif c.value.value is None:
            c.value.nextValue = 1
        else:
            v = c.value.value + 1
            if v > 5:
                v = 5

            c.value.nextValue = v


def updateCell(cell):
    if cell.value is not None:
        cell.value.update()

def onComplete():
    grid.traversal(updateCell, lambda : 1)

    print("=" * (grid.width() + 2))
    for i in range(grid.minI, grid.maxJ + 1):
        line = "="
        for j in range(grid.minJ, grid.maxJ + 1):
            cell = grid.getCellAt(i, j)
            if cell is None or cell.value is None or cell.value.value is None:
                line += " "
            else:
                line += str(cell.value.value)

        line += "="

        print line

startTime = time.time()
for i in range(0, loopTimes):
    grid.traversal(onCell, onComplete)

print("Time used :", time.time() - startTime)