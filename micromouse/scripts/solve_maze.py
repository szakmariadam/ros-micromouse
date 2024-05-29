import math
import numpy as np

#x --->
#y |
#  |
#  V


maze = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
['x', 's', 15, 14, 13, 12, 11, 10, 9, 8, 'x'],
['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 7, 'x'],
['x', 14, 15, 0, 0, 0, 0, 0, 'x', 6, 'x'],
['x', 13, 'x', 'x', 'x', 'x', 'x', 0, 'x', 5, 'x'],
['x', 12, 'x', 0, 0, 0, 'x', 0, 'x', 4, 'x'],
['x', 11, 'x', 0, 'x', 'x', 'x', 0, 'x', 3, 'x'],
['x', 10, 'x', 0, 0, 0, 0, 0, 'x', 2, 'x'],
['x', 9, 'x', 'x', 'x', 'x', 'x', 'x', 'x', 1, 'x'],
['x', 8, 7, 6, 5, 4, 3, 2, 1, 'g', 'x'],
['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]

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
print(waypoints,3)