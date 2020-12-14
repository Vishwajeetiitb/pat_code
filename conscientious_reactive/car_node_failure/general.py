import os
import time
agents = [1,2,4,6,10]
deads = [0,2,12]
runs = 5
os.system('rm -rf ./data/')
os.system('mkdir ./data/')

for i in agents:
	os.system('rm -rf ./data/cr'+str(i)+'/')
	os.system('mkdir ./data/cr'+str(i)+'/')
	for k in deads:
		os.system('rm -rf ./data/cr'+str(i)+'/'+str(k)+'dead')
		os.system('mkdir  ./data/cr'+str(i)+'/'+str(k)+'dead')
for i in agents:
	for k in deads:
		for j in range(runs):
			print(i,'cars ',k, ' is dead','run id is ',str(j))
			os.system('python3 server_cr_n_car_node_failure.py '+str(i)+' '+str(k)+' '+str(j))
			time.sleep(2)
