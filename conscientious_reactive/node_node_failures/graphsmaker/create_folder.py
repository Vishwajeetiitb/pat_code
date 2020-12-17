import os
f = open("./path_name.txt", "r")
path = './data/' + f.read() +'individual/'
os.system('rm -rf '+path)
os.system('mkdir '+path)
