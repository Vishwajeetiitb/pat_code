import os
import time
agents = [1,2,4,6,10]
# deads = [7]
runs = 5
os.system('rm -rf ./data/')
os.system('mkdir ./data/')

for i in agents:
	os.system('rm -rf ./data/cr'+str(i)+'/')
	os.system('mkdir ./data/cr'+str(i)+'/')
	# for k in deads:
	# 	os.system('rm -rf ./data/cr'+str(i)+'/'+str(k)+'dead')
	# 	os.system('mkdir  ./data/cr'+str(i)+'/'+str(k)+'dead')
for i in agents:
	for j in range(runs):
		# print(i,'cars ',k, ' is dead','run id is ',str(j))
		os.system('python3 no_dead.py '+str(i)+' '+str(j))
		time.sleep(2)
