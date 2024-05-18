import math
import numpy as np

def isNeighbour(maze, x, y, n):
    if maze[x-1][y]==n or maze[x+1][y]==n or maze[x][y-1]==n or maze[x][y+1]==n:
        return 1
    else:
        return 0
#térképezés eredménye:   
maz1 = [[ 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ],
        ['x','s','-', 0 ,'-', 0 ,'-', 0 ,'-', 0 ,'x'],
        [ 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'-', 0 ],
        ['x', 0 ,'-', 0 ,'-', 0 ,'-', 0 ,'x', 0 ,'x'],
        [ 0 ,'-', 0 ,'x', 0 ,'x', 0 ,'-', 0 ,'-', 0 ],
        ['x', 0 ,'x', 0 ,'-', 0 ,'x', 0 ,'x', 0 ,'x'],
        [ 0 ,'-', 0 ,'-', 0 ,'x', 0 ,'-', 0 ,'-', 0 ],
        ['x', 0 ,'x', 0 ,'-', 0 ,'-', 0 ,'x', 0 ,'x'],
        [ 0 ,'-', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'-', 0 ],
        ['x', 0 ,'-', 0 ,'-', 0 ,'-', 0 ,'-','g','x'],
        [ 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ]]
# páratlan index 0: sarok
maz2 = [['x','x','x','x','x','x','x','x','x','x','x'],
        ['x','s','-', 0 ,'-', 0 ,'-', 0 ,'-', 0 ,'x'],
        ['x','x','x','x','x','x','x','x','x','-','x'],
        ['x', 0 ,'-', 0 ,'-', 0 ,'-', 0 ,'x', 0 ,'x'],
        ['x','-','x','x','x','x','x','-','x','-','x'],
        ['x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x'],
        ['x','-','x','-','x','x','x','-','x','-','x'],
        ['x', 0 ,'x', 0 ,'-', 0 ,'-', 0 ,'x', 0 ,'x'],
        ['x','-','x','x','x','x','x','x','x','-','x'],
        ['x', 0 ,'-', 0 ,'-', 0 ,'-', 0 ,'-','g','x'],
        ['x','x','x','x','x','x','x','x','x','x','x']]

# '-' helyett is 0
maze = [['x','x','x','x','x','x','x','x','x','x','x'],
        ['x','s', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,'x'],
        ['x','x','x','x','x','x','x','x','x', 0 ,'x'],
        ['x', 0 , 0 , 0 , 0 , 0 , 0 , 0 ,'x', 0 ,'x'],
        ['x', 0 ,'x','x','x','x','x', 0 ,'x', 0 ,'x'],
        ['x', 0 ,'x', 0 , 0 , 0 ,'x', 0 ,'x', 0 ,'x'],
        ['x', 0 ,'x', 0 ,'x','x','x', 0 ,'x', 0 ,'x'],
        ['x', 0 ,'x', 0 , 0 , 0 , 0 , 0 ,'x', 0 ,'x'],
        ['x', 0 ,'x','x','x','x','x','x','x', 0 ,'x'],
        ['x', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,'g','x'],
        ['x','x','x','x','x','x','x','x','x','x','x']]


start = [1,1]
goal = [9,9]

for i in range(0, len(maze)):
    for j in range(0, len(maze[0])):
        if maze[i][j]==0 and isNeighbour(maze, i, j, 'g'):
            maze[i][j]=1

a = 1

while isNeighbour(maze, start[0], start[1], 0)==1:
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j]==0 and isNeighbour(maze, i, j, a):
                maze[i][j]=a+1
    a=a+1

for i in range(0,len(maze)):
    print(maze[i])