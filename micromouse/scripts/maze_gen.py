with open("test/test.sdf",'r+') as file:
    file.truncate(16)
testString=''
Strings=["""<link name='Wall_""","""'>
      <collision name='Wall_""","""_Collision'>
        <geometry>
          <box>
            <size>0.31 0.012 0.20</size>
          </box>
        </geometry>
        <pose>0 0 0.1 0 -0 0</pose>
      </collision>
      <visual name='Wall_""","""_Visual'>
        <pose>0 0 0.1 0 -0 0</pose>
        <geometry>
          <box>
            <size>0.31 0.012 0.20</size>
          </box>
        </geometry>
        <material>
          <script>
            <uri>file://media/materials/scripts/gazebo.material</uri>
            <name>Gazebo/Grey</name>
          </script>
          <ambient>1 1 1 1</ambient>
        </material>
        <meta>
          <layer>0</layer>
        </meta>
      </visual>
      <pose>""","""</pose>
    </link>"""]

pose=[0,0,0,0,0,0]


vertical_walls=[[1,0,0,1,0,0,0,1,1],[1,0,0,0,1,0,0,0,1],[1,0,0,1,0,0,1,0,1],[1,0,1,1,0,1,0,0,1],[1,1,0,1,1,0,1,0,1],[1,1,0,1,0,1,0,1,1],[1,1,1,1,0,0,1,1,1],[1,1,0,0,0,0,0,0,1]]
horizontal_walls=[[1,1,1,1,1,1,1,1],[0,1,0,1,1,1,0,0],[1,1,1,0,1,1,1,0],[1,1,0,0,1,0,0,1],[0,0,0,0,1,0,1,1],[0,1,0,1,0,1,0,0],[0,0,1,0,1,0,0,0],[0,0,0,1,1,1,1,0],[1,1,1,1,1,1,1,1]]
wall_id=0
wall_length=0.31
testString="""<?xml version='1.0'?>
<sdf version='1.7'>
  <model name='Untitled'>
    <pose>0 0 0 0 -0 0</pose>
    """
for i in range(8):
   for j in range(9):
       if vertical_walls[i][j]:
          pose=[wall_length*i, wall_length*j, 0,0,0, 0]
          testString=testString+Strings[0]+str(wall_id)+Strings[1]+str(wall_id)+Strings[2]+str(wall_id)+Strings[3]+str(pose[0])+' '+str(pose[1])+' '+str(pose[2])+' '+str(pose[3])+' '+str(pose[4])+' '+str(pose[5])+Strings[4]
          wall_id +=1
for i in range(9):
   for j in range(8):
       if horizontal_walls[i][j]:
          pose=[wall_length*i-wall_length/2, wall_length*j+wall_length/2, 0,0,0, 1.5708]
          testString=testString+Strings[0]+str(wall_id)+Strings[1]+str(wall_id)+Strings[2]+str(wall_id)+Strings[3]+str(pose[0])+' '+str(pose[1])+' '+str(pose[2])+' '+str(pose[3])+' '+str(pose[4])+' '+str(pose[5])+Strings[4]
          wall_id +=1



      
#for x in range(3):
#  pose=[pose[0]+x*2, pose[1]+x*2, 0,0,0, x*1.5708]
#  testString=testString+String1+str(wall_id)+String2+str(x)+String3+str(wall_id)+String4+str(pose[0])+' '+str(pose[1])+' '+str(pose[2])+' '+str(pose[3])+' '+str(pose[4])+' '+str(pose[5])+String5

testString+="""<static>1</static>
  </model>
</sdf>"""
with open("test/test.sdf","w") as f:
    f.writelines(testString)



