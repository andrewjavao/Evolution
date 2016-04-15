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

if len(sys.argv) > 1:
    loopTimes = int(sys.argv[1])

if len(sys.argv) > 2:
    pause_time = float(sys.argv[2])

grid = procgrid.ProcessGrid()

grid.setCellAt(0, 0, 1)
#grid.setCellAt(10, 10, 1)
#grid.setCellAt(5, 15, 1)
#grid.setCellAt(1, 2, 1)
#grid.setCellAt(-5, -8, 1)
#grid.setCellAt(-10, -3, 1)

ant1 = [0, 0, 1]
previous_ant1 = [0, 0, 1]

ant2 = [0, 0, 1]
previous_ant2 = [0, 0, 1]

ants = []
previous_ants = []

ants.append(ant1)
ants.append(ant2)

previous_ants.append(previous_ant1)
previous_ants.append(previous_ant2)

#1:(-1, 0), 2:(0, 1), 3:(1, 0), 4:(0, -1)
ant_dir = {1:[-1, 0], 2:[0, 1], 3:[1, 0], 4:[0, -1]}


def ant_sym(direct):
    if direct == 1:
        return "/\\"
    elif direct == 2:
        return "->"
    elif direct == 3:
        return "\\/"
    elif direct == 4:
        return "<-"
    else:
        return "O"

def turn_left(direct):
    direct -= 1
    if direct < 1:
        direct = 4

    return direct

def turn_right(direct):
    direct += 1
    if direct > 4:
        direct = 1

    return direct

def antStep(grid, ant, previous_ant):
    previous_ant[0], previous_ant[1], previous_ant[2] = ant[0], ant[1], ant[2]

    current_i, current_j = ant[0], ant[1]
    direct = ant_dir[ant[2]]
    next_i, next_j = ant[0] + direct[0], ant[1] + direct[1]

    current_cell = grid.getCellAt(current_i, current_j)

    if current_cell is None or current_cell.value is None:
        current_cell = grid.setCellAt(current_i, current_j, 0)

    next_cell = grid.getCellAt(next_i, next_j)

    if next_cell is None or next_cell.value is None:
        next_cell = grid.setCellAt(next_i, next_j, 0)

    #ant move
    ant[0] += direct[0]
    ant[1] += direct[1]

    if current_cell.value == 1 and next_cell.value == 1:
        # black to black, turn right, and set previous cell white
        ant[2] = turn_right(ant[2])
        current_cell.value = 0

    elif current_cell.value == 0 and next_cell.value == 0:
        # white to white, turn left, and set previous cell black
        ant[2] = turn_left(ant[2])
        current_cell.value = 1

    elif current_cell.value == 0 and next_cell.value == 1:
        # white to black, no turning, no changing
        ant[2] = turn_right(ant[2])
        current_cell.value = 1

    else: # 1, 0
        # black to white, avoid turning to black cell, and prefer to turn left, and set the cell after it black
        left_dir = ant_dir[turn_left(ant[2])]
        right_dir = ant_dir[turn_right(ant[2])]

        left_cell = grid.getCellAt(ant[0] + left_dir[0], ant[1] + left_dir[1])
        right_cell = grid.getCellAt(ant[0] + right_dir[0], ant[1] + right_dir[1])

        left_black = left_cell is None or not left_cell.value == 1
        right_black = right_cell is None or not right_cell.value == 1

        if not left_black == right_black:
            ant[2] = turn_left(ant[2])

        current_cell.value = 0


startTime = time.time()

step = 0
while True:
    step += 1

    for x in range(0, len(ants)):
        antStep(grid, ants[x], previous_ants[x])

    #check ants
    ant_index = {}
    new_ants = []
    new_previous_ants = []

    for x in range(0, len(ants)):
        ant = ants[x]

        if ant[0] in ant_index and ant[1] in ant_index[ant[0]]:
            if ant[2] in ant_index[ant[0]][ant[1]]: # the same ant
                new_ants.append([ant[0], ant[1], turn_right(ant[2])])
                new_previous_ants.append([ant[0], ant[1], turn_right(ant[2])])
                ant[2] = turn_left(ant[2])
                ant_index[ant[0]][ant[1]][ant[2]] = 1

        if ant[0] not in ant_index:
            ant_index[ant[0]] = {}
        if ant[1] not in ant_index[ant[0]]:
            ant_index[ant[0]][ant[1]] = {}
        ant_index[ant[0]][ant[1]][ant[2]] = 1

    ants.extend(new_ants)
    previous_ants.extend(new_previous_ants)

    if step > loopTimes:
        msg = "=" * (grid.width() + 2) * 2 + "\n"

        for i in range(grid.minI, grid.maxI + 1):
            line = "H "
            for j in range(grid.minJ, grid.maxJ + 1):
                is_ant = False

                for x in range(0, len(ants)):
                    if i == ants[x][0] and j == ants[x][1]:
                        line += ant_sym(ants[x][2])
                        is_ant = True

                    if is_ant:
                        break

                if not is_ant:
                    for x in range(0, len(previous_ants)):
                        if i == previous_ants[x][0] and j == previous_ants[x][1]:
                            line += ant_sym(previous_ants[x][2])
                            is_ant = True

                        if is_ant:
                            break

                if not is_ant:
                    cell = grid.getCellAt(i, j)
                    if cell is None or cell.value is None or not cell.value == 1:
                        line += "  "
                    else:
                        line += "EE"

            line += " H"

            msg += line + "\n"

        print(msg)
        print(step, "Ant Number:", len(ants))
        time.sleep(pause_time)
        os.system(clear_screen_cmd)
        #input()

print("Time used :", time.time() - startTime)