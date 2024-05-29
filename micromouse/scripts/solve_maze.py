import math
import numpy as np

#x --->
#y |
#  |
#  V

#megoldott labirintus fileból kiolvasása

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

for i in range(0,len(matrix)):
    print(matrix[i])


#waypointok kiszámolása

maze = matrix

start = [1,1]
goal = [9,9]

position = start

waypoints = [[0.155, 0.155]]

if maze[position[0]-1][position[1]]!='x' and maze[position[0]-1][position[1]]!=0:
    distance=maze[position[0]-2][position[1]]
    position[0]=position[0]-2
    waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]-0.31,3)])
elif maze[position[0]+1][position[1]]!='x' and maze[position[0]+1][position[1]]!=0:
    distance=maze[position[0]+2][position[1]]
    position[0]=position[0]+2
    waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]+0.31,3)])
elif maze[position[0]][position[1]-1]!='x' and maze[position[0]][position[1]-1]!=0:
    distance=maze[position[0]][position[1]-2]
    position[1]=position[1]-2
    waypoints.append([round(waypoints[len(waypoints)-1][0]-0.31,3),waypoints[len(waypoints)-1][1]])
elif maze[position[0]][position[1]+1]!='x' and maze[position[0]][position[1]+1]!=0:
    distance=maze[position[0]][position[1]+2]
    position[1]=position[1]+2
    waypoints.append([round(waypoints[len(waypoints)-1][0]+0.31,3),waypoints[len(waypoints)-1][1]])

while position!=goal:
    if maze[position[0]-1][position[1]]==distance-1:
        distance=maze[position[0]-2][position[1]]
        position[0]=position[0]-2
        waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]-0.31,3)])
    elif maze[position[0]+1][position[1]]==distance-1:
        distance=maze[position[0]+2][position[1]]
        position[0]=position[0]+2
        waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]+0.31,3)])
    elif maze[position[0]][position[1]-1]==distance-1:
        distance=maze[position[0]][position[1]-2]
        position[1]=position[1]-2
        waypoints.append([round(waypoints[len(waypoints)-1][0]-0.31,3),waypoints[len(waypoints)-1][1]])
    elif maze[position[0]][position[1]+1]==distance-1:
        distance=maze[position[0]][position[1]+2]
        position[1]=position[1]+2
        waypoints.append([round(waypoints[len(waypoints)-1][0]+0.31,3),waypoints[len(waypoints)-1][1]])

print(position)
print(distance)
print(waypoints)