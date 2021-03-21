import os
with open('./mouse_pose_x.txt') as f:
	x = int(f.read())
	
with open('./mouse_pose_y.txt') as f:
	y = int(f.read())
print(x,y)
for i in range(80):
	print(i)
	os.system('python3 ../../server2.py '+str(x)+' '+str(y))

