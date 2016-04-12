import this
import time
import random

accessTimes = 1000000

dic = {0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{}}
lst = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]



def accessDict(i, j):
    dic[i][j] = i


def accessList(i, j):
    lst[i][j] = i


startTime = time.time()

for i in range(0, accessTimes):
    index1 = random.randint(0,9)
    index2 = random.randint(0,i+10)
    accessDict(index1, index2)

deltaTime = time.time() - startTime
print("Time Used:", deltaTime)