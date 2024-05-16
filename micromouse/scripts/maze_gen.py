with open("test.sdf",'r+') as file:
    file.truncate(16)
testString=''
String1="""<?xml version='1.0'?>
<sdf version='1.7'>
  <model name='Untitled'>
    <pose>-2.9525 -2.0275 0 0 -0 0</pose>
    <link name='Wall_"""
String2="""'>
      <collision name='Wall_"""
String3="""_Collision'>
        <geometry>
          <box>
            <size>1.5 0.15 2.5</size>
          </box>
        </geometry>
        <pose>0 0 1.25 0 -0 0</pose>
      </collision>
      <visual name='Wall_"""
String4="""_Visual'>
        <pose>0 0 1.25 0 -0 0</pose>
        <geometry>
          <box>
            <size>1.5 0.15 2.5</size>
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
      <pose>"""
String5="""</pose>
    </link>
         <static>1</static>
  </model>
</sdf>"""
pose=[0,0,0,0,0,0]
for x in range(3):
  pose=[pose[0]+x*2, pose[1]+x*2, 0,0,0, x*1.5708]
  testString=testString+String1+str(x)+String2+str(x)+String3+str(x)+String4+str(pose[0])+' '+str(pose[1])+' '+str(pose[2])+' '+str(pose[3])+' '+str(pose[4])+' '+str(pose[5])+String5
with open("test.sdf","w") as f:
    f.writelines(testString)