import math
import numpy as np

def isNeighbour(maze, x, y, n):
    if maze[x-1][y]==n or maze[x+1][y]==n or maze[x][y-1]==n or maze[x][y+1]==n:
        return 1
    else:
        return 0
    
matrix = [[]]

f=open("temp.txt","r")

temp=f.read()

f.close()

rows=0

for i in range(0,len(temp)):
    if temp[i]=="\n":
        rows=rows+1
        matrix.append([])
    elif temp[i]!="," and temp[i]!="\n":
        if temp[i+1]!="," and temp[i]!="\n":
            matrix[rows].append(temp[i]+temp[i+1])
        elif temp[i-1]=="," or temp[i-1]=="\n":
            matrix[rows].append(temp[i])

for i in range(0, len(matrix)):
    for j in range(0, len(matrix[0])):
         if matrix[i][j]!="x" and matrix[i][j]!="s" and matrix[i][j]!="g":
            matrix[i][j]=int(matrix[i][j])

#maze=matrix

#térképezés eredménye:   
maze = [[ 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ,'x', 0 ],
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

# páratlan index 0: sarokú
# '-' helyett is 0

for i in range(0, len(maze)):
    for j in range(0, len(maze[0])):
        if i%2==0 and j%2==0 and maze[i][j]==0:
            maze[i][j]='x'
        elif maze[i][j] == '-':
            maze[i][j]=0

start = [1,1]
goal = [9,9]

maze[start[0]][start[1]]='s'
maze[goal[0]][goal[1]]='g'

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

#megoldott labirintus fileba irása

f = open("temp.txt", "w")
f.close()

f = open("temp.txt", "a")

for i in range(0, len(maze)):
    for j in range(0, len(maze[0])):
        f.write(str(maze[i][j]))
        f.write(",")
    if i!=len(maze)-1:
        f.write("\n")

f.close()