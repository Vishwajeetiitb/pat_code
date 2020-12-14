from pynput.mouse import Button, Controller
import os

mouse = Controller()
import time
time.sleep(5)
# Read pointer position
a = mouse.position
os.system('rm mouse_pose_x.txt')
f = open("mouse_pose_x.txt", "a")
f.write(str(a[0]))
f.close()
os.system('rm mouse_pose_y.txt')
f = open("mouse_pose_y.txt", "a")
f.write(str(a[1]))
f.close()
