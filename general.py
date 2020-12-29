import os
import time
agents = [1,2,4,6,10]
runs = 1
os.system('rm -rf ./data/')
os.system('mkdir ./data/')

for i in agents:
	os.system('rm -rf ./data/cr'+str(i)+'/')
	os.system('mkdir ./data/cr'+str(i)+'/')

for i in agents:
	for j in range(runs):
		print(i,'cars ','run id is ',str(j))
		os.system('python3 no_dead_code.py '+str(i)+' '+str(j))
		time.sleep(2)
