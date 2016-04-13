import time
from core import procgrid

grid = procgrid.ProcessGrid()

grid.setCellAt(0, 0, 1)
grid.setCellAt(10, 10, 1)
grid.setCellAt(5, 15, 1)
grid.setCellAt(1, 2, 1)
grid.setCellAt(-5, -8, 1)
grid.setCellAt(-10, -3, 1)

loopTimes = 100

ant = [0, 0, 1] #1:(-1, 0), 2:(0, 1), 3:(1, 0), 4:(0, -1)
previous_ant = [0, 0, 1]
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

def antStep(grid):
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
        pass

    else: # 1, 0
        # black to white, avoid turning to black cell, and prefer to turn left, and set the cell after it black
        left_dir = ant_dir[turn_left(ant[2])]
        right_dir = ant_dir[turn_right(ant[2])]

        left_cell = grid.getCellAt(ant[0] + left_dir[0], ant[1] + left_dir[1])
        right_cell = grid.getCellAt(ant[0] + right_dir[0], ant[1] + right_dir[1])

        if left_cell is None or not left_cell.value == 1:
            ant[2] = turn_left(ant[2])
        elif right_cell is None or not right_cell.value == 1:
            ant[2] = turn_right(ant[2])
        else:
            ant[2] = turn_left(ant[2])

        new_dir = ant_dir[ant[2]]
        grid.setCellAt(ant[0] - new_dir[0], ant[1] - new_dir[1], 1)
        current_cell.value = 0


startTime = time.time()

step = 0
while True:
    step += 1

    antStep(grid)

    if step > 500:
        msg = "=" * (grid.width() + 2) * 2 + "\n"

        for i in range(grid.minI, grid.maxI + 1):
            line = "H "
            for j in range(grid.minJ, grid.maxJ + 1):
                if i == ant[0] and j == ant[1]:
                    line += ant_sym(ant[2])

                elif i == previous_ant[0] and j == previous_ant[1]:
                    line += ant_sym(previous_ant[2])

                else:
                    cell = grid.getCellAt(i, j)
                    if cell is None or cell.value is None or not cell.value == 1:
                        line += "  "
                    else:
                        line += "EE"

            line += " H"

            msg += line + "\n"

        print(msg)
        time.sleep(0.28)
        #input()

print("Time used :", time.time() - startTime)