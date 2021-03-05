import socket
import time
from pynput.keyboard import Key, Controller
from pynput.mouse import Button
from pynput.mouse import Controller as Controller2
import sys
x = int(sys.argv[1])
y = int(sys.argv[2])
keyboard = Controller()
mouse = Controller2()
def server():
  host = socket.gethostname()   # get local machine name
  port = 8060  # Make sure it's within the > 1024 $$ <65535 range

  s = socket.socket()
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  s.bind((host, port))

  s.listen(1)
  client_socket, adress = s.accept()
  print("Connection from: " + str(adress))
  time.sleep(2)
  mouse.position = (x,y)
  time.sleep(2)
  mouse.press(Button.left)
  time.sleep(0.1)
  mouse.release(Button.left)
  while True:
    data = client_socket.recv(1024).decode('utf-8')


    # print('From online user: ' + data)
    if data == 'q':
      print('From online user: ' + data)
      time.sleep(1)
      mouse.position = (x+20,y+20)
      mouse.press(Button.left)
      time.sleep(1)
      mouse.release(Button.left)
      time.sleep(1)
      keyboard.press(Key.enter)
      time.sleep(0.1)
      keyboard.release(Key.enter)
      time.sleep(1)
      keyboard.press(Key.alt)
      keyboard.press(Key.f4)
      time.sleep(0.1)
      keyboard.release(Key.alt)
      keyboard.release(Key.f4)
      time.sleep(1)
      mouse.position = (x,y)
      mouse.press(Button.left)
      time.sleep(1)
      mouse.release(Button.left)
      # mouse.move(0,0)
      client_socket.close()
      break


server()
