#command line argument:
# first : int, run so many steps then start to render
# second : time for every step

import time
import os
import sys
from core import procgrid

loopTimes = 0
pause_time = 0.16
clear_screen_cmd = "clear"
max_w = 40

if len(sys.argv) > 1:
    loopTimes = int(sys.argv[1])

if len(sys.argv) > 2:
    pause_time = float(sys.argv[2])

if len(sys.argv) > 2:
    max_w = int(sys.argv[3])

up = [-1, 0]
down = [1, 0]
left = [0, -1]
right = [0, 1]
up_right = [-1, 1]
up_left = [-1, -1]
down_right = [1, 1]
down_left = [1, -1]
all_around = [up, down, left, right, up_right, up_left, down_right, down_left]
all_pairs = [[up, down], [left, right], [up_right, down_left], [up_left, down_right]]
explosion = [up, down, left, right]
explosion_x = [up_right, up_left, down_right, down_left]
rot_left = {}

def setRotLeft(p, to_p):
    if p[0] not in rot_left:
        rot_left[p[0]] = {}

    rot_left[p[0]][p[1]] = to_p

setRotLeft(up, up_left)
setRotLeft(down, down_right)
setRotLeft(left, down_left)
setRotLeft(right, up_right)
setRotLeft(up_right, up)
setRotLeft(up_left, left)
setRotLeft(down_right, right)
setRotLeft(down_left, down)

grid = procgrid.ProcessGrid()

#for i in range(0, 10):
#    for j in range(0, 10):
#        grid.setCellAt(i, j, 0)

grid.setCellAt(0, 0, 1)
grid.setCellAt(1, 1, 1)
grid.setCellAt(0, 2, 1)
grid.setCellAt(0, 4, 1)
grid.setCellAt(2, 1, 1)
grid.setCellAt(2, 2, 1)
grid.setCellAt(2, 4, 1)

#grid.setCellAt(5, 2, 1)
#grid.setCellAt(6, 6, 1)
#grid.setCellAt(7, 3, 1)

def seeCellsAround(cell, positions, value):
    if cell is None:
        return False

    for p in positions:
        c = cell.seeCellAwayFrom(p[0], p[1])
        if c is None or not c.value == value:
            return False

    return True

def seeFitPositions(cell, positions, value):
    if cell is None:
        return 0

    fit_position = []
    for p in positions:
        c = cell.seeCellAwayFrom(p[0], p[1])
        if (c is None and value == 0) or (c is not None and c.value == value):
            fit_position.append(list(p))

    return fit_position

# cannot be alone, arise/shut by odd/even 2-pair,
# 1:00000000 -> 0:11110000
def onCell(cell, i=0, j=0):
    # type: (GridCell) -> None
    if cell is None:
        myself = procgrid.GridCell(0, grid, i, j)
    else:
        myself = cell

    pair_num = 0
    for pair in all_pairs:
        if seeCellsAround(myself, pair, 1):
            pair_num += 1

    black_positions = seeFitPositions(myself, all_around, 1)

    if myself.value == 1 and len(black_positions) == 1:
        p = black_positions[0]
        rotter_position = [myself.i + p[0], myself.j + p[1]]
        p[0], p[1] = -p[0], -p[1]
        to_p = list(rot_left[p[0]][p[1]])

        cell.setValue(0, False)

        new_position = [rotter_position[0] + to_p[0], rotter_position[1] + to_p[1]]
        new = grid.getCellAt(new_position[0], new_position[1])
        if new is None:
            grid.setCellAt(new_position[0], new_position[1], 1, False)
        else:
            new.setValue(1, False)

    elif myself.value == 1 and len(black_positions) == 0:
        cell.setValue(0, False)

        for x in explosion:
            c = myself.getCellAwayFrom(x[0], x[1])
            if c is None:
                grid.setCellAt(myself.i + x[0], myself.j + x[1], False)
            else:
                c.setValue(1, False)

    elif myself.value == 1 and len(black_positions) == 0:
        cell.setValue(0, False)

        for x in explosion:
            c = myself.getCellAwayFrom(x[0], x[1])
            if c is None:
                grid.setCellAt(myself.i + x[0], myself.j + x[1], False)
            else:
                c.setValue(1, False)

    else:
        if pair_num == 1 or pair_num == 3:
            if cell is None:
                cell = grid.setCellAt(i, j, 0)

            value = cell.value
            if value is None:
                value = 0
            cell.setValue(abs(value - 1), False)


step = 0
while True:
    step += 1

    startTime = time.time()

    if grid.width() * grid.height() > max_w * max_w:
        grid.bounded = True

    grid.traversalAreaThenUpdate(grid.minI, grid.minJ, grid.width(), grid.height(), onCell)

    if step > loopTimes:
        msg = "=" * (grid.width() + 2) * 2 + "\n"

        for i in range(grid.minI, grid.maxI + 1):
            line = "H "
            for j in range(grid.minJ, grid.maxJ + 1):
                cell = grid.getCellAt(i, j)
                if cell is None or cell.value is None or not cell.value == 1:
                    line += "  "
                else:
                    line += "EE"

            line += " H"

            msg += line + "\n"

        os.system(clear_screen_cmd)
        print(msg)
        time_used = time.time() - startTime
        print(step, "Time used :", time_used)
        pt = pause_time - time_used
        if pt > 0:
            time.sleep(pt)
        #input()
