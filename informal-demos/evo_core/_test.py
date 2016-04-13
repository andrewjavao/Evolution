import time
from core import procgrid

grid = procgrid.ProcessGrid()
grid.setCellAt(0, 0, 1)

loopTimes = 100


def onCell(cell):
    value = cell.value
    if value is None:
        return

    if value == 0:
        cell.setValue(None, False)
    elif value == 1:
        cell.getCellAwayFrom(-1, 0).setValue(2, False)
        cell.setValue(2, False)
    elif value == 2:
        cell.getCellAwayFrom(0, 1).setValue(3, False)
        cell.setValue(3, False)
    elif value == 3:
        cell.getCellAwayFrom(-1, 1).setValue(4, False)
        cell.setValue(4, False)
    elif value == 4:
        cell.getCellAwayFrom(1, 1).setValue(5, False)
        cell.setValue(5, False)
    elif value == 5:
        cell.setValue(None, False)

        c = cell.getCellAwayFrom(-1, -1)
        if c.value is not None:
            v = c.value - 1
            if v <= 0:
                c.setValue(None, False)
            else:
                c.setValue(v, False)

        c = cell.getCellAwayFrom(1, 0)
        if c.value is None:
            c.setValue(1, False)
        else:
            v = c.value + 1
            if v > 5:
                v = 5

            c.setValue(v, False)


def updateCell(cell):
    if cell.value is not None:
        cell.value.update()

def onComplete():
    print("=" * (grid.width() + 2))
    for i in range(grid.minI, grid.maxI + 1):
        line = "="
        for j in range(grid.minJ, grid.maxJ + 1):
            cell = grid.getCellAt(i, j)
            if cell is None or cell.value is None:
                line += " "
            else:
                line += str(cell.value)

        line += "="

        print line

startTime = time.time()

for i in range(0, loopTimes):
    grid.traversalThenUpdate(onCell, onComplete)

print("Time used :", time.time() - startTime)